updatePresence = function() {
	$.getJSON('/presence', {}, function(data) {
		$('#valeur-presence').text(data);
	});
}

$(document).ready(function() {

	//Timer for variables update
	setInterval(updatePresence, 1000); 

	//design constants
	var WIDTH = $(window).width() * 0.9; 
	var HEIGHT = $(window).height() * 0.6;
	var diffH = $(window).height() - HEIGHT;
	var diffW = $(window).width() - WIDTH;
	//Draw maison 
	paper = new Raphael(diffW,diffH,WIDTH,HEIGHT);

	//rooms
	createRect(0,0,WIDTH,HEIGHT);
	createRect(100,100,100,50);
	createRect(100,100,100,50);
	createRect(100,100,100,50);
	createRect(100,100,100,50);

	function createRect(x,y,width,height)
	{
	    var rect = paper.rect(x,y,width,height).attr({"fill":"white","stroke":"red"});

	    //Adds a listener to the rect
	    addHoverListener(rect);
	   
	}

	function addHoverListener(obj)
	{
	    obj.mouseover(function(event){
	                    obj.attr({"fill":"red"});
	    });
	   
	    obj.mouseout(function(event){
	       obj.attr({"fill":"white"});
	     });
	}

})