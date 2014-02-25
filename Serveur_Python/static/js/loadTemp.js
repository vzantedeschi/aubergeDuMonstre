$(document).ready(function() { 
    pieces = new Array();
    //rects statiques
	rects = new Array();
    $.getJSON('/surveillance/pieces', {}, function(data) {
        pieces = data.result;
    });
    setInterval(updateEtats, 1000);

    var $notification = $('#notification.hidden');
    $notification.hide();
})

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

function updateEtats() {
    for (var i = 0; i < pieces.length ; i++) {
        var piece = i + 1;
        updateEtatPiece(piece);
        if (rects[0])  {
            rects[i].attr({"fill":"white"});
            if (pieces[i].name == $("#piece").text()) {
                rects[i].attr({"fill":"red"});
            }
        }
    }
}

function updateEtatPiece(piece) {
    var persos = new Array();
    $.getJSON('/surveillance/personnages', {piece : piece}, function(data) {
        persos = data.result;
        if (rects[0])  {
        	drawPerso(piece,persos);
        }
        for (var j = 0; j < persos.length; j ++) {
            if (new String(persos[j].nom).valueOf() == new String("Intrus")){
                if (new String(persos[j].ignore).valueOf() == new String("false")) {
                    if (new String(data.logged).valueOf() != new String("None")) {
                        $('#piece').text(pieces[piece - 1].name);
                        $('#notification').show();
                        $("#notification").removeClass('hidden');
                        //la prochaine fois, on ignore cet intrus
                        $.getJSON('/surveillance/' + persos[j].personne_id);
                    }
                }
            }
        }   
    });
}