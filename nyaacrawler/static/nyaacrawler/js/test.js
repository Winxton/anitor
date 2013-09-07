
function bindScrollBar() {
    $(".table-data").mCustomScrollbar({
    scrollButtons:{
            enable:true
        },
        theme:"dark-thick",
    });
    $(".dropdown-inverse").mCustomScrollbar({
        theme:"light-thick",
    });
}

  (function($){
        $(window).load(function(){
            //bindScrollBar();
        });
    })(jQuery);

	var animename;

	$(document).ready(function(){
        $("select").selectpicker({style: 'btn-primary', menuStyle: 'dropdown-inverse'});
		$('.fancybox').fancybox();
		var numfansub=0,fansubcnt=0,numquality=0;qualitycnt=0;
		$('.subscribe').click(function() {
			animename = $(this).parents('div').eq(3).attr('id');
			$(".checkbox-all-quality").addClass("checked");
			$(".checkbox-all-fansub").addClass("checked");
			$('#fansub-list').empty();
			numfansub=0;
			numquality=0;
			$("#alert-success-private").remove();
			$("#alert-error-private").css("display","none");
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
			qualitycnt=numquality;
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
			var success=true;
			$(".subscribe-final").click(function(){	
				if(success==true){
					$('<div class="alert alert-success" id="alert-success-private"> <button type="button" class="close"></button> <strong>Congrats!</strong> You have successfully subscribed to this anime.</div>').appendTo('#'+animename);
					$.fancybox.close();
					setTimeout(function() {
					$("#alert-success-private").fadeOut();
					}, 2000);
				}
				else
				$("#alert-error-private").css("display","block");
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