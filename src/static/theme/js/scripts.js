
// You can take this refresh out as most people don't resize their page, this is for the demo
/*================================================================*/
/*	REFRESH IF WINDOW IS UNDER OR OVER 747 PX WIDE (removed 20px for scroll bar, that's why)
/*================================================================*/
var ww = $(window).width();
var limit = 747; 

function refresh() {
   ww = $(window).width();
   var w =  ww<limit ? (location.reload(true)) :  ( ww>limit ? (location.reload(true)) : ww=limit );
}

var tOut;
$(window).resize(function() {
    var resW = $(window).width();
    clearTimeout(tOut);
    if ( (ww>limit && resW<limit) || (ww<limit && resW>limit) ) {        
        tOut = setTimeout(refresh, 100);
    }
}); 

/*================================================================*/
/*	TRIGGER EQUAL COLUMNS AT 767 px 
/*================================================================*/
$(window).load(function(){
if (document.documentElement.clientWidth > 767) { //if client width is greater than 767px load equal columns

(function($) {

    $.fn.eqHeights = function() {

        var el = $(this);
        if (el.length > 0 && !el.data('eqHeights')) {
            $(window).bind('resize.eqHeights', function() {
                el.eqHeights();
            });
            el.data('eqHeights', true);
        }
        return el.each(function() {
            var curHighest = 0;
            $(this).children().each(function() {
                var el = $(this),
                    elHeight = el.height('auto').height();
                if (elHeight > curHighest) {
                    curHighest = elHeight;
                }
            }).height(curHighest);
        });
    };

    $('#equalHeights,#equalHeightsA,#equalHeightsB,#equalHeightsC,#equalHeightsD').eqHeights(); /*one time per page unless you make another id to add here */

}(jQuery));
} // end if
}); // end windowload


/*================================================================*/
/*	FADE ALL EXCEPT HOVERED
/*================================================================*/
$(document).ready(function() {
$('.image-widget li').hover(function(){
	$(this).siblings().addClass('fade');
	}, function(){
	$(this).siblings().removeClass('fade');
	});
});


/*================================================================*/
/*	DESKTOP MENU
/*================================================================*/
if (document.documentElement.clientWidth > 767) { //if client width is greater than 767px

ddsmoothmenu.init({
	mainmenuid: "main_menu", 
	orientation: 'h',
	contentsource: "markup",
	showhidedelay: {showdelay: 300, hidedelay: 100} //set delay in milliseconds before sub menus appear and disappear, respectively
})

} // end if 


/*================================================================*/
/*	SWITCH TO MULIT-LEVEL ACCORDION when mobile
/*================================================================*/
if (document.documentElement.clientWidth < 767) { //if client width is less than 767px

$(document).ready(function() {

// accordion
$('.accordmobile').dcAccordion({
		eventType: 'click',
		saveState: false,
		autoClose: true,
		disableLink: true,
		speed: 'fast',
		showCount: false,
		autoExpand: false,
		classExpand	 : 'parent'
});

});	// end document ready
				
} // end if 


/*================================================================*/
/*	MOBILE NAV TRIGGER
/*================================================================*/
$(document).ready(function(){

$('.mobile_nav a').click(function(){
	$('#main_menu').slideToggle(400);
	$(this).toggleClass('active'); return false;
});
	
/*================================================================*/
/*	IPAD MENU ONLY
/*================================================================*/

$(document).ready(function(){

var deviceAgent = navigator.userAgent.toLowerCase();
var agentID = deviceAgent.match(/(iphone|ipod|ipad)/);
if (agentID)   {
	if (document.documentElement.clientWidth > 767) {
		$('#main_menu ul li.parent').click(function(event) {
			$(this).children('.parent').hide();	
			$('ul', this).toggle();
			$(this).toggleClass('foo');
			event.stopPropagation();
	});

	} //end clientWidth	

}// end IS ipad/iphone/ipod

});
	
/*================================================================*/
/*	ADD CLASSES TO VARIOUS THINGS TO FIX IE
/*================================================================*/
$(".sort li:first-child").addClass('first');
$(".sort li:last-child, .footerPosts li:last-child, .footerCredits ul li:last-child").addClass('last');
$(".features li:nth-child(odd)").addClass('odd');
$(".features li:nth-child(even)").addClass('even');

});

/*================================================================*/
/*	BACK TO TOP
/*================================================================*/
$(document).ready(function(){

if ( navigator.userAgent.indexOf('iPad','iPhone','iPod') == -1 )
  {
	// hide .backToTop first
	$(".backToTop").hide();
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.backToTop').fadeIn();
        } else {
            $('.backToTop').fadeOut();
        }        
 });
 
    $('.backToTop').click(function(){
        $("html, body").animate({ scrollTop: 0 }, 800);
        return false;
    });

  } // end if NOT

var deviceAgent = navigator.userAgent.toLowerCase();
var agentID = deviceAgent.match(/(iphone|ipod|ipad)/);
if (agentID)   {

	$('.backToTop').css({"position":"relative","clear":"both","margin":"0 auto","width":"100%","right":"auto","bottom":"auto"});
	$('.backToTop a').css({"width":"100%"});

}// end IS ipad/iphone/ipod

});

/*================================================================*/
/*	SEARCH
/*================================================================*/
if (document.documentElement.clientWidth < 767) { 
$(document).ready(function(){
$('.search input').hide();
$('#search-trigger').click(function(){
    $('.search input').slideToggle('fast').focus(); 
	$('.preheader .user, .preheader .phone').slideToggle('fast'); 
       	$(this).toggleClass('active');
  	  });
});
}

if (document.documentElement.clientWidth > 767) { 
$(document).ready(function(){
$('.search input').hide();
$('#search-trigger').click(function(){
    $('.search input').slideToggle('fast').focus(); 
       	$(this).toggleClass('active');
  	  });
});
}

/*================================================================*/
/*	FORGOT PASSWORD (on login page)
/*================================================================*/

$(document).ready(function(){

$('.forgot-password').hide();
	$('.forgotpw, .forgot-password .closeforgot').click(function(){
		$('.forgot-password').slideToggle('fast').focus(); 
	});  		
});


/*================================================================*/
/*	SIMPLE ACCORDION
/*================================================================*/

$(document).ready(function(){
    
//  var allPanels = $('.s-accordion li.s-wrap div.s-content').hide();
    
//  $('.s-accordion li.s-wrap .trigger a').click(function() {
// 	 $(this).addClass('active')
//    allPanels.slideUp();
//     if($(this).parent().next().is(':hidden'))
//		{
//     $(this).parent().next().slideDown();
//		} 
//	 return false;
//  });

       $('.s-accordion li.s-wrap div.s-content').hide();
       $('.s-accordion li.s-wrap .trigger a').click(function(){
          if ($(this).hasClass('active')) {
               $(this).removeClass('active');
               $(this).parent().next().slideUp();
          } else {
               $('.s-accordion li.s-wrap .trigger a').removeClass('active');
               $(this).addClass('active');
               $('.s-accordion li.s-wrap div.s-content').slideUp();
               $(this).parent().next().slideDown();
          }
          return false;
       });

});




/*================================================================*/
/*	TOOL TIPS and POP OVERS
/*================================================================*/

  $(function(){

    $('.titletip, ul.social li a').tooltip({});
    $(".detailsPop").popover({trigger: 'hover'});
});

/*================================================================*/
/*	SMOOTH SCROLL to ANCHOR (DIV WITH ID)
/*================================================================*/

$(document).ready(function($) {
 
	$(".scrollto, .container.visible-phone.hidden-tablet.hidden-desktop .btn").click(function(event){		
		event.preventDefault();
		$('html,body').animate({scrollTop:$(this.hash).offset().top}, 800);return false;
	});
});


/*================================================================*/
/*	ADD ACTIVE CLASS TO MENU - DEMO only you can remove this if you want, your CMS should be set up so that the active class is added via php
/*================================================================*/
$(document).ready(function(){
   var path = location.pathname.substring(1);
   if ( path )
	//	$('#main_menu li a[href$="' + path + '"]').parents('li').addClass('active');
		$('#main_menu li a[href$="' + path + '"]').parents('li').last().addClass('active');
		$('#main_menu li a[href$="' + path + '"]').parents('li').first().addClass('active');
     	$('#main_menu li a[href$="' + path + '"]').parent('li').addClass('active');
 });
 
 $(document).ready(function(){
   var path = location.pathname.substring(1);
   if ( path )
          $('ul.navigation li a[href$="' + path + '"]').parents('li').addClass('active');
 });
