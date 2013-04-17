$(document).ready(function() {

/*================================================================*/
/*	FANCY BOX WITH BUTON HELPERS AND THUMBNAILS USED IN GALLERY or PORTFOLIO PAGE
// More options are confusing but more options are necessary

/*================================================================*/
	$(".fancyme").fancybox({
		prevEffect		: 'elastic',
		nextEffect		: 'elastic',
		padding		: 0,
		closeBtn		: true,
		helpers		: { 
		
			title	: { type : 'inside' },
			buttons	: {},
			thumbs	: {
				width	: 75,
				height	: 50
			}
		}
});	// fancybox		


/*================================================================*/
/*	SINGLE IMAGE
/*================================================================*/
	$(".fancysingle").fancybox({
		prevEffect		: 'elastic',
		nextEffect		: 'elastic',
		padding		: 0,
		closeBtn		: true,
		helpers		: { 
			title	: { type : 'inside' }
		}
});	// fancybox		


/*================================================================*/
/*	FANCY BOX WITH BUTON HELPER ONLY for back and next but no thumbs
/*================================================================*/

	$(".fancybutton").fancybox({
		prevEffect		: 'elastic',
		padding		: 0,
		nextEffect		: 'elastic',
		closeBtn		: true,
		helpers		: { 
			title	: { type : 'inside' },
			buttons	: {}
		}
});// fancybox
			
/*================================================================*/
/*	FANCY BOX MEDIA FOR VIDEOS
/*================================================================*/
	$('.fancybox-media').fancybox({
  beforeLoad: function(){
   this.title = $(this.element).next('.entry-summary').html();
  },
  		prevEffect		: 'none',
		padding		: 0,
		nextEffect		: 'none',
		helpers		: { 
			media	: { },
			title	: { type : 'inside' }
		}
 }); // fancybox

/*================================================================*/
/*	FANCY BOX FOR OTHER STUFF (google maps, ajax)
/*================================================================*/
	$(".various").fancybox({
		maxWidth	: 1000,
		maxHeight	: 600,
		fitToView	: false,
		width		: '100%',
		height		: '100%',
		autoSize	: false,
		prevEffect 	: 'elastic',
		nextEffect : 'elastic',
		closeClick	: true,
		padding		: 0,
		openEffect	: 'fade',
		closeEffect	: 'fade',
				helpers: {
			title : {
				type : 'inside'
					}
				}

	}); // fancybox
			
/*================================================================*/
/*	FANCY BOX WITH SUMMARY TITLE (portfolio lightbox)
/*================================================================*/

$(".fancytitle").fancybox({
  beforeLoad: function(){
   this.title = $(this.element).next('.entry-summary').html();
  },
  		prevEffect		: 'elastic',
		padding		: 0,
		nextEffect		: 'elastic',
		helpers		: { 
		
			title	: { type : 'inside' },
			buttons	: {}//
			//thumbs	: {width	: 75,height	: 50} // removed thumbs as they were covering up the permalink in the summary on laptops and short screens 
		}
 }); // fancybox
 
 
 
 
 

 }); //document ready