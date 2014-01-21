/**
 * jQuery Unveil
 * A very lightweight jQuery plugin to lazy load images
 * http://luis-almeida.github.com/unveil
 *
 * Licensed under the MIT license.
 * Copyright 2013 LuÃ­s Almeida
 * https://github.com/luis-almeida
 */

;(function($) {

    $.fn.unveil = function(threshold, callback) {

	var $w = $(window),
        th = threshold || 0,
        retina = window.devicePixelRatio > 1,
        attrib = retina? "data-src-retina" : "data-src",
        images = this,
        loaded;

	this.one("unveil", function() {
	    var source = this.getAttribute(attrib);
	    source = source || this.getAttribute("data-src");
	    if (source) {
		this.setAttribute("src", source);
		if (typeof callback === "function") callback.call(this);
	    }
	});

	function unveil() {
	    var inview = images.filter(function() {
		var $e = $(this);
		if ($e.is(":hidden")) return;

		var wt = $w.scrollTop(),
		wb = wt + $w.height(),
		et = $e.offset().top,
		eb = et + $e.height();

		return eb >= wt - th && et <= wb + th;
	    });

	    loaded = inview.trigger("unveil");
	    images = images.not(loaded);
	}

	$w.scroll(unveil);
	$w.resize(unveil);

	unveil();

	return this;

    };

})(window.jQuery || window.Zepto);

// end unveil

function bindScrollBar() {
    $(".table-data").mCustomScrollbar({
        scrollButtons:{
            enable:true
        },
        theme:"dark-thick",
    });
}

(function($){
    $(window).load(function(){
        bindScrollBar(); //bind scrollbars
        $(".image img").unveil();
    });
})(jQuery);

function populate(epno,anid){
            var html="";
            
            var loaderImg = "<img src='/static/nyaacrawler/images/loader.gif'>";
            ($("#"+anid).find('.anime-data')).html("Loading ... ");

                    $.get(
                    "/search/get-torrent-list/", 
                    {id:anid,episode:epno},
                        function(response) {
                        for (var i = 0 ; i<response.length; i++) {
                        html += '<tr>'+
                            '<td class="fansub">';
                            if(response[i-1]){
                            if(response[i-1]['fansub']!=response[i]['fansub'])
                            html+=response[i]['fansub'];
                            }
                            else{
                                html+=response[i]['fansub'];
                            }
                            html+='</td>'+
                            '<td class="quality">';
                            html+=response[i]['quality'];
                            html+='</td>'+
                            '<td class="file-size">';
                            html+=response[i]['file_size'];
                            html+='</td>'+
                            '<td class="seed">';
                            html+=response[i]['seeders'];
                            html+='</td>'+
                            '<td class="leach">';
                            html+=response[i]['leechers'];
                            html+='</td>'+
                            '<td class="magnet"><a href="'+ response[i]['magnet_link']+'" class="btn btn-block magtor">';
                            html+='Magnet</a></td>'+
                            '<td class="torrent"><a href="'+ response[i]['torrent_link']+'" class="btn btn-block magtor" target="_blank">';
                            html+="Torrent</a></td>"+
                            "</tr>";
                            } 

                            $("#"+anid).find('.anime-data').remove();
                            $("#"+anid).find('.mCSB_container').append( $('<table class="anime-data"></table>') );
                            $(html).appendTo($("#"+anid).find('.anime-data'));
                            
                            },
                    "json"
                    );
	}

    function subscribeSuccess(results, textStatus, jqXHR) {
        if (results['success'] == false) {
            $("#alert-error-private").css("display","block");
        }
        else {
            $('<div class="alert alert-success" id="alert-success-private"> <button type="button" class="close"></button> <strong>Congrats!</strong> You have successfully subscribed to this anime.</div>').appendTo('#'+animename);
            $.fancybox.close();
            setTimeout(function() {
            $("#alert-success-private").fadeOut();
            }, 3000);
        }
    }

	$(document).ready(function(){
        
        $("select").selectpicker({style: 'btn-primary', menuStyle: 'dropdown-inverse'});
		$('.fancybox').fancybox();

		var numfansub=0,fansubcnt=0,numquality=0;qualitycnt=0;
		
        $('.subscribe').click(function() {
            $("#alert-error-private").css("display","none");
            $("#alert-message").empty();

			animename = $(this).parents('div').eq(3).attr('id');
			$(".checkbox-all-quality").addClass("checked");
            $(".checkbox-quality").addClass("checked");
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
            numquality=3;
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

        $(".subscribe-final").click(function(){
            var subscription= {};
            var quality =[];
            var fansub =[];
            $(".checkbox-quality").each(function(){
                if($(this).hasClass("checked"))
                    quality.push($(this).attr("id"));
            });
            $(".checkbox-fansub").each(function(){
                if($(this).hasClass("checked"))
                    fansub.push($(this).text());
            });
            subscription.qualities = quality.join(',');
            subscription.fansub_groups = fansub.join(',');
            subscription.email=$("#email-box").val();
            subscription.anime_key=animename;
            var jsonText = JSON.stringify(subscription);

            $.ajax ({
				url: "/subscribe/",
				type: 'POST',
                data: jsonText,
                success: subscribeSuccess,
                dataType: 'json'
            });

        });

        $(".select-block").change(function(){
             var epno = $(this).val();
             var anid = $(this).closest('.sub-wrapper').attr("id");
             populate(epno,anid);
        });

        $(".fui-arrow-right").click(function(){
            var epno = parseInt($(this).closest('.nav-bar').find(".select-block").val(),10);
            var anid = $(this).closest('.sub-wrapper').attr("id");
            var maxep=$(this).closest('.nav-bar').find(".select-block option:last").val();
            if(epno<maxep)
            {
                epno+=1;
                $(this).closest('.nav-bar').find(".select-block").selectpicker('val',epno);
            }
        });

        $(".fui-arrow-left").click(function(){
            var epno = parseInt($(this).closest('.nav-bar').find(".select-block").val(),10);
            var anid = $(this).closest('.sub-wrapper').attr("id");
            if(epno>1)
            {
                epno-=1;
                $(this).closest('.nav-bar').find(".select-block").selectpicker('val',epno);
            }
        });
});

