select l.update_ts,l.* from logistics_stop as l where route_end_date is not null order by update_ts desc;

-- INSERT INTO `logistics_stop` (`id`,`route_id`,`route_start_date`,`operator_name`,`customer_name`,`ship_to`,`customer_zip`,`total_miles`,`carts`,`pallets`,`percent_load`,`stop_misc`,`stop_operator_pay`,`customer_cost`,`percent_freight`,`revenue_per_mile`,`cost_per_mile`) VALUES ('2082017SPI','2082017SPI','2017-2-8','Spiece','Costco','227',22153,21.7409240924092,1,0,0.02,0,12.168096809681,512.16,0.0237583895846629,23.5574163187856,0.559686274509804);

-- update logistics_stop set route_id = 'Updated Route' where id = '5739407210446848_5629499534213120'