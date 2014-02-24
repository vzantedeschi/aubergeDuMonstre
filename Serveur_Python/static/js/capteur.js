$(document).ready(function() {
	attenteTemplate = loadTemplate('#attente-template');
	notifTemplate = loadTemplate('#notif-template');
})

function valider() {
	var id = $('#captID').val();
	var type = $('#type').val();
	var piece = $('#nom').val();
	$.getJSON('/appareillage/capteur', {id : id, type : type, piece : piece}, function(data) {
        console.log(data);
        var $form = $(".form-horizontal");
        if (new String(data.error).valueOf() == new String("false")) {
        	$form.html(attenteTemplate());
        } else {
			$form.prepend(notifTemplate());
        }
    });
}