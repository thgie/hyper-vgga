s = snack;
one = function(node) { return snack.wrap(node)[0]; }
all = snack.wrap;

s.ready(function() {

	var invnumb = one('.inventory_number').value;

	s.listener({
		node: one('input.submit'),
		event: 'click'
	}, function(event) {

		s.preventDefault(event);

		var not_fullfilled_yet = [];

		all('.check').each(function(e){
			
			if(e.value === '') {
				not_fullfilled_yet.push(e)
			}
		});

		if(not_fullfilled_yet.length > 0){
			alert('Bitte noch Daten auswählen.');
			return;
		}

		if(!one('.second_check').value) {
			alert('Begründung fehlt.');
			return;
		}

		one('form#reservation').submit();
	});
});