$(function(){
	$('form#form-msg').submit(function(){
		var jqxhr = $.get( "http://echo.jsontest.com/key/value/one/two", function() {
		  alert( "success" );
		})
		  .done(function() {
			alert( "second success" );
		  })
		  .fail(function() {
			alert( "error" );
		  })
		  .always(function() {
			
		  });
	});
});