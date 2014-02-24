$(document).ready(function() { 
	regTemplate = loadTemplate('#reg-template'); 

	var $regles = $("#listeRegles");
	console.log("ok") //s'affiche pas
	$regles.html("");
	$.getJSON('/parametrage/chargerRegles', {}, function(data) {
		console.log(data);
		$regles.append(regTemplate(data));
	});
})


