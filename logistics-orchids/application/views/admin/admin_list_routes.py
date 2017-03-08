# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.forms import RouteForm
from application.models import RouteEntryMain

from application.decorators import login_required

from datetime import datetime


class AdminListExamples(View):

    @login_required
    def dispatch_request(self):
        routes = RouteEntryMain.query()
        form = RouteForm()
        errors = 0
        if form.validate_on_submit():
            route = RouteEntryMain(
                route_date_start=form.route_date_start.data,
                route_date_end=form.route_date_end.data,
                operator_name=form.operator_name.data,
                operator_pay=form.operator_pay.data,
                hotel_expenses=form.hotel_expenses.data,
                fuel_expenses=form.fuel_expenses.data,
                misc_expenses=form.misc_expenses.data,
                route_id=form.route_id.data,
                #fuel_gallons=form.fuel_gallons.data,
                total_miles=form.total_miles.data,
                #total_hours=form.total_hours.data,
                added_by=users.get_current_user(),
                timestamp=datetime.now(),
                up_timestamp=datetime.now()
            )
            try:
                route.put()
                route_id = route.key.id()
                flash(u'Route %s successfully saved.' % route_id, 'success')
                return redirect(url_for('show_route',route_id=route_id))
            except CapabilityDisabledError:
                flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                return redirect(url_for('list_routes'))
        else:
            if request.method == 'POST':
                errors = 1
        return render_template('list_routes.html', routes=routes, form=form,errors=errors)
