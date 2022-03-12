
$(document).ready(function() {

	$('form').on('submit', function(event) {
		$('#embedurl').addClass('active');
		$('#embedurl').val("fetching...");
		$.ajax({
			data : {
				query : $('#playlisturl').val(),
			},
			type : 'GET',
			url : '/embedlink/'
		})
		.done(function(data) {
			if (!data.error) {
				$('#embedurl').val(data.embed_base_url);
			}
			else {
				$('#embedurl').val(data.error);
			}
		});

		event.preventDefault();

	});

});