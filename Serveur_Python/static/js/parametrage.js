$(document).ready(function() { 
	regTemplate = loadTemplate('#reg-template'); 

	var $regles = $("#listeRegles");
	console.log("ok")
	$regles.html("");
	$.getJSON('/parametrage/chargerRegles', {}, function(data) {
		//console.log(data);
		$regles.append(regTemplate(data));
	}
})


