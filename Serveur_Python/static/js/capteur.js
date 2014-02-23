$(document).ready(function() {

	console.log("ready");
	$('.checkbox').on('change', function() {
	    $('.checkbox').not(this).prop('checked', false);  
	});
})

function valider() {
	var id = $('#captID').val();
	console.log(id);
}