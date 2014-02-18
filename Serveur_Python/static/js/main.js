function alertOui() {	
	alert("A table!");
	$('#notification').hide();
}

function alertNon() {	
	alert("Rien à faire");
	$('#notification').hide();
}

$(document).ready(function() { 
    $('#notification').hide();
})