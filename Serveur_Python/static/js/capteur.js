$(document).ready(function() {
	attenteTemplate = loadTemplate('#attente-template');
	notifTemplate = loadTemplate('#notif-template');
	appaTemplate = loadTemplate('#appa-template');
})

var id;
var type;
var piece;

function valider() {
	id = $('#captID').val();
	type = $('#type').val();
	piece = $('#nom').val();
	$.getJSON('/appareillage/verifier', {id : id}, function(data) {
        console.log(data);
        var $form = $(".form-horizontal");
        if (new String(data.error).valueOf() == new String("false")) {
        	$form.html(attenteTemplate());
        } else {
			$form.prepend(notifTemplate("ID incorrect"));
        }
    });
}

function appareiller() {
	var $form = $(".form-horizontal");
	$form.html(appaTemplate());
	$.getJSON('/appareillage/capteur', {id : id, type : type, piece : piece}, function(data) {
		console.log(data);
        var $form = $(".form-horizontal");
        if (new String(data.error).valueOf() == new String("true")) {
        	$form.html(notifTemplate("Impossible d'ajouter le dispositif. Réessayez"));
        } else {
			$form.html(notifTemplate("Dispositif ajouté!"));
        }
	});
	
}