$(document).ready(function() { 
    status = new Array();
    pieces = new Array();
    
    $.getJSON('/surveillance/pieces', {}, function(data) {
        pieces = data.result;
    });
    setInterval(updateEtats, 1000);

    var $notification = $('#notification.hidden');
    $notification.hide();
})

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
var rects = new Array();
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

function updateEtats() {
    for (var i = 0; i < pieces.length ; i++) {
        var piece = i + 1;
        updateEtatPiece(piece);
        rects[i].attr({"fill":"white"});
        if (pieces[i].name == $("#piece").text()) {
            rects[i].attr({"fill":"red"});
        }
    }
}

function drawPerso(piece,perso){
    //console.log(rects[piece - 1].attr("width"));
}

function updateEtatPiece(piece) {
    var persos = new Array();
    $.getJSON('/surveillance/personnages', {piece : piece}, function(data) {
        persos = data.result;
        for (var j = 0; j < persos.length; j ++) {
            drawPerso(piece,persos[j]);
            if (new String(persos[j].nom).valueOf() == new String("Intrus")){
                if (new String(persos[j].ignore).valueOf() == new String("false")) {
                    $('#piece').text(pieces[piece - 1].name);
                    $('#notification').show();
                    $("#notification").removeClass('hidden');
                    //la prochaine fois, on ignore cet intrus
                    $.getJSON('/surveillance/' + persos[j].personne_id);
                }
            }
        }   
    });
}
function alertOui() {	
	alert("A table!");
	$('#notification').hide();
    $("#notification").addClass('hidden');
    piece = $("#piece").text();
    $("#piece").text("");
    $.getJSON('/surveillance/reponse', {piece : piece, rep : "oui"});
}

function alertNon() {	
	alert("Rien à faire");
    $('#notification').hide();
    $("#notification").addClass('hidden');
	piece = $("#piece").text();
    $("#piece").text("");
    $.getJSON('/surveillance/reponse', {piece : piece, rep : "non"});
}

/* Handlebars */
loadTemplate = function(template_id) {
    var source = $(template_id).html();
    return Handlebars.compile(source);
}