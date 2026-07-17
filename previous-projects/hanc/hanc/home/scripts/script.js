$(document).ready(function(e) {
    var s = skrollr.init();
	$("#circle_big").animate({
				width:"0px",
				height:"0px",
				top:"0px",
				left:"100px",
				opacity:0
			},0);
	$("#circle").drags();
	$("#circle").click(function(e) {
        $("#circle #notice").remove();
    });
	$("#circle").mouseenter(function(e) {
        $(this).fadeTo("fast",1);
    });
	$("#circle").mouseleave(function(e) {
        $(this).fadeTo(1000,0.6);
    });
	var menuOpen=false;
	$("#circle_small").dblclick(function(e) {
		menuOpen=true;
        $("#circle_big").animate({
				width:"200px",
				height:"200px",
				top:"0px",
				left:"0px",
				opacity:1
			});
    });
	
	$(document).scroll(function(e) {
		console.log(menuOpen);
		if(menuOpen){
			menuOpen=false;
        $("#circle_big").animate({
				width:"0px",
				height:"0px",
				top:"0px",
				left:"100px",
				opacity:0
			},1000)};
    });
	
	$(document).scroll(function(e) {
		$s = $(document).scrollTop();
		if($s>=1220)
			$("#panel").css('color','black');
		else
			$("#panel").css('color','white');
    });
	$(document).scroll(function(e){
		$s = $(document).scrollTop();
		if($s>=0 && $s<=1320)
			$(".home").css('border-bottom','1px solid white');
		else if($s>=1320 && $s<3240)
		{
			if($s>=2280)
				$(".logo").css('visibility','visible');
			else
				$(".logo").css('visibility','hidden');
			$(".item").css('border-bottom','none');
			$(".eve span").css('border-bottom','1px solid black');
		}
		else if($s>=3240 && $s<4190)
		{
			$time = 500;
			$delay = 100;
			$('#hu').animate({
				marginRight:"0px",
				opacity:1},500);
			$('#ag').delay($delay).animate({
				marginRight:"0px",
				opacity:1},$time);
			$('#neg').delay($delay*2).animate({
				marginRight:"0px",
				opacity:1},$time);
			$('#con').delay($delay*3).animate({
				marginRight:"0px",
				opacity:1},$time);
			$(".item, span").css('border-bottom','none');
			$(".faq").css('border-bottom','1px solid black');
		}
		else if($s>=5160 && $s<6120)
		{
			$(".item, span").css('border-bottom','none');
			$(".con").css('border-bottom','1px solid black');
		}
		else if($s>4190 && $s<5160)
		{
			$(".item, span").css('border-bottom','none');
			$(".spons").css('border-bottom','1px solid black');
		}
	});
	
	var items = document.querySelectorAll('#circle a');
	console.log(items);
	for(var i = 0, l = items.length; i < l; i++) 
	{
	  items[i].style.left = (44 - 49*Math.cos(-0.5 * Math.PI - 2*(1/l)*i*Math.PI)).toFixed(4) + "%";
	  items[i].style.top = (45 + 49*Math.sin(-0.5 * Math.PI - 2*(1/l)*i*Math.PI)).toFixed(4) + "%";
	}
var animateScrollTo = function(duration,pos) 
	{
            $('html, body').animate({ scrollTop: pos }, duration);
	}
	$('.home').click(function(e) {
		animateScrollTo(1500,0);
    });
	$('.bits').click(function(e) {
		animateScrollTo(1000,1620);
    });
	$('.han').click(function(e) {
		animateScrollTo(1000,2280);
    });
	$('.faq').click(function(e) {
		animateScrollTo(1000,3240);
    });
	$('.con').click(function(e) {
		animateScrollTo(1000,5160);
    });
	$('.spons').click(function(e) {
		animateScrollTo(1000,4200);
    });
		
	$(".eve").mouseenter(function(e) {
        $(".drop").css('border-top-width','3px').animate({
				height:"65px",
				paddingTop:"10px",
				paddingBottom:"10px",
			},500);
    });
	$(".drop,#panel").mouseleave(function(e) {
        $(".drop").animate({
				height:"0px",
				paddingTop:"0px",
				paddingBottom:"0px",
				borderTopWidth:"0px",
			},500);
    });
	
	$('#carousel').flexslider({
    animation: "slide",
    controlNav: false,
    animationLoop: false,
    slideshow: false,
    itemWidth: 210,
    itemMargin: 5,
    asNavFor: '#slider'
  });
 
  $('#slider').flexslider({
    animation: "slide",
    controlNav: false,
    animationLoop: false,
    slideshow: false,
    sync: "#carousel"
  });
});

(function($) {
	//http://css-tricks.com/snippets/jquery/draggable-without-jquery-ui/
    $.fn.drags = function(opt) {

        opt = $.extend({handle:""}, opt);

        if(opt.handle === "") {
            var $el = this;
        } else {
            var $el = this.find(opt.handle);
        }

        return $el.css('cursor', opt.cursor).on("mousedown", function(e) {
            if(opt.handle === "") {
                var $drag = $(this).addClass('draggable');
            } else {
                var $drag = $(this).addClass('active-handle').parent().addClass('draggable');
            }
            var z_idx = $drag.css('z-index'),
                drg_h = $drag.outerHeight(),
                drg_w = $drag.outerWidth(),
                pos_y = $drag.offset().top + drg_h - e.pageY,
                pos_x = $drag.offset().left + drg_w - e.pageX;
            $drag.css('z-index', 1000).parents().on("mousemove", function(e) {
                $('.draggable').offset({
                    top:e.pageY + pos_y - drg_h,
                    left:e.pageX + pos_x - drg_w
                }).on("mouseup", function() {
                    $(this).removeClass('draggable').css('z-index', z_idx);
                });
            });
            e.preventDefault(); // disable selection
        }).on("mouseup", function() {
            if(opt.handle === "") {
                $(this).removeClass('draggable');
            } else {
                $(this).removeClass('active-handle').parent().removeClass('draggable');
            }
        });

    }
})(jQuery);