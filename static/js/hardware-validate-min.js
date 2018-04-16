$(document).ready(function() {

	var invnumb = $('.inventory_number').value;

	$('input.submit').click( function(event) {

		event.preventDefault();

		var not_fullfilled_yet = [];

		$('.check').each(function(index){
			if($(this)[0].value === '') {
				not_fullfilled_yet.push($(this).prev().text());
			}
		});

		if(not_fullfilled_yet.length > 0){
			alert('Bitte noch ' + not_fullfilled_yet.join(', ') + ' ausfüllen.');
			return;
		}

		if(edit && ($('.inventory_number').value === invnumb)) {
			$('form#hardware').submit();
			return;
		}

		$.post('/hardware/invn/',{ 'number': $('.inventory_number').val() }, function(data) {
			if(data == 'true') {
				alert('Inventarnummer schon vorhanden.');
				return;
			}

			$('form#hardware').submit();
		});
	});
});