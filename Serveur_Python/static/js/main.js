function alertOui() {	
	alert("A table!");
	$('#notification').hide();
    $.getJSON('/surveillance/reponse', {rep : "oui"});
}

function alertNon() {	
	alert("Rien à faire");
	$('#notification').hide();
    $.getJSON('/surveillance/reponse', {rep : "non"});
}

/* Handlebars */
loadTemplate = function(template_id) {
    var source = $(template_id).html();
    return Handlebars.compile(source);
}

$(document).ready(function() { 
    $('#notification').hide();
})