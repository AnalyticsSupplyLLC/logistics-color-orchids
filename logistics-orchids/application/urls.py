"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app

from application.views.public.public_warmup import PublicWarmup
from application.views.public.public_index import PublicIndex
from application.views.public.public_say_hello import PublicSayHello

from application.views.admin.admin_list_routes import AdminListExamples
#from application.views.admin.admin_list_examples_cached import AdminListExamplesCached
from application.views.admin.admin_secret import AdminSecret
from application.views.admin.admin_edit_route import AdminEditExample, AdminShowExample, AdminEditStop, AdminDeleteStop
from application.views.admin.admin_delete_route import AdminDeleteExample
from application.views.admin.add_db_entry import AdminAddDBEntry


# URL dispatch rules

# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'public_warmup', view_func=PublicWarmup.as_view('public_warmup'))

app.add_url_rule('/', 'public_index', view_func=PublicIndex.as_view('public_index'))

app.add_url_rule('/hello/<username>', 'public_say_hello', view_func=PublicSayHello.as_view('public_say_hello'))

app.add_url_rule('/routes', 'list_routes', view_func=AdminListExamples.as_view('list_routes'), methods=['GET', 'POST'])

#app.add_url_rule('/examples/cached', 'cached_examples', view_func=AdminListExamplesCached.as_view('cached_examples'))

app.add_url_rule('/admin_only', 'admin_only', view_func=AdminSecret.as_view('admin_only'))

app.add_url_rule('/routes/<int:route_id>/edit', 'edit_route', view_func=AdminEditExample.as_view('edit_route'), methods=['GET', 'POST'])

app.add_url_rule('/routes/<int:route_id>/delete', 'delete_route', view_func=AdminDeleteExample.as_view('delete_route'), methods=['POST'])

app.add_url_rule('/routes/<int:route_id>/show', 'show_route', view_func=AdminShowExample.as_view('show_route'),methods=['GET','POST'])

app.add_url_rule('/stops/<int:route_id>/<int:stop_id>/edit', 'edit_stop', view_func=AdminEditStop.as_view('edit_stop'),methods=['GET','POST'])

app.add_url_rule('/stops/<int:route_id>/<int:stop_id>/delete','delete_stop', view_func=AdminDeleteStop.as_view('delete_stop'),methods=['GET','POST'])

app.add_url_rule('/dbentry','db_entry',view_func=AdminAddDBEntry.as_view('db_entry'),methods=['GET','POST'])
# Error handlers

# Handle 404 errors


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
