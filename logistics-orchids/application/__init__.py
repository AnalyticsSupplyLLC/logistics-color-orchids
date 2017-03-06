"""
Initialize Flask app

"""
from flask import Flask, jsonify
import os
import traceback
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from models import DBEntry
from application.decorators import login_required

app = Flask('application')

app.config['SQLALCHEMY_DATABASE_URI'] = DBEntry.get_connection_string('Datawarehouse')
db = SQLAlchemy(app)


from database import store_route_stop, update_all_by_ndb
from initialize import init_customer_location
from models import Customer

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


@app.route('/store-result/<int:route_main>/<int:route_entry>', methods=['GET'])
def store_result(route_main,route_entry):
    store_route_stop(route_main, route_entry)
    return jsonify({'result':'success'})

@app.route('/syncdw', methods=['GET'])
@login_required
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
    

if __name__ == "__main__":
    app.run()