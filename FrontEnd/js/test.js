
  (function($){
        $(window).load(function(){
            $(".table-data").mCustomScrollbar({
				scrollButtons:{
						enable:true
					},
				autoHideScrollbar:true,
				theme:"dark-thick",
			});
        });
    })(jQuery);
	$(document).ready(function(){
	$('.fancybox').fancybox();
	
	$('.subscribe').click(function() {
		var animename = $(this).parent('div').attr('id');
		$('#fansub-list').empty();
		$("#"+animename+ " .fansub").each(function(){
		if($(this).text()){
		//Create the label element
		var label = $('<label class="checkbox" for="checkbox1">').text($(this).text());
		//Create the input element
		var input = $('<input type="checkbox" id="checkbox1" data-toggle="checkbox"><span class="icons"><span class="first-icon fui-checkbox-unchecked"></span><span class="second-icon fui-checkbox-checked"></span></span>').attr({});
		//Insert the input into the label
		input.appendTo(label);
		//Insert the label into the DOM - replace body with the required position
		$('#fansub-list').append(label);
		}
		});
	});
	});
	
	