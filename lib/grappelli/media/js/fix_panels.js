(function($) {
    function setCookie(name, value, expires, path, domain, secure) {
      document.cookie = name + "=" + escape(value) +
        ((expires) ? "; expires=" + expires : "") +
        ((path) ? "; path=" + path : "") +
        ((domain) ? "; domain=" + domain : "") +
        ((secure) ? "; secure" : "");
    };
    
    function getCookie(name) {
        var cookie = " " + document.cookie;
        var search = " " + name + "=";
        var setStr = null;
        var offset = 0;
        var end = 0;
        if (cookie.length > 0) {
            offset = cookie.indexOf(search);
            if (offset != -1) {
                offset += search.length;
                end = cookie.indexOf(";", offset)
                if (end == -1) {
                    end = cookie.length;
                }
                setStr = unescape(cookie.substring(offset, end));
            }
        }
        return(setStr);
    };    
    
    var $button = $('<button style="float: right; margin-right: 30px; font-size: 0.8em; height: 14px; padding: 1px;">hide</button>');
    var COOKIE_NAME = 'grappelli-panels-hide';
    
    function hide(){
        $('div.module.footer, #header').hide();
        $('#breadcrumbs').addClass('up');
        $button.html('show');
        setCookie(COOKIE_NAME, true, '', '/');
    };
    
    function show(){
        $('div.module.footer, #header').show();
        $('#breadcrumbs').removeClass('up');
        $button.html('hide');
        setCookie(COOKIE_NAME, '');
    };

    function add_button(){
         $('#breadcrumbs').append($button);
         
         $button.click(function(){
             if ($('#breadcrumbs').hasClass('up')){
                 show();
             }else{
                 hide();
             };
         });
         
         if (getCookie(COOKIE_NAME)){
             hide();
         }
    };
    
    $(document).ready(function() {
        add_button();
    });
})(django.jQuery);
