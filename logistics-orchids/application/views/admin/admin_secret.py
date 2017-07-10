# -*- coding: utf-8 -*-

from flask.views import View

from decorators import admin_required
from flask import flash, redirect, url_for, render_template, request
from application.models import Customer

class AdminSecret(View):

    @admin_required
    def dispatch_request(self):

        return 'Super-seekrit admin page.'


class AdminUpdate(View):
    
    @admin_required
    def dispatch_request(self):
        models = ['Customer','Operator']
        return render_template('update_backend.html',models=models)
    
class AdminCustomerUpdate(View):
    
    @admin_required
    def dispatch_request(self, customer_id):
        customer = Customer.get_by_id(customer_id)
        return render_template('update_customer.html',customer_name=customer.customer_name, customer_id=customer.id)