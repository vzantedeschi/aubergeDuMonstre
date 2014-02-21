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

/*function valider() {
	console.log('tout va bien');
	var id = $(this).val();
	var action = $(this).text();
	console.log('tout va bien');
	var bool = false;
	console.log(piece_id);
	if (value == "Activer") {
		console.log(value);
		bool = true;
	}
	$.getJSON('/controle/action', {piece : piece_id, type : bool, action : action});
}*/