$(document).ready(function() { 
	modifTempTemplate = loadTemplate('#modifTemp-template'); 
	modifBougeTemplate = loadTemplate('#modifBouge-template'); 
	modifHumTemplate = loadTemplate('#modifHum-template'); 
	modifChangeTemplate = loadTemplate('#modifChange-template');
	misePage();
 })

	


function ajoutReg(id_regle){
	
	
	$.getJSON('modifierRegle/' + id_regle, {}, function(data){
		//console.log(data);
		regle_id=id_regle;
		conditions = data;
		console.log(conditions);
		//window.location.href="/modifierRegle";
	});

}

function misePage(){
	var $modification = $("#modif");
	var i=0;
	for(i=0; i<conditions.result.length; i++){
		if(conditions.result[i].nom=="tempSup" || conditions.result[i].nom=="tempInf"){
			$modification.append(modifTempTemplate(conditions.result[i]));
		}
		else{
			if(conditions.result[i].nom=="humInf" || conditions.result[i].nom=="humSup"){
				$modification.append(modifHumTemplate(conditions.result[i]));
			}
			else{
				if(conditions.result[i].nom=="pasBouge"){
					$modification.append(modifBougeTemplate(conditions.result[i]));
				}
				else{
					$modification.append(modifChangeTemplate(conditions.result[i]));
				}

			}
		}
	}
}

