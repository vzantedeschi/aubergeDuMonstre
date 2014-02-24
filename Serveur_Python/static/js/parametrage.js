var nb=1;
$(document).ready(function() { 
	regTemplate = loadTemplate('#reg-template'); //loadtemplate indéfini

	var $regles = $("#listeRegles");
	var i=0;
	console.log("ok") 
	$regles.html("");
	$.getJSON('/parametrage/chargerRegles', {}, function(data) {
		for(i=0; i<data.result.length; i++){
			var id_regle = data.result[i].regle_id;
			//$("#reg_id").value=id_regle;

			$.getJSON('parametrage/ActCond/' + id_regle, {}, function(donnee) {
				console.log(donnee);
				$regles.append(regTemplate(donnee));
				//document.getElementById("reg_id").value=id_regle;
			});
		}
	});
})

