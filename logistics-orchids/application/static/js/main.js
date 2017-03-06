var Utils = {
    renderFieldErrorTooltip: function (selector, msg, placement) {
        var elem;
        if (typeof placement === 'undefined') {
            placement = 'right'; // default to right-aligned tooltip
        }
        elem = $(selector);
        elem.tooltip({'title': msg, 'trigger': 'manual', 'placement': placement});
        elem.tooltip('show');
        elem.addClass('error');
        elem.on('focus click', function(e) {
            elem.removeClass('error');
            elem.tooltip('hide');
        });
    }
};

/* Your custom JavaScript here */

function load_customers(infunction){
	var url = "/customers";
	  $.getJSON( url, function(data) {
		  customers = data;
		  infunction();
	  } );
}

function get_locations(cust_id,locations,infunction){
	var url = "/locations/"+cust_id;
	$.getJSON(url, function(data){
		locations[cust_id] = data;
		infunction(cust_id);
	});
}

function init_locations(customers,locations, init_idx, infunction){
	var arrayLength = customers.length;
	
	for (var i = 0; i < arrayLength; i++){
		locations[customers[i]['value']] = [];
	}
	get_locations(customers[init_idx]['value'],locations,infunction);
}

function isEmpty(obj) {
	  return Object.keys(obj).length === 0;
	}

function switch_to_select(input_id, options){
	var opPar = $('#'+input_id).parent();
	$('#'+input_id).remove();
	opPar.append('<select name="'+input_id+'", id="'+input_id+'" type="text" class="form-control" ></select>');
	var arrayLength = options.length;
	for (var i = 0; i < arrayLength; i++) {
	    if (i == 0){
	    	$('#'+input_id).append('<option selected="selected" value="'+options[i]['value']+'">'+options[i]['display']+'</option>');
	    }else{
	    	$('#'+input_id).append('<option value="'+options[i]['value']+'">'+options[i]['display']+'</option>');
	    }
	}
}