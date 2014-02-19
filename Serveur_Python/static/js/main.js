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

Handlebars.registerHelper('breaklines', function(text) {
    text = Handlebars.Utils.escapeExpression(text);
    text = preprocessText(text);
    return new Handlebars.SafeString(text);
});

Handlebars.registerHelper('fixedDecimal', function(number) {
  return number.toFixed(4);
});

$(document).ready(function() { 
    $('#notification').hide();
})