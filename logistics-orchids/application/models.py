"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

class NDBBase(ndb.Model):
    added_by = ndb.UserProperty(auto_current_user_add=True)
    updated_by = ndb.UserProperty(auto_current_user=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    up_timestamp = ndb.DateTimeProperty(auto_now=True)
    
    @property
    def id(self):
        """Override for getting the ID.
        Resolves NotImplementedError: No `id` attribute - override `get_id`
        :rtype: str
        """
        return self.key.id()

    @classmethod
    def _post_get_hook(cls, key, future):
        self = future.get_result()
        if self:
            self._is_saved = bool(key)

    def _post_put_hook(self, future):
        self._is_saved = future.state == future.FINISHING

    def set_saved(self):
        self._is_saved = True

    def is_saved(self):
        if self._has_complete_key():
            return getattr(self, "_is_saved", False)
        return False
    
    def convert_bool(self, value):
        if str(value).lower().strip()  == "true":
            return True
        
        if str(value).lower().strip() == "1":
            return True
        return False

class DBEntry(ndb.Model):
    conn_name = ndb.StringProperty(required=True)
    conn_string = ndb.StringProperty(required=True)
    conn_user = ndb.StringProperty(required=True)
    conn_pass = ndb.StringProperty(required=True)
    conn_host = ndb.StringProperty(required=True)
    conn_port = ndb.StringProperty(required=True)
    conn_database = ndb.StringProperty(required=True)
    
    def set_password(self, password):
        self.conn_pass = generate_password_hash(password)
    
    @classmethod  
    def get_connection_string(cls,dbtype):
        dbe = DBEntry.query(DBEntry.conn_name == dbtype).get()
        if dbe:
            ##  mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
            #return dbe.conn_string+dbe.conn_user+":"+dbe.conn_pass+"@"+dbe.conn_host+":"+dbe.conn_port+"/"+dbe.conn_database
            dburl = dbe.conn_string+dbe.conn_user+":{}"+"@"+dbe.conn_host+dbe.conn_port+"/"+dbe.conn_database
            print(dburl)
            return dburl.format(dbe.conn_pass)
        else:
            db = DBEntry()
            db.conn_database = "x"
            db.conn_host = "x"
            db.conn_name = dbtype
            db.conn_pass = "x"
            db.conn_port = "x"
            db.conn_string = "x"
            db.conn_user = "x"
            db.put()
            return db
    
    
    

class LastUpdate(NDBBase):
    name = ndb.StringProperty(required=True)
    last_updated = ndb.DateTimeProperty()
    
    @classmethod
    def get_last_update(cls):
        lstUp = LastUpdate.query(LastUpdate.name == 'last_update').get()
        if not lstUp:
            lstUp = LastUpdate()
            lstUp.name = 'last_update'
            lstUp.last_updated = datetime.strptime('1/1/2015','%m/%d/%Y')
            lstUp.put()
        return lstUp
    
    def update(self):
        self.last_updated = datetime.now()
        self.put()
 
class Customer(NDBBase):
    customer_name = ndb.StringProperty(required=True)
    
    @property
    def locations(self):
        return Location.query(Location.customer == self.key).fetch()
    
    @classmethod
    def get_customer(cls,custName):
        return Customer.query(Customer.customer_name == custName).get()
    
    
    @classmethod
    def create_customer(cls,custName, _id=None):
        instance = None
        if _id:
            key = ndb.Key(Customer,_id)
            instance = Customer(key=key)
        else:
            instance = Customer()
        
        instance.customer_name = custName
        instance.put()
        return instance.key
    
    @classmethod
    def get_customers(cls):
        cust_list = []
        custs = Customer.query().order(Customer.customer_name).fetch()
        for cust in custs:
            cust_list.append({'display':cust.customer_name,'value':cust.id})
        return cust_list
    
    @classmethod
    def get_locations(cls, cust_id):
        cust = Customer.get_by_id(cust_id)
        loc_list = []
        locations = cust.locations
        for location in locations:
            loc_list.append({'value':location.id,'display':location.location_name,'zipcode':location.zipcode,'distance':location.milesFromCompany})
        return loc_list
           
class Location(NDBBase):
    location_name = ndb.StringProperty(required=True)
    city = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    milesFromCompany = ndb.FloatProperty()
    customer = ndb.KeyProperty(kind=Customer)
    
    @classmethod
    def get_location(cls, loc_id):
        return Location.get_by_id(loc_id)
    
    @classmethod
    def create_location(cls, name, city, zipcode, miles, cust_key):
        loc = Location()
        loc.location_name = name
        loc.city = city
        loc.zipcode = zipcode
        loc.milesFromCompany = miles
        loc.customer = cust_key
        loc.put()

class Operator(NDBBase):
    operator_name = ndb.StringProperty(required=True)
    operator_other = ndb.StringProperty(default="")
    
    @classmethod
    def add_operators(cls):
        op_arr = ['Paculua','American',
                  'Becker','Bell','CH Robin.','Comstock',
                  'Jackson','MJ Transp.','Peninsula','Pennys',
                  'Polo','R & K','Spiece','TJ Demarlo','Todd Smith','TQL']
        operators = Operator.query()
        cnt = 0
        for _ in operators:
            cnt = cnt + 1
            
        if cnt == 0:
            for op in op_arr:
                o = Operator()
                o.operator_name = op
                o.operator_other = ""
                o.put()
            
            
            
    
class RouteEntryMain(NDBBase):
    """Route Model"""
    route_date_start = ndb.DateProperty(required=True)
    route_date_end = ndb.DateProperty(required=True)
    operator_name = ndb.StringProperty(required=True)
    operator_pay = ndb.FloatProperty(required=True)
    hotel_expenses = ndb.FloatProperty(required=False)
    fuel_expenses = ndb.FloatProperty(required=False)
    
    misc_expenses = ndb.FloatProperty()
    #fuel_gallons = ndb.FloatProperty(required=False)
    total_miles = ndb.FloatProperty(required=False)
    #total_hours = ndb.FloatProperty(required=False)
    route_id = ndb.StringProperty()
    
    def get_route_id(self):
        if not self.route_id or self.route_id == "":
            return self.route_date_start.strftime('%m/%d/%Y')+"_"+self.operator_name
        return self.route_id
        
    @property
    def stops(self):
        return RouteStops.query(ancestor=self.key).fetch()
    
    @classmethod
    def get_by_date(cls, from_date):
        fromDate = from_date - timedelta(days=1)
        print("Pulling all updates from this time: "+str(fromDate))
        qry = RouteEntryMain.query(RouteEntryMain.up_timestamp >= fromDate)
        return qry.fetch()
    
    @classmethod
    def switch_to_misc(cls):
        qry = RouteEntryMain.query()
        update_list = []
        for route in qry:
            route.misc_expenses = route.hotel_expenses + route.fuel_expenses
            route.put()
            update_list.append({'id':route.id,'misc_expenses':route.misc_expenses,'status':'COMPLETE'})
        return update_list
    
    def default_nulls(self):
        if not self.operator_pay:
            self.operator_pay = 0.0
            
        if not self.hotel_expenses:
            self.hotel_expenses = 0.0
            
        if not self.fuel_expenses:
            self.fuel_expenses = 0.0
            
        if not self.fuel_gallons:
            self.fuel_gallons = 0.0
        
        if not self.total_miles:
            self.total_miles = 0.0
            
        if not self.total_hours:
            self.total_hours = 0.0
    
    
    def get_summary(self):
        d = {'stops':[]}

        for stop in self.stops:
            d['stops'].append(stop.get_stop_summary())
        
        return d
    
    def get_total_miles(self):
        dist = 0
        for stop in self.stops:
            dist += stop.stop_dist
            
        return dist
    
    def get_total_pallets(self):
        pallets = 0
        for stop in self.stops:
            pallets += stop.stop_pallets
            
        return pallets
    
    def get_total_carts(self):
        carts = 0
        for stop in self.stops:
            carts += stop.stop_carts
        
        return carts
        


class RouteStops(NDBBase):
    """ Route Stop """
    stop_name = ndb.StringProperty(required=True)
    stop_ship_to = ndb.StringProperty(required=True)
    stop_zip = ndb.StringProperty(required=True)
    stop_dist = ndb.IntegerProperty(required=True)
    stop_load = ndb.IntegerProperty(required=True)
    stop_pallets = ndb.IntegerProperty()
    
    #stop_ret_carts = ndb.IntegerProperty()
    stop_carts = ndb.IntegerProperty()
    customer_cost = ndb.FloatProperty(required=False)
    invoice_num = ndb.StringProperty()
    
    stop_company = ndb.StringProperty(default="Color Orchids")
    
    percent = None
    parent = None
    
    @classmethod
    def get_stop(cls, route_id, stop_id):
        #key = ndb.Key(RouteStops,stop_id)
        return RouteStops.get_by_id(stop_id, ndb.Key(RouteEntryMain,route_id))
    
    def check_parent_percent(self):
        self.check_parent()
            
        self.check_percent()
            
        if not self.customer_cost:
            self.customer_cost = 0.0
            
    def update_parent(self, up_time):
        self.check_parent()
        self.parent.up_timestamp = up_time
        self.parent.put()
            
    def check_parent(self):
        if not self.parent:
            self.parent = self.key.parent().get()
            
    def check_percent(self):
        if not self.percent:
            self.percent = self.get_percent_total()
            
    def get_percent_total(self, tot=None):
        if not tot:
            self.check_parent()
            tot = self.parent.get_total_miles()
        
        self.percent = float(self.stop_dist)/tot
        
        return self.percent
    
    def get_miles(self):
        self.check_parent_percent()
        return self.parent.total_miles * self.percent
    
    def get_hours(self):
        self.check_parent_percent()
        return self.parent.total_hours * self.percent
    
    def get_fuel_gallons(self):
        self.check_parent_percent()
        return self.parent.fuel_gallons * self.percent
    
    def get_operator_pay(self):
        self.check_parent_percent()
        return self.parent.operator_pay * self.percent
    
    def get_hotel_expenses(self):
        self.check_parent_percent()
        return self.parent.hotel_expenses * self.percent
    
    def get_fuel_expenses(self):
        self.check_parent_percent()
        return self.parent.fuel_expenses * self.percent
    
    def get_misc_expenses(self):
        self.check_parent_percent()
        return self.parent.misc_expenses * self.percent
    
    def get_trip_expenses(self):
        #return self.get_operator_pay() + self.get_hotel_expenses() + self.get_fuel_expenses()
        return self.get_operator_pay() + self.get_misc_expenses()
    
    def get_cost_per_mile(self):
        if not self.get_miles() or self.get_miles() == 0:
            return 0
        return self.get_trip_expenses() / self.get_miles()
    
    def get_revenue_per_mile(self):
        if not self.get_miles() or self.get_miles() == 0:
            return 0
        return self.customer_cost / self.get_miles()
    
    def get_percent_freight(self):
        self.check_parent_percent()
        if self.customer_cost == 0.0:
            return .0
        
        return self.get_trip_expenses() / self.customer_cost
    
    def get_fuel_rate(self):
        if self.get_fuel_gallons() == 0.0:
            return 0.0
        
        return self.get_miles()/self.get_fuel_gallons()
            
    def get_percent_load(self):
        self.check_parent_percent()
        maxNumber = 44
        tot = self.stop_carts
        if self.parent.get_total_pallets() > 0:
            maxNumber = 28
            tot = self.stop_pallets
        
        return tot/float(maxNumber)
    
    def get_stop_summary(self):
        metrics = ['_id','route_id','route_start_date','route_end_date','misc_expenses','total_miles',
                   'operator_name','operator_pay','customer_name','ship_to','customer_zip','miles_from_company','customer_cost',
                   'percent_load','pallets','carts','returned_carts','percent_of_total','stop_miles','invoice_num',
                   'stop_operator_pay','stop_misc','stop_company','percent_freight','cost_per_mile','revenue_per_mile']
        
        calcs = self.get_calculations()
        pd = self.parent.to_dict()
        ## convert dates
        #pd['route_date_start'] = pd['route_date_start'].strftime('%m/%d/%Y')
        #pd['route_date_end'] = pd['route_date_end'].strftime('%m/%d/%Y')
        
        pd['_id'] = str(self.parent.id) + "_" + str(self.id) 
        pd['route_id'] = self.parent.get_route_id()
        
        for key in pd.keys():
            calcs[key] = pd[key]
            
        cd = self.to_dict()
        
        for key in cd.keys():
            calcs[key] = cd[key]
        
        renames = self.get_renames()
        new_calcs = {}
        for key in calcs.keys():
            inkey = key
            outkey = key
            if inkey in renames.keys():
                outkey = renames[inkey]
            
            if outkey in metrics:
                new_calcs[outkey] = calcs[inkey]
        return new_calcs
            
        
    
    def get_calculations(self):
        d = {'percent_of_total':self.get_percent_total()}
        d['percent_load'] = self.get_percent_load()
        d['stop_miles'] = self.get_miles()
        #d['stop_hours'] = self.get_hours()
        #d['stop_fuel_gallons'] = self.get_fuel_gallons()
        d['stop_operator_pay'] = self.get_operator_pay()
        #d['stop_hotel'] = self.get_hotel_expenses()
        #d['stop_fuel'] = self.get_fuel_expenses()
        d['stop_misc'] = self.get_misc_expenses()
        d['percent_freight'] = self.get_percent_freight()
        #d['fuel_rate'] = self.get_fuel_rate()
        d['cost_per_mile'] = self.get_cost_per_mile()
        d['revenue_per_mile'] = self.get_revenue_per_mile()
        
        return d
    
    def get_renames(self):
        d = {}
        d['route_date_start'] = 'route_start_date'
        d['route_date_end'] = 'route_end_date'
        d['stop_name'] = 'customer_name'
        d['stop_ship_to'] = 'ship_to'
        d['stop_zip'] = 'customer_zip'
        d['stop_dist'] = 'miles_from_company'
        d['stop_pallets'] = 'pallets'
        d['stop_carts'] = 'carts'
        #d['stop_ret_carts'] = 'returned_carts'
        return d

class UserModel(ndb.Model):
    username = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)        

class User:
    pw_hash = None
    username = None
    
    def __init__(self, user, pw):
        self.username = user
        self.set_password(pw)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def get_model(self):
        return UserModel(username=self.username, pw_hash=self.pw_hash)
        
        
            
        
        
    
