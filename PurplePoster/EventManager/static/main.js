
function gotPosition(location) {
	$('input[name="location-lat"]').val(location['coords']['latitude']);
	$('input[name="location-lon"]').val(location['coords']['longitude']);
	
	location_field = $('input[name="filming-location"]');
	location_field.attr('placeholder', "Current Location");
	location_field.addClass('current-location-placeholder')
}

if(geo_position_js.init()){
	geo_position_js.getCurrentPosition(gotPosition,function(){});
}
