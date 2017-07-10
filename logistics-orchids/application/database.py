'''
Created on Feb 25, 2017

@author: jason
'''

from application.models import RouteStops, RouteEntryMain, LastUpdate

from application import db

from datetime import datetime

def update_all_by_date(year, month, day):
    fromDate = datetime.strptime(str(month)+"/"+str(day)+"/"+str(year), '%m/%d/%Y')
    update_all_by_date2(fromDate)
    
def update_all_by_ndb():
    lstUp = LastUpdate.get_last_update()
    update_all_by_date2(lstUp.last_updated)
    lstUp.update()
    return 0
    

def update_all_by_date2(fromDate):
    routes = RouteEntryMain.get_by_date(fromDate)
    for route in routes:
        print("Updating Route: "+str(route.id))
        store_route_class(route)

def store_route(route_id):
    route = RouteEntryMain.get_by_id(route_id)
    store_route_class(route)
    
def store_route_class(route):
    stops = route.stops
    for stop in stops:
        print("Updating Stop: "+str(stop.id))
        store_route_stop(route.id, stop.id)
    

def store_route_stop(route_id,stop_id):
    stop = RouteStops.get_stop(route_id,stop_id)
    summary = stop.get_stop_summary()
    instance = db.session.query(RouteStop).filter_by(id=summary['_id']).first()
    if instance:
        del summary['_id']
        instance.update(**summary)
    else:
        instance = RouteStop(**summary)
        db.session.add(instance)
    db.session.commit() 
    
class RouteStop(db.Model):
    __tablename__ = 'logistics_stop'
    id = db.Column(db.String(80), primary_key=True)
    route_id = db.Column(db.String(80))
    route_start_date = db.Column(db.String(80))
    route_end_date = db.Column(db.String(80))
    #hotel_expenses = db.Column(db.String(80))
    misc_expenses = db.Column(db.String(80))
    #fuel_gallons = db.Column(db.String(80))
    total_miles = db.Column(db.String(80))
    #total_hours = db.Column(db.String(80))
    operator_name = db.Column(db.String(80))
    operator_pay = db.Column(db.String(80))
    customer_name = db.Column(db.String(80))
    ship_to = db.Column(db.String(80))
    customer_zip = db.Column(db.String(80))
    miles_from_company = db.Column(db.String(80))
    customer_cost = db.Column(db.String(80))
    percent_load = db.Column(db.String(80))
    pallets = db.Column(db.String(80))
    carts = db.Column(db.String(80))
    percent_of_total = db.Column(db.String(80))
    stop_miles = db.Column(db.String(80))
    #stop_hours = db.Column(db.String(80))
    #stop_fuel_gallons = db.Column(db.String(80))
    stop_operator_pay = db.Column(db.String(80))
    #stop_hotel = db.Column(db.String(80))
    stop_misc = db.Column(db.String(80))
    percent_freight = db.Column(db.String(80))
    #fuel_rate = db.Column(db.String(80))
    cost_per_mile = db.Column(db.String(80))
    revenue_per_mile = db.Column(db.String(80))
    invoice_num = db.Column(db.String(80))
    update_ts = db.Column(db.DateTime)
    
    def update(self, route_id, route_start_date,route_end_date,misc_expenses,total_miles,
                 operator_name,operator_pay,customer_name,ship_to,customer_zip,miles_from_company,
                 customer_cost,percent_load,pallets,carts,percent_of_total,stop_miles,
                 stop_operator_pay,stop_misc,percent_freight,cost_per_mile,revenue_per_mile,invoice_num):
        self.route_id = route_id
        self.route_start_date    =    route_start_date
        self.route_end_date    =    route_end_date
        #self.hotel_expenses    =    hotel_expenses
        self.misc_expenses    =    misc_expenses
        #self.fuel_gallons    =    fuel_gallons
        self.total_miles    =    total_miles
        #self.total_hours    =    total_hours
        self.operator_name    =    operator_name
        self.operator_pay    =    operator_pay
        self.customer_name    =    customer_name
        self.ship_to    =    ship_to
        self.customer_zip    =    customer_zip
        self.miles_from_company    =    miles_from_company
        self.customer_cost    =    customer_cost
        self.percent_load    =    percent_load
        self.pallets    =    pallets
        self.carts    =    carts
        self.percent_of_total    =    percent_of_total
        self.stop_miles    =    stop_miles
        #self.stop_hours    =    stop_hours
        #self.stop_fuel_gallons    =    stop_fuel_gallons
        self.stop_operator_pay    =    stop_operator_pay
        #self.stop_hotel    =    stop_hotel
        self.stop_misc    =    stop_misc
        self.percent_freight    =    percent_freight
        #self.fuel_rate    =    fuel_rate
        self.cost_per_mile    =    cost_per_mile
        self.revenue_per_mile    =    revenue_per_mile
        self.invoice_num = invoice_num
        self.update_ts = datetime.now()

    def __init__(self, _id,route_id, route_start_date,route_end_date,misc_expenses,total_miles,
                 operator_name,operator_pay,customer_name,ship_to,customer_zip,miles_from_company,
                 customer_cost,percent_load,pallets,carts,percent_of_total,stop_miles,
                 stop_operator_pay,stop_misc,percent_freight,cost_per_mile,revenue_per_mile,invoice_num):
        self.id    =    _id
        self.route_id = route_id
        self.route_start_date    =    route_start_date
        self.route_end_date    =    route_end_date
        #self.hotel_expenses    =    hotel_expenses
        self.misc_expenses    =    misc_expenses
        #self.fuel_gallons    =    fuel_gallons
        self.total_miles    =    total_miles
        #self.total_hours    =    total_hours
        self.operator_name    =    operator_name
        self.operator_pay    =    operator_pay
        self.customer_name    =    customer_name
        self.ship_to    =    ship_to
        self.customer_zip    =    customer_zip
        self.miles_from_company    =    miles_from_company
        self.customer_cost    =    customer_cost
        self.percent_load    =    percent_load
        self.pallets    =    pallets
        self.carts    =    carts
        self.percent_of_total    =    percent_of_total
        self.stop_miles    =    stop_miles
        #self.stop_hours    =    stop_hours
        #self.stop_fuel_gallons    =    stop_fuel_gallons
        self.stop_operator_pay    =    stop_operator_pay
        #self.stop_hotel    =    stop_hotel
        self.stop_misc    =    stop_misc
        self.percent_freight    =    percent_freight
        #self.fuel_rate    =    fuel_rate
        self.cost_per_mile    =    cost_per_mile
        self.revenue_per_mile    =    revenue_per_mile
        self.invoice_num = invoice_num
        self.update_ts = datetime.now()
