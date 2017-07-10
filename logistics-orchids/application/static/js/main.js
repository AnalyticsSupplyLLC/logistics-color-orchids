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
var set_message = function(message){
	jQuery(function () {
		  jQuery.notifyBar({
		    html: message,
		    delay: 2000,
		    animationSpeed: "normal"
		  });  
		});
}

$(document).ready(function() {
    $(".dropdown-toggle").dropdown();
});

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

function editRow(rowId, options, fields){  

	   for (var propertyName in fields)
	   {
		   var typ = fields[propertyName];
		   if (typ == 'o')
		   {
			  var opts = options[propertyName];
			  var optField = $('#'+rowId+"_"+propertyName);
			  optField.attr('class','edit-cell');
			  var name = optField.text();
			  var val = 0;
			  for (i = 0; i < opts.length; i++) { 
				    var n = opts[i].split(":");
				    if (name == n[0]){
				    	val = n[1];
				    }
				}
			  optField.text("");
			  d3.select('[id="'+rowId+'_'+propertyName+'"]')
			    .append("select")
			        .attr("id",rowId+"_sel"+propertyName)
			        .attr("class","form-control")
			          .selectAll("option").data(opts)
			            .enter().append("option")
			            .text(function (d) { return d.split(":")[0];})
			            .attr("value",function (d){ return d.split(":")[1];})
			  $("#"+rowId+"_sel"+propertyName).val(val);
			  
		   }
		   else if (typ == 'i'){
			   var inField = $('#'+rowId+"_"+propertyName);
			   var val = inField.text();
			   inField.text("");
			   //inField.css("background-color",'#fff');
			   inField.attr('class','edit-cell');
			   inField.css("display",'');
			   inField.css("color",'black');
			   d3.select('[id="'+rowId+'_'+propertyName+'"]')
			     .append('span')
			     .attr('contenteditable',true)
			     .attr('id',rowId+"_span"+propertyName)
			     .text(val);
		   }
		   else {
			   // DISPLAY/HIDDEN FIELDS
		   }
		   
	   }
	   $("#"+rowId+"_edit").hide();
	   $("#"+rowId+"_save").show();
	}

 function saveRowDT(rowId,options,fields,update,order, model_name){
 	var tableId = model_name+'-table';
 	saveRowDT2(rowId,options,fields,update,order, model_name,tableId);
 }

 function saveRowDT2(rowId,options,fields,update,order, model_name,tableId){
 	saveRow(rowId,options,fields,update);
		var t = $('#'+tableId).DataTable();
		var d = t.row($('#'+rowId)).data();
		for (i=0;i<order.length;i++){
			var prop = order[i];
			d[i] = $('#'+rowId+'_'+prop).text();
		}
		d[order.length] = $('#'+rowId+'_buttons').text();
		t.row($('#'+rowId)).data(d).draw();
		var btnId = rowId+"_buttons";
		add_buttons(rowId,model_name,d3.select('[id="'+btnId+'"]'));
		
 }

	function saveRow(rowId, options, fields, update){
		update['id'] = rowId;
		for (var propertyName in fields)
		{
			var typ = fields[propertyName];
			var idm = rowId+"_"+propertyName;
			
			if (typ == 'o'){
				var opts = options[propertyName];
				var ids = rowId+"_sel"+propertyName;
				var optField = $('#'+ids);
				var txtField = $('#'+idm);
				txtField.attr('class','display-cell');
				var val = optField.val();
				var name = "";
				for (i = 0; i < opts.length; i++) { 
				    var n = opts[i].split(":");
				    if (val == n[1]){
				    	name = n[0];
				    }
				}
				optField.remove();
				txtField.text(name);
				
			    update[propertyName] = val;
			}
			else if (typ == 'i'){
				var txtField = $('#'+idm);
				txtField.attr('class','display-cell');	
				var ids = rowId+"_span"+propertyName;
				var sField = $('#'+ids);
				var val = sField.text();
				sField.remove();
				txtField.text(val);
				txtField.css("background-color",'transparent');
				update[propertyName] = val;
			}
			else{
				// DISPLAY ONLY or HIDDEN FIELD
			}
		}
		$("#"+rowId+"_edit").show();
	    $("#"+rowId+"_save").hide();
	    if (update.service_name == 'add'){
	    	call_add_service(update.model_name,update,fields);
	    }
	    else{
	    	call_update_service(update);	
	    }
	}
	
	function check_numeric(value){
		if ($.isNumeric(value)){
			return value;
		}
		return 0;
	}
	
	function call_update_service(update_fields){
		var inData = adjust_data(update_fields);
		$.ajax({
		    type: "POST",
		    url: "/"+update_fields.service_name,
		    // The key needs to match your method's input parameter (case-sensitive).
		    data: JSON.stringify(inData),
		    contentType: "application/json; charset=utf-8",
		    dataType: "json",
		    success: function(data){
		    	var message = "Row Update Succeeded!!!"
		    	if (data.hasOwnProperty('status')){
		    		message = "Row Update Failed!!";
			    	if (data.status == 'success'){message = "Row Update Succeeded!!!";}
		    	}
		    	set_message(message)
		     },
		     error: function(data){
			        console.log(data.responseText);
			        //alert(json.error);},
			    },
			    failure: function(data){
			        console.log(data.responseText);
			        //alert(json.error);
			        }
		});
	}
	
	function call_add_service(model_name, update_fields,fields){
		var rowId = update_fields.id;
		var field_values = {};
		for (var propertyName in fields)
		{
			var typ = fields[propertyName];
			if (typ != 'd'){
				field_values[propertyName] = update_fields[propertyName];
			}
		}
		
		var inData = {};
		inData[model_name] = field_values;
		$.ajax({
			type: "POST",
			url: "/rest/"+model_name+"/",
			headers: { 
		        Accept : "application/json; charset=utf-8",
		        "Content-Type": "application/json; charset=utf-8"
		    },
		    data: JSON.stringify(inData),
		    dataType: "json",
		    success: function(data){
		    	//var id = data.key;
		    	set_message("Row Added Successfully");
		    	convert_save(rowId,data,model_name);
		    }
		    
			
		});
	}
	
	

	function addRow(model_name,options, fields, data){
		addRowDel(model_name,options, fields, data, false);
	}
	
	function delRow(rowId,options, fields, update){
		update['id'] = rowId;
    	update['soft_delete'] = true;
    	if (update.service_name != 'add'){
    		call_update_service(update);
    	}
    	
    	$('#'+rowId).remove();
    	$('#delete_modal').modal('hide');
    	$('#modal_del_btn').off('click');
    }
	
	function delRowDT(rowId, options, fields, update){
		update['id'] = rowId;
		update['soft_delete'] = true;
		var t = $('#'+update['model_name']+'-table').DataTable();
		if (update.service_name != 'add'){
    		call_update_service(update);
    	}
    	t.row($('#'+rowId)).remove().draw(false);
    	$('#delete_modal').modal('hide');
    	$('#modal_del_btn').off('click');
	}
	
	function addRowDel(model_name, options, fields, data, addDel){
		var tableId = model_name+"-table";	
		var rowId = tableId+"-newrow"+Math.round(Math.random() * 1000);
		data['id'] = rowId;
		data['model_name'] = model_name;
		data['service_name'] = 'add';
		var tr = d3.select('[id="'+tableId+'"]')
		  .select('tbody')
		  .append('tr');
		tr.attr('id',rowId);
		for (var propertyName in fields){
			var typ = fields[propertyName];
			if (typ != 'h'){
				tr.append('td')
				  .attr('id',rowId+"_"+propertyName);
			}			
		}
		var btn_td = tr.append('td');
		  btn_td.attr('id',rowId+'_buttons')
		    .append('a')
		    .attr('id',rowId+"_save")
		    .attr('class','btn btn-primary save_row')
		    .on('click',function (){
		    	  saveRow(rowId,options,fields,data);
		    })
		    .text('Save');
		if (addDel == true){
			btn_td.append('a')
			      .attr('id',rowId+"_del")
			      .attr('class','btn btn-primary del_row')
			      .on('click',function(){
			    	  $('#delete_modal').modal('show');
			    	  $('#modal_del_btn').on('click', function(){
			    		  delRow(rowId,options,fields, data);
			    		  get_availability_default(data['plantgrow']);
			    	  })})
			      .text('Delete');    
		}
		//<a id='{{ crw.id }}_save' class="btn btn-primary save_row" onclick="saveRowCust('{{ crw.id }}')">Save</a	
		editRow(rowId,options,fields);		
	}
	
	function addRowDT(model_name, options, fields, data, order, addDel){
		var tableId = model_name+"-table";
		addRowDT2(model_name, options, fields, data, order, addDel, tableId);
	}
	
	function addRowDT2(model_name, options, fields, data, order, addDel, tableId){	
		var rowId = tableId+"-newrow"+Math.round(Math.random() * 1000);
		data['id'] = rowId;
		data['model_name'] = model_name;
		data['service_name'] = 'add';
		var t = $("#"+tableId).DataTable();
		var cArray = [];
		for (i=0;i<order.length;i++){
			var prop = order[i];
			var typ = fields[prop];
			if (typ == 'o'){
				cArray.push("");
			}else{
				if (typ != 'h'){
				   cArray.push(0);
				}
			}
		}
		// add button cell
		cArray.push("");
		var r = t.row.add(cArray).draw(false).node();
		$(r).attr('id',rowId);
		var tdArray = $(r).children();
		for (i=0;i<(order.length + 1);i++){
			var cellId = rowId + "_buttons";
			if (i < order.length){
				cellId = rowId + "_" + order[i];
			}
			$(tdArray[i]).attr('id',cellId);
		}
		var cellId = rowId + "_buttons";
		var btn_td = d3.select('[id="'+cellId+'"]');
		btn_td.attr('id',rowId+'_buttons')
	          .append('a')
	          .attr('id',rowId+"_save")
	          .attr('class','btn btn-primary save_row')
	          .on('click',function (){
	    	     saveRowDT(rowId,options,fields,data,order,model_name);
	    	     var values = []
	    	     for (var i=0;i<order.length;i++){
	    	    	 values.push($('#'+rowId+'_'+order[i]).text());
	    	     }
	    	     values.push($('#'+rowId+'_buttons').text()); // for the buttons
	    	     t.row($('#'+rowId)).data(values).draw(false);
	            })
	          .text('Save');
	    if (addDel == true){
		   btn_td.append('a')
		         .attr('id',rowId+"_del")
		         .attr('class','btn btn-primary del_row')
		         .on('click',function(){
		    	      $('#delete_modal').modal('show');
		    	      $('#modal_del_btn').on('click', function(){
		    	    	  data['model_name'] = model_name;
		    		      delRowDT(rowId,options,fields, data);
		    		      get_availability_default(data['plantgrow']);
		    	      })
		    	   })
		      .text('Delete');    
	     }
	    editRow(rowId,options,fields);	
	}
	
	function convert_save(old_id, new_id,model_name){

		 d3.select('[id="'+old_id+'"]')
		  .attr('id',new_id)
		  .selectAll('td')
		  .each(function(){
		      var oId = d3.select(this).attr('id');
		      var end = oId.split("_")[1]
		      d3.select(this).attr('id',oId.replace(old_id,new_id));
		      if (end == 'buttons'){
		    	  add_buttons(new_id,model_name,d3.select(this));

		      }
		  });
		}
	
	function get_option_data(model_name, field_name, option_name, callback_func){
		$.ajax({
			url:"/options/"+option_name,
			dataType: "json",
			success: function(data){
				console.log(data);
				callback_func(model_name, field_name, data);
			},
			error: function(data){
				console.log("ERROR!!!!");
				console.log(data);
			}
		});
	}
	
		function add_buttons(rowId, model_name, td_node){
			     var msg = td_node.text().trim();
			     td_node.text("");
		         td_node.insert('a',":first-child")
		           .attr('id',rowId+"_edit")
		           .attr('class','btn btn-primary edit_row')
		           .on('click',function(){
		               edit_row(rowId,model_name);
		           })
		           .text('Edit');
		         td_node.append('a')
		           .attr('id',rowId+"_save")
		           .attr('class','btn btn-primary save_row')
		           .on('click',function(){
		               save_row(rowId,model_name);
		           })
		           .text('Save');
		         if (msg.endsWith('Delete')){
		        	 td_node.append('a')
			           .attr('id',rowId+"_del")
			           .attr('class','btn btn-primary del_row')
			           .on('click',function(){
			               del_row(rowId,model_name);
			           })
			           .text('Delete');
		         }
		         
		         $('#'+rowId+'_save').hide();
		         $('#'+rowId+'_edit').show();
		}

