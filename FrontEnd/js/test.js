
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
	var numfansub=0,fansubcnt=0,numquality=0;qualitycnt=0;
	$('.subscribe').click(function() {
		var animename = $(this).parent('div').attr('id');
		$(".checkbox-all-quality").addClass("checked");
		$(".checkbox-all-fansub").addClass("checked");
		$('#fansub-list').empty();
		numfansub=0;
		numquality=0;
		$("#"+animename+ " .fansub").each(function(){
		if($(this).text()){
			var label = $('<label id="test" class="checkbox checkbox-fansub checked">').text($(this).text());
			var input = $('<input class="checkbox-option-fansub" type="checkbox" data-toggle="checkbox" checked=""><span class="icons"><span class="first-icon fui-checkbox-unchecked"></span><span class="second-icon fui-checkbox-checked"></span></span>').attr({});
			input.appendTo(label);
			$('#fansub-list').append(label);
			numfansub+=1;
		}
		});	
		fansubcnt=numfansub;
		qualitycnt=numquality;
		$('#quality-list').empty();
		$("#"+animename+ " .quality").each(function(){
		if($(this).text()){
			var label = $('<label class="checkbox checked checkbox-quality">').text($(this).text());
			var input = $('<input class="checkbox-option-quality" type="checkbox" data-toggle="checkbox" checked=""><span class="icons"><span class="first-icon fui-checkbox-unchecked"></span><span class="second-icon fui-checkbox-checked"></span></span>').attr({});
			input.appendTo(label);
			$('#quality-list').append(label);
			numquality+=1;
		}
		});
		$(".checkbox-fansub").click(function(){
			if($(this).hasClass("checked"))
			fansubcnt-=1;
			else
			fansubcnt+=1;
			if(fansubcnt==numfansub){
				$(".checkbox-all-fansub").addClass("checked");
			}
			else
			{
				$(".checkbox-option-fansub").removeAttr("checked");
				$(".checkbox-option-all-fansub").removeAttr("checked");
				$(".checkbox-all-fansub").removeClass("checked");
			}
		});
		$(".checkbox-quality").click(function(){
			if($(this).hasClass("checked"))
				qualitycnt-=1;
			else
				qualitycnt+=1;
			if(qualitycnt==numquality){
				$(".checkbox-all-quality").addClass("checked");
			}
			else
			{
				$(".checkbox-option-quality").removeAttr("checked");
				$(".checkbox-option-all-quality").removeAttr("checked");
				$(".checkbox-all-quality").removeClass("checked");
			}
		});
		
	});
	
	$(".checkbox-all-fansub").click(function() {
		if($(".checkbox-all-fansub").hasClass("checked")){	
			$(".checkbox-option-fansub").removeAttr("checked");
			$(".checkbox-option-all-fansub").removeAttr("checked");
			$(".checkbox-fansub").removeClass("checked");
			fansubcnt=0;
		}
		else{
			$(".checkbox-option-fansub").attr("checked","");
			$(".checkbox-option-all-fansub").attr("checked","");
			$(".checkbox-fansub").addClass("checked");
			fansubcnt=numfansub;
		}
	});

	$(".checkbox-all-quality").click(function() {
		if($(".checkbox-all-quality").hasClass("checked")){	
				$(".checkbox-option-quality").removeAttr("checked");
				$(".checkbox-option-all-quality").removeAttr("checked");
				$(".checkbox-quality").removeClass("checked");
				qualitycnt=0;
			}
			else{
				$(".checkbox-option-quality").attr("checked","");
				$(".checkbox-option-all-quality").attr("checked","");
				$(".checkbox-quality").addClass("checked");
				qualitycnt=numquality;
			}
	});
	
	
	
	});
	
	
	
	