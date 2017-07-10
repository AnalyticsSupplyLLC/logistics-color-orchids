'''
Created on Dec 17, 2016

@author: jason

THis is just my way of making the REST stuff work
'''
from application.models import Customer, Location, RouteEntryMain, RouteStops, Operator

from google.appengine.ext import ndb

from application.views.admin import authen
from datetime import datetime
from application.rest import DispatcherException, Dispatcher
from flask import make_response,jsonify

from exceptions import AttributeError
import sys, traceback
from application.decorators import login_required, admin_required

Dispatcher.base_url = "/rest"
Dispatcher.add_models({"customer": Customer,'location':Location, 'operator':Operator,   
                       "routeentrymain":RouteEntryMain,'routestops':RouteStops})


form_options = {'boolean':{'type':'fixed',
                           'values':['true','false'],
                           'field':'boolean',
                           'key':'id',
                           'name':'boolean',
                           'filters':[]},
               'locations':{'type':'model',
                            'values':[],
                            'field':'location_name',
                            'key':'id',
                            'name':'Location',
                            'filters':[{'field':'product','key':True,'type':'Customer'}]},
                'operators':{'type':'model',
                             'values':[],
                             'field':'operator_name',
                             'key':'operator_name',
                             'name':'Operator',
                             'filters':[]},
                'customers':{'type':'model',
                             'values':[],
                             'field':'customer_name',
                             'name':'Customer',
                             'key':'id',
                             'filters':[]}}
@admin_required
def get_option_field(field, filters):
    form_field = form_options.get(field,None)
    resp = {}
    resp['values'] = []
    if form_field:
        if form_field['type'] == 'fixed':
            for value in form_field['values']:
                resp['values'].append({'key':value, 'value':value})
        else:
            if form_field['type'] == 'model':
                where_cls = ""
                if filters and len(form_field['filters']) > 0:
                    wheres = []
                    for filt in form_field['filters']:
                        name = filt['field']
                        isKey = filt['key']
                        mType = filt['type']
                        if name in filters.keys():
                            if not isKey:                            
                                wheres.append("{} = {}".format(name,filters[name]))
                            else:
                                wheres.append("{} = KEY('{}',{})".format(name,mType,filters[name]))
                    if len(wheres) > 0:
                        where_cls = "WHERE "
                        for w in wheres:
                            where_cls = where_cls + w + " AND "
                        where_cls = where_cls[:-5]
                stmt = "SELECT * FROM {} "+where_cls
                stmt = stmt.format(form_field['name'])
                model = ndb.gql(stmt)
                for m in model:
                    key = ""
                    field = ""
                    field_name = form_field['field']
                    if len(field_name.split(".")) > 1:
                        parts = field_name.split(".")
                        p = m
                        for i in range(len(parts)):
                            if i+1 < len(parts):
                                p = getattr(p,parts[i]).get()
                            else:
                                field = getattr(p,parts[i])
                    else:
                        field = getattr(m,form_field['field'])
                    key_name = form_field['key']
                    if len(key_name.split(".")) > 1:
                        parts = key_name.split(".")
                        p = m
                        for i in range(len(parts)):
                            if i+1 < len(parts):
                                p = getattr(p,parts[i]).get()
                            else:
                                key = getattr(p,parts[i])
                    else:
                        key = getattr(m,form_field['key'])
                            
                    resp['values'].append({'key':key,'value':field})
    return resp
                
        
    

updates = {'Customer':{'options':[], 
                      'update_name':'Customer',
                      'fields':{'customer_name':'i'},
                      'order':['customer_name'],
                      'style':'in_line'},
           'Operator':{'options':[],
                       'update_name':'Operator',
                       'fields':{'operator_name':'i','operator_other':'i'},
                       'order':['operator_name','operator_other'],
                       'style':'in_line'},
           'Location':{'options':[{'field_name':'customer', 'option_name':'customers'}],
                    'update_name':'Location',
                    'fields':{'location_name':'i','city':'i','zipcode':'i','milesFromCompany':'i','customer':'h'},
                    'order':['location_name','city','zipcode','milesFromCompany'],
                    'style':'in_line'}}

Dispatcher.authenticator = authen.BasicAuthenticator()
Dispatcher.authorizer = authen.OwnerAuthorizer()

def process_rest_request(path, request,response):
    print(path)
    d = Dispatcher(request,response)
    try:
        if request.method == "PUT":
            d.put()
        elif request.method == "DELETE":
            d.delete()
        elif request.method == "POST":
            d.post()
        elif request.method == "GET":
            d.get()
        response = d.response
    except DispatcherException as e:
        #if d.response.status_code == 200:
        traceback.print_exc(file=sys.stdout)
        response = make_response("<html><body>{}: {}</body></html>".format(e.error_code,e.message),e.error_code)
    except AttributeError as err:
        print(err)
        traceback.print_exc(file=sys.stdout)
        response = make_response("<html><body>{}: Attribute Error</body></html>".format(err.message),500)
    except:
        traceback.print_exc(file=sys.stdout)
        print("Unexpected error:", sys.exc_info()[0])
        response = make_response("<html><body>{}: Bad Request</body></html>".format(sys.exc_info()[0]),500)
        
        
    
    return response

@login_required
def get_update_info(update_name):
    if update_name in updates.keys():
        return jsonify({'status':'success','message':'Pulled update info for: '+update_name,'payload':updates[update_name]})
    else:
        return jsonify({'status':'failed','message':'Update Name Does Not Exist','payload':{}})
