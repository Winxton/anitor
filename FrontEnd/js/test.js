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
	
	$(document).ready(function() {
			$('.fancybox').fancybox();
			$('.theworldonlygodknows .fansub').each(function()
			{
				var temp=$(this).html();
				if(temp){
				//Create the label element
				var label = $('<label class="checkbox" for="checkbox1">').text($(this).html());
				//Create the input element
				var input = $('<input type="checkbox" value="" id="checkbox1" data-toggle="checkbox">').attr({});

				//Insert the input into the label
				input.appendTo(label);
				//Insert the label into the DOM - replace body with the required position
				$('.fansub-list').append(label);
				}
			});
		})(jQuery);