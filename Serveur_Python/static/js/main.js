//design constants
var WIDTH = $(document).width() * 0.4; 
var HEIGHT = $(document).height() * 0.7;
var dec = 5;

//principal corners' definition
var p1x = WIDTH * 0.2;
var p1y = HEIGHT * 0.45;
var w1 = WIDTH / 3;
var w2 = WIDTH - w1;
var w3 = WIDTH / 4;
var w4 = WIDTH - w1 - w3;
var h2 = HEIGHT * 2 / 5;
var h3 = HEIGHT - h2;
var h4 = HEIGHT * 0.3;
var h5 = HEIGHT - h2 - h4;
var MARGE = 3;

//Draw maison 
maison = new Raphael(document.getElementById("maison"), WIDTH + MARGE * 2, HEIGHT);
//rects statiques
rects = new Array();
rects[0] = createRoom(w1 + MARGE, h2 + MARGE, w3, h3 - MARGE);
rects[1] = createRoom(0, 0, w1, HEIGHT);
rects[2] = createRoom(w1 + w3 + 2 * MARGE, h2 + MARGE, w4 - MARGE, h4 - MARGE);
rects[3] = createRoom(w1 + w3 + 2 * MARGE, h2 + h4 + MARGE, w4 - MARGE, h5 - MARGE);
rects[4] = createRoom(w1 + MARGE, 0, w2, h2);

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
        show(obj);
    });
}

function drawPerso(piece,persos){
    var w = rects[piece - 1].attr("width") - 25;
    var h = rects[piece - 1].attr("height") - 25;
    var len = persos.length;
    var x = 0;
    var y = 0;
    if (piece == 1) {
        x = w1 + MARGE;
        y = h2 + MARGE;
    }  else if (piece == 3) {
        x = w1 + w3 + 2 * MARGE;
        y = h2 + MARGE;
    } else if (piece == 4) {
        x = w1 + w3 + 2 * MARGE;
        y = h2 + h4 + MARGE;
    } else if (piece == 5) {
        x = w1 + MARGE;
    }
    for (var j = 0; j < len; j ++) {
        maison.image('/static/img/' + persos[j].image, x + w/len * j, y + h/len * j, 50, 50);                
    }
}

function removePerso() {
    rects = new Array();
    rects[0] = createRoom(w1 + MARGE, h2 + MARGE, w3, h3 - MARGE);
    rects[1] = createRoom(0, 0, w1, HEIGHT);
    rects[2] = createRoom(w1 + w3 + 2 * MARGE, h2 + MARGE, w4 - MARGE, h4 - MARGE);
    rects[3] = createRoom(w1 + w3 + 2 * MARGE, h2 + h4 + MARGE, w4 - MARGE, h5 - MARGE);
    rects[4] = createRoom(w1 + MARGE, 0, w2, h2);
}

$(document).ready(function() { 
    setInterval(removePerso, 2000);
})
