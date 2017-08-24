"""
Initialize Flask app

"""
from flask import Flask, jsonify, request, make_response
import os,sys
import traceback
import datetime
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from models import DBEntry
from application.decorators import login_required, admin_required
from application.models import Operator

from google.appengine.api.taskqueue import taskqueue

app = Flask('application')

app.config['SQLALCHEMY_DATABASE_URI'] = DBEntry.get_connection_string('Datawarehouse')
db = SQLAlchemy(app)


from database import store_route_stop, update_all_by_ndb, update_all_by_date2, update_all
from initialize import init_customer_location
from models import Customer,RouteEntryMain,Operator

if os.getenv('FLASK_CONF') == 'TEST':
    app.config.from_object('application.settings.Testing')

elif 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    # Development settings
    app.config.from_object('application.settings.Development')
    # Flask-DebugToolbar
    toolbar = DebugToolbarExtension(app)

    # Google app engine mini profiler
    # https://github.com/kamens/gae_mini_profiler
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    _temp = __import__('gae_mini_profiler', globals(), locals(), ['profiler', 'templatetags'], -1)
    profiler = _temp.profiler
    templatetags = _temp.templatetags
    #from gae_mini_profiler import profiler, templatetags
    #from flasext.gae_mini_profiler import profiler

    @app.context_processor
    def inject_profiler():
        return dict(profiler_includes=templatetags.profiler_includes())
    app.wsgi_app = profiler.ProfilerWSGIMiddleware(app.wsgi_app)
else:
    app.config.from_object('application.settings.Production')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Pull in URL dispatch routes
import urls
import restful

@app.route('/rest')
@app.route('/rest/<path:path>/',methods=['DELETE', 'GET', 'GET_METADATA', 'POST', 'PUT'])
def rest_impl(path):
    return restful.process_rest_request(path, request,make_response())

@app.route('/store-result/<int:route_main>/<int:route_entry>', methods=['GET'])
def store_result(route_main,route_entry):
    store_route_stop(route_main, route_entry)
    return jsonify({'result':'success'})

@app.route('/syncdw', methods=['GET'])
def sync_datawarehouse():
    update_all_by_ndb()
    return jsonify({'result':'success'})

@app.route('/initcustloc',methods=['GET'])
def init_cust_loc():
    init_customer_location()
    return jsonify({'result':'success'})

@app.route('/customers', methods=['GET'])
@login_required
def get_customers():
    try:
        custs = Customer.get_customers()
        return jsonify(custs)
    except Exception:
        return traceback.format_exc()

@app.route('/locations/<int:cust_id>', methods=['GET'])
@login_required
def get_locations(cust_id):
    try:
        locs = Customer.get_locations(cust_id)
        return jsonify(locs)
    except Exception:
        msg = traceback.format_exc()
        print(msg)
        return jsonify({"problem":msg})

@app.route('/convert_expenses',methods=['GET'])
@admin_required
def convert_expenses():
    try:
        upd = RouteEntryMain.switch_to_misc()
        return jsonify({'result':'success','msg':upd})
    except Exception:
        msg = traceback.format_exc()
        print(msg)
        return jsonify({"problem":msg})
    
@app.route('/update_info/<path:path>/',methods=['DELETE', 'GET', 'GET_METADATA', 'POST', 'PUT'])
def get_update_info(path):
    return restful.get_update_info(path)

@app.route('/options/<path:path>/',methods=['GET'])
def get_options(path):
    r = restful.get_option_field(path, request.values)
    return jsonify(r)

@app.route('/add_operators',methods=['GET'])
def add_op():
    Operator.add_operators()
    return jsonify({'msg':'success'})

@app.route('/push_dw',methods=['GET','POST'])
def process_dw_task():
    process_task = request.values.get("task")
    process_step = request.values.get('process')
    task = taskqueue.add(
        url='/run_dw_task',
        target='worker',
        params={'task':process_task,'process':process_step})
    
    return jsonify({'task_name':task.name,'task_eta':task.eta})

@app.route('/run_dw_task',methods=['POST','GET'])
def run_dw_task():
    runtask = request.values.get('task')
    process = request.values.get("process") # either prep or run
    
    try:
        if runtask == 'syncdw':
            update_all_by_ndb()
        elif runtask == 'syncdw_all':
            update_all()
        elif runtask == 'syncdw_date':
            fromDate = datetime.datetime.strptime(process, '%m/%d/%Y')
            update_all_by_date2(fromDate)
            
            return jsonify({"status":"success"})
    except:
        traceback.print_exc(file=sys.stdout)
        print("Unexpected error:", sys.exc_info()[0])
        return jsonify({"status":"failed"})

if __name__ == "__main__":
    app.run()