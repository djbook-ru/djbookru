var gettext = gettext || function(val){return val;};

$(function() {
    spelling._init();
    $(document).bind('keydown', function(e) {
        if (e.keyCode == 13 && e.ctrlKey) {
            spelling.showForm();
        }
    });
});

var spelling = {
    selection: null,
    $form: $('<div class="modal" id="myModal">'+
                '<div class="modal-header">'+
                    '<button class="close" data-dismiss="modal">×</button>'+
                    '<h3>'+gettext('Send error form')+'</h3>'+
                '</div>'+
                '<div class="modal-body">'+
                    '<h3>'+gettext('Context of error')+'</h3>'+
                    '<p class="context-error"></p>'+
                '</div>'+
                '<form class="form-horizontal">'+
                    '<fieldset>'+
                        '<div class="control-group">'+
                            '<label class="control-label" for="spelling-form-email">E-mail *</label>'+
                            '<div class="controls"><input id="spelling-form-email" type="text" class="span4" placeholder="E-mail"></div>'+
                        '</div>'+
                        '<div class="control-group">'+
                            '<label class="control-label" for="spelling-form-comment">'+gettext('Comment')+' *</label>'+
                            '<div class="controls"><textarea id="spelling-form-comment" class="span4" placeholder="'+gettext('Comment')+'"></textarea></div>'+
                        '</div>'+
                        '<div class="control-group">'+
                            '<div class="controls"><label class="checkbox" for="spelling-form-notify"><input id="spelling-form-notify" type="checkbox">'+gettext('Notify me')+'</label></div>'+
                        '</div>'+
                    '</fieldset>'+
                '</form>'+
                '<div class="modal-footer">'+
                    '<a href="#" class="btn" data-dismiss="modal">'+gettext('Close')+'</a>'+
                    '<a href="#" class="btn btn-primary send">'+gettext('Send')+'</a>'+
                '</div>'+
            '</div>'),

    _init: function(){
        var $form = this.$form;
        $form.modal({show: false});

        $form.on('hide', spelling.reset);

        $('.btn.send', $form).click(function(){
            spelling.resetFormErrors();
            var valid = true;
            var email = $('#spelling-form-email').val();
            var comment = $('#spelling-form-comment').val();

            if (comment === '') {
                valid = false;
                $('#spelling-form-comment').parents('.control-group').addClass('error');
            }

            if (email === '' || (! spelling.isValidEmail(email))) {
                 valid = false;
                $('#spelling-form-email').parents('.control-group').addClass('error');
            }

            if (valid){
                $.post('/claims/', {
                        ctx_left: spelling.selection.context_left,
                        selected: spelling.selection.context_error,
                        ctx_right: spelling.selection.context_right,
                        email: email,
                        notify: $('#spelling-form-notify').prop('checked'),
                        comment: comment
                    },
                    function(xml) {
                        var text = $(xml).find('result').text();
                        if (text == 'ok') {
                            spelling.alert(gettext('Message sent success!'));
                        }
                        else {
                            spelling.alert(gettext('Something broken. Try later.'));
                        }
                    }
                );
                $form.modal('hide');
            }

            return false;
        });
    },

    reset: function(){
        spelling.$form.find('form')[0].reset();
        spelling.resetFormErrors();
        spelling.selection = null;
    },

    resetFormErrors: function(){
        this.$form.find('.control-group').removeClass('error');
    },

    showForm: function(){
        this.selection = this.getErrorSelection();

        if ( ! this.selection)
            return;

        var context_error = '<span>' + this.selection.context_left + '</span>'+
            '<span class="selected">' + this.selection.context_error+
            '</span>' + '<span>' + this.selection.context_right + '</span>';

        $('.context-error', this.$form).html(context_error);

        this.$form.modal('show');
    },

    /**
     * Алерт на замену стандартному
     * @param message
     * @param title
     */
    alert: function(message) {
        alert(message);
    },

    /**
     * Возвращает массив с текстом ошибки и обрамляющим ее текстом справа и слева
     * В случае выделения больше 255 символов возвращает false
     *
     * @return array | false
     */
    getErrorSelection: function() {
        var userSelection;
        if (window.getSelection) { // ie, mozilla, object
            userSelection = window.getSelection();
        } else if (document.getSelection) { // konqueror, string
            userSelection = document.getSelection();
        } else if (document.selection) { // opera, object
            userSelection = document.selection.createRange();
        }

        // получаем контекст выделения
        var context_left, context_error, context_right;

        var bodyEl = document.getElementsByTagName('BODY')[0];
        var bodyText;
        if ( ! userSelection.getRangeAt){
            userSelection = userSelection.htmlText;
        }
        if (typeof userSelection == 'object') {
            var range = userSelection.getRangeAt(0); // берём первое выделение
            context_left = range.startContainer.nodeValue;
            if (context_left){
                context_left = context_left.substring(0, range.startOffset);
            }else{
                context_left = '';
            }
            context_error = userSelection.toString();
            context_right = range.endContainer.nodeValue;
            if (context_right){
                context_right = context_right.substring(0, range.endOffset);
            }else{
                context_right = '';
            }
        } else if (typeof userSelection == 'string') {
            // получаем текст документа (без \n и с нормализованными пробелами)
            bodyText = bodyEl.innerText.replace(/[ \n]+/g, ' ');

            // находим первое совпадение
            var index = bodyText.indexOf(userSelection);
            var context_start = index;
            var context_end = index + userSelection.length;
            // вычисляем контекст
            var counter = 5;
            while (counter > 0 && context_start >= 0) {
                if (bodyText.charAt(context_start - 1) == " ") counter--;
                context_start--;
            }
            counter = 5;
            while (counter > 0 && context_end < bodyText.length) {
                if (bodyText.charAt(context_end + 1) == " ") counter--;
                context_end++;
            }
            // результат
            context_left = bodyText.slice(context_start, index);
            context_error = userSelection;
            context_right = bodyText.slice(index + userSelection.length, context_end);
        }

        // усечение данных
        if (context_error.length > 255) {
            this.alert(gettext('You can\'t mark more then 255 symbols!'));
            return false;
        }
        if (context_left.length > 255) context_left = context_left.substring(context_left.length - 255);
        if (context_right.length > 255) context_right = context_right.substring(0, 255);


        return {
            'context_left': context_left,
            'context_right': context_right,
            'context_error': context_error
        };

    },

    /**
     * Валидация email
     * @param value
     */
    isValidEmail: function(value) {
        // contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
        return (/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i).test(value);
    }

};
