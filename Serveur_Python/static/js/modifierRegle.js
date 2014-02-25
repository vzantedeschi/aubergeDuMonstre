
$(document).ready(function() { 
	modifTempTemplate = loadTemplate('#modifTemp-template'); 
	modifBougeTemplate = loadTemplate('#modifBouge-template'); 
	modifHumTemplate = loadTemplate('#modifHum-template'); 
	modifChangeTemplate = loadTemplate('#modifChange-template'); 

	var $modification = $("#modif");
	var i=0;
	for(i=0; i<conditions.length; i++){
		if(conditions[i].nom="tempSup" || conditions[i].nom="tempInf"){
			$modif.append(modifTempTemplate(conditions[i]));
		}
		else{
			if(conditions[i].nom="humInf" || conditions[i].nom="humSup"){
				$modif.append(modifHumTemplate(conditons[i]));
			}
			else{
				if(conditions[i].nom="pasBouge"){
					$modif.append(modifBougeTemplate(conditions[i]));
				}
				else{
					$modif.append(modifChangeTemplate(conditons[i]));
				}

			}
		}
	}
})

