function alertOui() {	
	alert("A table!");
	$('#notification').hide();
    piece = $("#piece").text();
    $("#piece").text("");
    $.getJSON('/surveillance/reponse', {piece : piece, rep : "oui"});
}

function alertNon() {	
	alert("Rien à faire");
    $('#notification').hide();
	piece = $("#piece").text();
    $("#piece").text("");
    $.getJSON('/surveillance/reponse', {piece : piece, rep : "non"});
}

/* Handlebars */
loadTemplate = function(template_id) {
    var source = $(template_id).html();
    return Handlebars.compile(source);
}

$(document).ready(function() { 
    $('#notification').hide();
})