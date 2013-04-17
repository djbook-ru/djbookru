// ********** Isotope/Masonry 4 Columns *******

$(document).ready(function(){

var $container = $('.four_col');
	
$container.imagesLoaded(function() {
$container.isotope({
   itemSelector : 'li',
	animationEngine: 'best-available',
	resizable: true, // disable normal resizing
	resizesContainer: true,
	masonry: { columnWidth: $container.width() / 4 }
  });
});


$(window).smartresize(function(){
  $container.isotope({
	masonry: { columnWidth: $container.width() / 4 }
  });
});

$container.imagesLoaded( function(){
  $(window).smartresize();
});


$('.sort li a').click(function(){
	$('.sort li a').removeClass('active');
	$(this).addClass('active');
	var selector = $(this).attr('data-filter');
	$container.isotope({ filter: selector });
	return false;
});

}); //end 4 column



// ********** Isotope/Masonry 3 Columns *******

$(document).ready(function(){

if (document.documentElement.clientWidth > 767) { //if client width is greater than 767px

var $container = $('.three_col');
	
$container.imagesLoaded(function() {
$container.isotope({
   itemSelector : 'li',
	animationEngine: 'best-available',
	resizable: true, // disable normal resizing
	resizesContainer: true,
	masonry: { columnWidth: $container.width() / 3 }
  });
});


$(window).smartresize(function(){
  $container.isotope({
	masonry: { columnWidth: $container.width() / 3 }
  });
});

$container.imagesLoaded( function(){
  $(window).smartresize();
});


$('.sort li a').click(function(){
	$('.sort li a').removeClass('active');
	$(this).addClass('active');
	var selector = $(this).attr('data-filter');
	$container.isotope({ filter: selector });
	return false;
});

}

}); //three columns


// ********** switch 3 column to 2 columns for mobile (it must be an even number so this turns the small into 2 columns) *******
if (document.documentElement.clientWidth < 767) { //if client width is less than 767px

$(document).ready(function(){


var $container = $('.three_col');
	
$container.imagesLoaded(function() {
$container.isotope({
   itemSelector : 'li',
	animationEngine: 'best-available',
	resizable: true, // disable normal resizing
	resizesContainer: true,
	masonry: { columnWidth: $container.width() / 4 } // this is actually two columns
  });
});


$(window).smartresize(function(){
  $container.isotope({
	masonry: { columnWidth: $container.width() / 4 } // this is actually two columns
  });
});

$container.imagesLoaded( function(){
  $(window).smartresize();
});


$('.sort li a').click(function(){
	$('.sort li a').removeClass('active');
	$(this).addClass('active');
	var selector = $(this).attr('data-filter');
	$container.isotope({ filter: selector });
	return false;
});


}); 

}//end switch 3 to 2

// ********** switch 3 column to 1 columns for mobile (it must be an even number so this turns the small into 2 columns) *******

$(document).ready(function(){

if (document.documentElement.clientWidth < 500) { //if client width is less than 767px

var $container = $('.three_col, .four_col, .two_col');
	
$container.imagesLoaded(function() {
$container.isotope({
   itemSelector : 'li',
	animationEngine: 'best-available',
	resizable: true, // disable normal resizing
	resizesContainer: true,
	masonry: { columnWidth: $container.width() / 1 } // this is actually two columns
  });
});


$(window).smartresize(function(){
  $container.isotope({
	masonry: { columnWidth: $container.width() / 1 } // this is actually two columns
  });
});

$container.imagesLoaded( function(){
  $(window).smartresize();
});


$('.sort li a').click(function(){
	$('.sort li a').removeClass('active');
	$(this).addClass('active');
	var selector = $(this).attr('data-filter');
	$container.isotope({ filter: selector });
	return false;
});

}

}); //end switch 3 to 1



//turn filter into dropdown menu for smaller devices
$(document).ready(function(){

if (document.documentElement.clientWidth < 767) { //if client width is less than 767px show filter drop down

  $('#filter').click(function(){
      $('#option').slideToggle();
      	$('#filter').toggleClass('active'); return false;

   });
  $('#option a').click(function(e){
        $('#filter').text($(this).text());
         $('#option').slideToggle();
  })
    
    
} //end if client width is less than 767

    
}); //end document ready
    
    
    
    
    
    
// ********** Isotope/Masonry 2 Columns *******

$(document).ready(function(){

var $container = $('.two_col');
	
$container.imagesLoaded(function() {
$container.isotope({
   itemSelector : 'li',
	animationEngine: 'best-available',
	resizable: true, // disable normal resizing
	resizesContainer: true,
	masonry: { columnWidth: $container.width() / 2 }
  });
});


$(window).smartresize(function(){
  $container.isotope({
	masonry: { columnWidth: $container.width() / 2 }
  });
});

$container.imagesLoaded( function(){
  $(window).smartresize();
});


$('.sort li a').click(function(){
	$('.sort li a').removeClass('active');
	$(this).addClass('active');
	var selector = $(this).attr('data-filter');
	$container.isotope({ filter: selector });
	return false;
});

}); //two columns



    
