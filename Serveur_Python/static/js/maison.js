$(document).ready(function() { 
	descriptionTemplate = loadTemplate('#description-template'); 
	//design constants
	var WIDTH = $(document).width() * 0.4; 
	var HEIGHT = $(document).height() * 0.7;
	var dec = 5

	//principal corners' definition
	var p1x = WIDTH * 0.2
	var p1y = HEIGHT * 0.45
	var w1 = WIDTH / 3
	var w2 = WIDTH - w1
	var w3 = WIDTH / 4
	var w4 = WIDTH - w1 - w3
	var h2 = HEIGHT * 2 / 5
	var h3 = HEIGHT - h2
	var h4 = HEIGHT * 0.3
	var h5 = HEIGHT - h2 - h4
	var MARGE = 3

	//Draw maison 
	maison = new Raphael(document.getElementById("maison"), WIDTH + MARGE * 2, HEIGHT);

	var rects = new Array();
	var status = new Array();
	var pieces = new Array();

	$.getJSON('/surveillance/pieces', {}, function(data) {
		pieces = data.result;
	});

	updateEtats();
	//rects	statiques
	rects[0] = createRoom(w1 + MARGE, h2 + MARGE, w3, h3 - MARGE);
	rects[1] = createRoom(0, 0, w1, HEIGHT);
	rects[2] = createRoom(w1 + w3 + 2 * MARGE, h2 + MARGE, w4 - MARGE, h4 - MARGE);
	rects[3] = createRoom(w1 + w3 + 2 * MARGE, h2 + h4 + MARGE, w4 - MARGE, h5 - MARGE);
	rects[4] = createRoom(w1 + MARGE, 0, w2, h2);

	setInterval(updateEtats, 1000);


	/********* Définition des fonctions **********/
	function createRoom(x,y,width,height)
	{
	    var rect = maison.rect(x,y,width,height).attr({"fill":"white","stroke":"red"});
	    addHoverListener(rect);
	    return rect;
	}

   
	function addHoverListener(obj) {
	    obj.mouseout(function(event){

			obj.attr({"stroke-width": 1});
		});

		obj.mouseover(function(event){

			obj.attr({"stroke-width": 5});

		});

		obj.click(function(event){

			showEtat(obj);
		});
	}

	function showEtat(obj) {
		var $description = $("#description");
		var piece_id = rects.indexOf(obj);
		piece_id ++;
		$description.html("");
		$.getJSON('/surveillance/etat/' + piece_id, {}, function(data) {
			console.log(data);		
			$description.append(descriptionTemplate(data));
		});
	}

	function updateEtats() {
		for (var i = 0; i < pieces.length ; i++) {
			var piece = i + 1;
			var intrus = updateEtatPiece(piece);
			if (intrus) {
				rects[i].attr({"fill":"red"});
			} else {
				rects[i].attr({"fill":"white"});
			}	
		}
	}

	function updateEtatPiece(piece) {
		$.getJSON('/surveillance/personnages', {piece : piece}, function(data) {
			var intrus = false;
			var persos = new Array();
			persos = data.result;
			for (var j = 0; j < persos.length; j ++) {
				if (new String(persos[j].nom).valueOf() == new String("Intrus")){
					console.log(persos[j].ignore);
					if (new String(persos[j].ignore).valueOf() == new String("false")) {
						intrus = true;
						console.log("intrus dans " + (piece - 1));
						$('#piece').text(pieces[piece - 1].name);
						$('#notification').show();
						//la prochaine fois, on ignore cet intrus
						$.getJSON('/surveillance/' + persos[j].personne_id);
					}
				}
			}		
		})
		return intrus;
	}
})