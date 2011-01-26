/**
* @author Falchenko Maxim aka be3
* @plugin_page http://tops.net.ua/jquery_addtocopy/
* @desc Adds a link to the copied text
* @version 1.2
* @example
* $("#content").addtocopy();
* @license free
**/
jQuery.fn.addtocopy = function(usercopytxt) {
    var options = {htmlcopytxt: '<br>More: <a href="'+window.location.href+'">'+window.location.href+'</a><br>', minlen: 25, addcopyfirst: false}
    $.extend(options, usercopytxt);
	var copy_sp = document.createElement('span');
	copy_sp.id = 'ctrlcopy';
	copy_sp.innerHTML = options.htmlcopytxt;
	return this.each(function(){
		$(this).mousedown(function(){$('#ctrlcopy').remove();});
		$(this).mouseup(function(){
			if(window.getSelection){	//good times 
				var slcted=window.getSelection();
				var seltxt=slcted.toString();
				if(!seltxt||seltxt.length<options.minlen) return;
				var nslct = slcted.getRangeAt(0);
				seltxt = nslct.cloneRange();
				seltxt.collapse(options.addcopyfirst);
				seltxt.insertNode(copy_sp);
				if (!options.addcopyfirst) nslct.setEndAfter(copy_sp);
				slcted.removeAllRanges();
				slcted.addRange(nslct);
			} else if(document.selection){	//bad times
				var slcted = document.selection;
				var nslct=slcted.createRange();
				var seltxt=nslct.text;
				if (!seltxt||seltxt.length<options.minlen) return;
				seltxt=nslct.duplicate();
				seltxt.collapse(options.addcopyfirst);
				seltxt.pasteHTML(copy_sp.outerHTML);
				if (!options.addcopyfirst) {nslct.setEndPoint("EndToEnd",seltxt); nslct.select();}
			}
		});
  });
}