$(document).ready(function() { 

	//design constants
	var WIDTH = $(window).width() / 3; 
	var HEIGHT = $(window).height();
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
	maison = new Raphael(document.getElementById("maison"), WIDTH, HEIGHT);

	//rooms	
	var salon = createRoom(0, 0, w1, HEIGHT)
	var chambre = createRoom(w1 + MARGE, 0, w2, h2)
	var couloir = createRoom(w1 + MARGE, h2 + MARGE, w3, h3 - MARGE)
	var bain = createRoom(w1 + w3 + 2 * MARGE, h2 + MARGE, w4 - MARGE, h4 - MARGE)
	var cuisine = createRoom(w1 + w3 + 2 * MARGE, h2 + h4 + MARGE, w4 - MARGE, h5 - MARGE)

	function createRoom(x,y,width,height)
	{
	    var rect = maison.rect(x,y,width,height).attr({"fill":"white","stroke":"red"});
	    return rect;
	}

	//Timer for variables update
	setInterval(updatePresence, 1000);

	function updatePresence() {
		$.getJSON('/presence', {}, function(data) {
		if(new String(data).valueOf() == new String("true").valueOf()) {
			couloir.attr({"fill":"red"});
			//$("body").html("<div class='alert-danger'>Quelqu'un est dans le couloir</div>");
		}
		else {
			couloir.attr({"fill":"white"});
		}
		});
	}
})