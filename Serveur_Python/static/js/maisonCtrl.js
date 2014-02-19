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
	maisonCtrl = new Raphael(document.getElementById("maisonCtrl"), WIDTH + MARGE * 2, HEIGHT);

	var rects = new Array();
	var status = new Array();
	var pieces = new Array();
	var persos = new Array();

	
	//rects	statiques
	rects[0] = createRoom(w1 + MARGE, h2 + MARGE, w3, h3 - MARGE);
	rects[1] = createRoom(0, 0, w1, HEIGHT);
	rects[2] = createRoom(w1 + w3 + 2 * MARGE, h2 + MARGE, w4 - MARGE, h4 - MARGE);
	rects[3] = createRoom(w1 + w3 + 2 * MARGE, h2 + h4 + MARGE, w4 - MARGE, h5 - MARGE);
	rects[4] = createRoom(w1 + MARGE, 0, w2, h2);

	/********* Définition des fonctions **********/
	function createRoom(x,y,width,height)
	{
	    var rect = maisonCtrl.rect(x,y,width,height).attr({"fill":"white","stroke":"red"});
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

			showForm(obj);
		});
	}

	function showForm(obj) {
		var piece_id = rects.indexOf(obj);
		var etat = status[piece_id];
		console.log(etat)
		var piece = pieces[piece_id];

		var str0 = "<div class=\"media\">";
		var str1 = "<a class=\"pull-left\" href=\"#\"><img class=\"media-object\" src=\"";
		var str2 = "</a><div class=\"media-body\"><h4 class=\"media-heading\">";
		var str3 = "</h4></div></div>";
		var canvas = document.getElementById("description");

		//nom pièce
		var description = "<div class=\"well\" style=\"padding: 8px 0;\">" + str0 ;
		description += str1 + "/static/img/hotel.png\" width=\"40px\">" + str2 + "Piece : " + piece.name + str3;
/*
		//température et humidité
		description += str0 + str1 + "/static/img/temp.png\" width=\"40px\">" + str2 + "Température : " + etat.temperature + str3;
		description += str0 + str1 + "/static/img/hum.png\" width=\"20px\">" + str2 + "Humidité : " + etat.humidite + str3;
		//Rideaux
		var str;
		if (new String(etat.rideauxOuverts).valueOf() == new String("true")) {
			str = "Ouverts"
		} else {
			str = "Fermés"
		}
		description += str0 + str1 + "/static/img/temp.png\" width=\"40px\">" + str2 + "Rideaux : " + str + str3;
		//Incendie
		if (new String(etat.antiIncendieDeclenche).valueOf() == new String("true")) {
			str = "Déclenchée"
		} else {
			str = "Non déclenchée"
		}
		description += str0 + str1 + "/static/img/fire.png\" width=\"40px\">" + str2 + "Antincendie : " + str + str3;
		//Climatisation
		if (new String(etat.climActivee).valueOf() == new String("true")) {
			str = "Active"
		} else {
			str = "Eteinte"
		}
		description += str0 + str1 + "/static/img/temp.png\" width=\"40px\">" + str2 + "Climatisation : " + str + str3;
		if (new String(etat.voletsOuverts).valueOf() == new String("true")) {
			str = "Ouverts"
		} else {
			str = "Fermés"
		}
		description += str0 + str1 + "/static/img/rideaux.png\" width=\"40px\">" + str2 + "Rideaux : " + str + str3;
		if (new String(etat.priseDeclenchee).valueOf() == new String("true")) {
			str = "Allumée"
		} else {
			str = "Eteinte"
		}
		description += str0 + str1 + "/static/img/temp.png\" width=\"40px\">" + str2 + "Prise Intelligente : " + str + str3;
		if (new String(etat.portesFermees).valueOf() == new String("true")) {
			str = "Fermées"
		} else {
			str = "Ouvertes"
		}
		description += str0 + str1 + "/static/img/door.png\" width=\"40px\">" + str2 + "Portes : " + str + str3 + "</div>";
		*/
		canvas.innerHTML = description;
	}


})