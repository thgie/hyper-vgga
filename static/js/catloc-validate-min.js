s = snack;
$ = function(node) { return snack.wrap(node)[0]; }
$$ = snack.wrap;

s.ready(function() {

	s.listener({
		node: $('input.submit'),
		event: 'click'
	}, function(event) {

		s.preventDefault(event);

		s.request({
			method: 'post',
			url: '/' + is + '/check',
			data: {
				title: $('#item_title').value
			}
		}, function (err, res){
			if(res == 'true') {
				alert('Schon vorhanden.');
				return;
			}

			$('form#item_form').submit();
		});
	});
});