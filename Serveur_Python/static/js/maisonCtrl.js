$(document).ready(function() { 
	liTemplate = loadTemplate('#li-template'); 
})

var piece_id;

function show(obj) {
	var $actionneurs = $("#formu");
	piece_id = rects.indexOf(obj);
	piece_id ++;
	$actionneurs.html("");
	$.getJSON('/controle/' + piece_id, {}, function(data) {
		$actionneurs.append(liTemplate(data));
	});
}

function valider(elt) {
	console.log(elt);
	var actionneur_id = elt.value;
	var action = $(elt).text();
	console.log(action);
	var bool = false;
	console.log(piece_id);
	if (action == "Activer") {
		console.log(action);
		bool = true;
	}
	$.getJSON('/controle/action', {piece : piece_id, type : bool, action : actionneur_id});
}
