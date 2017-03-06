# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.forms import get_db_form
from application.models import DBEntry

from application.decorators import admin_required
from wtforms import fields

class AdminAddDBEntry(View):

    @admin_required
    def dispatch_request(self):
        form = get_db_form()

        if request.method == "POST":
            if form.validate_on_submit():
                entry = DBEntry(
                    conn_name=form.conn_name.data,
                    conn_string=form.conn_string.data,
                    conn_user = form.conn_user.data,
                    conn_pass = form.conn_pass.data,
                    conn_host = form.conn_host.data,
                    conn_port = form.conn_port.data,
                    conn_database = form.conn_database.data
                    )
                entry.set_password(form.conn_pass.data)
                entry.put()
                entry_id = entry.key.id()
                #{{ url_for('list_routes') }}
                flash(u'DB Entry %s successfully saved.' % entry_id, 'success')
                return redirect(url_for('list_routes'))
        return render_template('add_db_entry.html',form=form)

