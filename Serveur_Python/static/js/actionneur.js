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
        if (new String(data.error).valueOf() == new String("false")) {
        	$(".form-horizontal").html(attenteTemplate());
        } else {
			$("#attention").html(notifTemplate("ID incorrect"));
        }
    });
}

function annuler() {
	$.getJSON('/appareillage/annuler', {id : id, type : type, piece : piece});
}

function confirmer() {
	var $form = $(".form-horizontal");
    $.getJSON('/appareillage/confirmer', {id : id, type : type, piece : piece});
	$form.html(notifTemplate("Dispositif ajouté!"));
}

function appareiller() {
	var $form = $(".form-horizontal");
	$form.html(appaTemplate());
	$.getJSON('/appareillage/actionneur', {id : id, type : type, piece : piece});
}