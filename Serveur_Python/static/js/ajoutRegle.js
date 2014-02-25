$(document).ready(function() { 

	

	ajCNormTemplate = loadTemplate('#ajCNorm-template'); 
	ajCTempTemplate = loadTemplate('#ajCTemp-template'); 
	ajCHumTemplate = loadTemplate('#ajCHum-template'); 
	ajCBougeTemplate = loadTemplate('#ajCBouge-template'); 
	ajCChangeTemplate = loadTemplate('#ajCChange-template'); 

	ajATemplate = loadTemplate('#ajA-template'); 

	var $cond = $("#condition");
	var $act = $("#action")
	var i=0;
	console.log("ok") 
	$cond.html("");
	$act.html("");

	$.getJSON('/ajoutRegle/chargerCond', {}, function(data) {
		for(i=0; i<data.result.length; i++){
			console.log(data.result[i].nom);
			if(data.result[i].nom == "tempSup" || data.result[i].nom == "tempInf"){
				$cond.append(ajCTempTemplate(data.result[i]));
			}
			else{
				if(data.result[i].nom == "humSup" || data.result[i].nom == "humInf"){
					$cond.append(ajCHumTemplate(data.result[i]));
				}
				else{
					if(data.result[i].nom == "pasChange"){
						$cond.append(ajCChangeTemplate(data.result[i]));
					}
					else{
						if(data.result[i].nom == "pasBouge"){
							$cond.append(ajCBougeTemplate(data.result[i]));
						}
						else{
							$cond.append(ajCNormTemplate(data.result[i]));
						}
					}
				}

			}
		}

		
	});

	$.getJSON('/ajoutRegle/chargerAct', {}, function(data) {
		//console.log(data);
		$act.append(ajATemplate(data));
	});
})


	