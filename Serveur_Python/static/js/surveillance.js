$(document).ready(function() { 
	descriptionTemplate = loadTemplate('#description-template'); 
})

function show(obj) {
	var $description = $("#description");
	var piece_id = rects.indexOf(obj);
	piece_id ++;
	$description.html("");
	$.getJSON('/surveillance/etat/' + piece_id, {}, function(data) {
		console.log(data);		
		$description.append(descriptionTemplate(data));
	});
}