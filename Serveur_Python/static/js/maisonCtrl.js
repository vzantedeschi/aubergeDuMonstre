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




})