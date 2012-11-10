
function gotPosition(location) {
	$('input[name="location-lat"]').val(location['coords']['latitude'])
	$('input[name="location-lon"]').val(location['coords']['longitude'])
}

if(geo_position_js.init()){
	geo_position_js.getCurrentPosition(gotPosition,function(){});
}
