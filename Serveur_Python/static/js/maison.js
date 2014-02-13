$(document).ready(function() { 

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

	var rooms = new Array();
	var status = new Array();
	updateEtats();
	var objects;

	$.getJSON('/surveillance/pieces', {}, function(data) {
		objects = data.result;
	});
	//rooms	statiques
	rooms[0] = createRoom(w1 + MARGE, h2 + MARGE, w3, h3 - MARGE);
	rooms[1] = createRoom(0, 0, w1, HEIGHT);
	rooms[2] = createRoom(w1 + w3 + 2 * MARGE, h2 + MARGE, w4 - MARGE, h4 - MARGE);
	rooms[3] = createRoom(w1 + w3 + 2 * MARGE, h2 + h4 + MARGE, w4 - MARGE, h5 - MARGE);
	rooms[4] = createRoom(w1 + MARGE, 0, w2, h2);

	setInterval(updateEtats, 2000);


	/********* Définition des fonctions **********/
	function createRoom(x,y,width,height)
	{
	    var rect = maison.rect(x,y,width,height).attr({"fill":"white","stroke":"red"});
	    addHoverListener(rect);
	    return rect;
	}

   
	function addHoverListener(obj) {
	    obj.mouseout(function(event){

			obj.attr({"fill":"white","stroke-width": 1});
		});

		obj.mouseover(function(event){

			obj.attr({"stroke-width": 5});

		});

		obj.click(function(event){

			obj.attr({"fill":"red"});
			showEtat(obj);

		});
	}

	function showEtat(obj) {
		var piece_id = rooms.indexOf(obj);
		var etat = status[piece_id];
		var piece = objects[piece_id];
		var canvas = document.getElementById("description");
		var description = "<div class=\"well\" style=\"padding: 8px 0;\"><ul class=\"nav nav-list\"><li class=\"nav-header\"><h2><img style=\"margin-left: 5%; margin-right: 20%;\" src=\"../static/img/hotel.png\"/ width=\"15%\">";
		description += piece.name;
		description += "</h2><li class=\"divider\"></li>";
		description += "<li class=\"text-center\">Température : " + (etat.temperature).toString() + "</li>";
		description += "<li class=\"text-center\">Rideaux : " + (etat.rideauxOuverts).toString() + "</li>";
		description += "<li class=\"text-center\">AntiIncendie : " + (etat.antiIncendieDeclenche).toString() + "</li>";
		description += "<li class=\"text-center\">Climatisation : " + (etat.climActivee).toString() + "</li>";
		description += "<li class=\"text-center\">Volets : " + (etat.voletsOuverts).toString() + "</li>";
		description += "<li class=\"text-center\">Prise : " + (etat.priseDeclenchee).toString() + "</li>";
		description += "<li class=\"text-center\">Portes : " + (etat.portesFermees).toString() + "</li>";
		description += "</ul></div>";
		canvas.innerHTML = description;
	}

	function showPerso(etat) {
		var piece_id = etat.piece_id;
		// à terminer
	}

	function updateEtats() {
		$.getJSON('/surveillance/etats', {}, function(data) {
			status = data.result;
			for (var i = 0; i < status.length ; i++)
			{
				showPerso(status[i]);
			}
		});
	}
})