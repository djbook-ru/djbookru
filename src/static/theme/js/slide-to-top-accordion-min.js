	/*
	* smartresize: debounced resize event for jQuery
	*
	* latest version and complete README available on Github:
	* https://github.com/louisremi/jquery.smartresize.js
	*
	* Copyright 2011 @louis_remi
	* Licensed under the MIT license.
	*/

(function(window,$,undefined){var $event=$.event,resizeTimeout;$event.special.smartresize={setup:function(){$(this).bind("resize",$event.special.smartresize.handler)},teardown:function(){$(this).unbind("resize",$event.special.smartresize.handler)},handler:function(event,execAsap){var context=this,args=arguments;event.type="smartresize";if(resizeTimeout){clearTimeout(resizeTimeout)}resizeTimeout=setTimeout(function(){jQuery.event.handle.apply(context,args)},execAsap==="execAsap"?0:100)}};$.fn.smartresize=function(fn){return fn?this.bind("smartresize",fn):this.trigger("smartresize",["execAsap"])};$.Accordion=function(options,element){this.$el=$(element);this.$items=this.$el.children("ul").children("li.st-content-wrapper");this.itemsCount=this.$items.length;this._init(options)};$.Accordion.defaults={open:-1,oneOpenedItem:false,speed:600,easing:"easeInOutExpo",scrollSpeed:900,scrollEasing:"easeInOutExpo"};$.Accordion.prototype={_init:function(options){this.options=$.extend(true,{},$.Accordion.defaults,options);this._validate();this.current=this.options.open;this.$items.find("div.st-content").hide();this._saveDimValues();if(this.current!=-1){this._toggleItem(this.$items.eq(this.current))}this._initEvents()},_saveDimValues:function(){this.$items.each(function(){var $item=$(this);$item.data({originalHeight:$item.find("a:first").height(),offsetTop:$item.offset().top})})},_validate:function(){if(this.options.open<-1||this.options.open>this.itemsCount-1){this.options.open=-1}},_initEvents:function(){var instance=this;this.$items.find("a:first").bind("click.slideaccordion",function(event){var $item=$(this).parent();if(instance.options.oneOpenedItem&&instance._isOpened()&&instance.current!==$item.index()){instance._toggleItem(instance.$items.eq(instance.current))}instance._toggleItem($item);return false});$(window).bind("smartresize.slideaccordion",function(event){instance._saveDimValues();instance.$el.find("li.st-open").each(function(){var $this=$(this);$this.css("height",$this.data("originalHeight")+$this.find("div.st-content").outerHeight(true))});if(instance._isOpened()){instance._scroll()}})},_isOpened:function(){return(this.$el.find("li.st-open").length>0)},_toggleItem:function($item){var $content=$item.find("div.st-content");($item.hasClass("st-open"))?(this.current=-1,$content.stop(true,true).fadeOut(this.options.speed),$item.removeClass("st-open").stop().animate({height:$item.data("originalHeight")},this.options.speed,this.options.easing)):(this.current=$item.index(),$content.stop(true,true).fadeIn(this.options.speed),$item.addClass("st-open").stop().animate({height:$item.data("originalHeight")+$content.outerHeight(true)},this.options.speed,this.options.easing),this._scroll(this))},_scroll:function(instance){var instance=instance||this,current;(instance.current!==-1)?current=instance.current:current=instance.$el.find("li.st-open:last").index();$("html, body").stop().animate({scrollTop:(instance.options.oneOpenedItem)?instance.$items.eq(current).data("offsetTop"):instance.$items.eq(current).offset().top},instance.options.scrollSpeed,instance.options.scrollEasing)}};var logError=function(message){if(this.console){console.error(message)}};$.fn.slideaccordion=function(options){if(typeof options==="string"){var args=Array.prototype.slice.call(arguments,1);this.each(function(){var instance=$.data(this,"slideaccordion");if(!instance){logError("cannot call methods on slideaccordion prior to initialization; attempted to call method '"+options+"'");return}if(!$.isFunction(instance[options])||options.charAt(0)==="_"){logError("no such method '"+options+"' for slideaccordion instance");return}instance[options].apply(instance,args)})}else{this.each(function(){var instance=$.data(this,"slideaccordion");if(!instance){$.data(this,"slideaccordion",new $.Accordion(options,this))}})}return this}})(window,jQuery);

//initialize ALL CLOSED

$(function() {
			
				$(".slide-to-top.all-closed").slideaccordion({
					oneOpenedItem	: true,
					open			: -1 // 0 = first pane is open / -1 all are closed
				});

// Uncomment BELOW if you want all to be open on load
		//	$('.slide-to-top ul li.st-content-wrapper').addClass( 'st-open' );
  		//  $('.slide-to-top ul li.st-content-wrapper.st-open .st-content').show();
  		  		
				
});


//initialize FIRST OPEN

$(function() {
			
				$(".slide-to-top.first-pane-open").slideaccordion({
					oneOpenedItem	: true,
					open			: 0 // 0 = first pane is open / -1 all are closed
				});

				
});



