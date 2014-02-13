$(document).ready(function() { 

	//design constants
	var WIDTH = $(document).width() * 0.4; 
	var HEIGHT = $(document).height() * 0.8;
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

	var rooms=new Array();

	$.getJSON('/surveillance/pieces', {}, function(data) {
		//rien pour le moment. Gérer les pièces dinamiquement?
	});

	//rooms	statiques
	rooms[0] = createRoom(0, 0, w1, HEIGHT)
	rooms[1] = createRoom(w1 + MARGE, 0, w2, h2)
	rooms[2] = createRoom(w1 + MARGE, h2 + MARGE, w3, h3 - MARGE)
	rooms[3] = createRoom(w1 + w3 + 2 * MARGE, h2 + MARGE, w4 - MARGE, h4 - MARGE)
	rooms[4] = createRoom(w1 + w3 + 2 * MARGE, h2 + h4 + MARGE, w4 - MARGE, h5 - MARGE)

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

		});
	}

	function showEtat(obj) {
		//var piece_id = 
	}

	function showPerso() {

	}

	//setInterval(updateEtats, 1000);

	function updateEtats() {
		$.getJSON('/surveillance/etats', {}, function(data) {
			console.log(data.result[0]);
		});
	}
})