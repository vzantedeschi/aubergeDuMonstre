function alertOui() {	
	alert("A table!");
	$('#notification').hide();
}

function alertNon() {	
	alert("Rien à faire");
	$('#notification').hide();
}

/* Handlebars */
loadTemplate = function(template_id) {
    var source = $(template_id).html();
    return Handlebars.compile(source);
}

$(document).ready(function() { 
    $('#notification').hide();
})