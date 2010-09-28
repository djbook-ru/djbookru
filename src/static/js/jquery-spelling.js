var gettext = gettext || function(val){return val}

$(function() {

    spelling.startInformer();

    $(document).bind('keydown', function(e) {
        if (e.keyCode == 13 && e.ctrlKey) {
            spelling.showForm();
        }
    })
});

var spelling = {
    /**
     * Запуск обновления статуса информера по таймеру
     */
    startInformer: function() {
        this.updateInformer();
        setInterval(this.updateInformer, 30000);
    },

    /**
     * Обновление статуса перевода
     */
    updateInformer: function() {

        $.get('/claims/pending/', function(xml) {
            var $xml = $(xml);
            $('#spelling_error_count_pending').html($xml.find('pending').text());
            $('#spelling_error_count_assigned').html($xml.find('assigned').text());
            $('#spelling_error_count_fixed').html($xml.find('fixed').text());
            $('#spelling_error_count_invalid').html($xml.find('invalid').text());
            //$('#readers_count').html($xml.find('readers').text());
        }, 'xml');

    },
    $form: '',
    /**
     * Форма для заполнения данных об обнаруженной ошибке
     */
    showForm: function() {

        var selection = this.getErrorSelection()

        if (selection == false)
            return;

        var context_error = '<span>' + selection.context_left + '</span>'
                + '<span class="ui-widget-content ui-state-error">' + selection.context_error
                + '</span>' + '<span>' + selection.context_right + '</span>';

        this.$form = this.$form || $('<div title="'+gettext('Send error form')+'" >' +
                '<form id="spelling_form">' +
                '<p><label>'+gettext('Context of error')+'</label>' +
                '<span class="display">' + context_error + '</span>' +
                '</p>' +
                '<p><label>'+gettext('Comment')+' *</label>' +
                '<textarea id="comment" />' +
                '</p>' +
                '<p><label>E-mail *</label>' +
                '<input type="text" id="email"></p>' +
                '<p><input type="checkbox"  id="notify" />' +
                '<label>'+gettext('Notify about changes of error status')+'</label></p>' +
                '</div>');

        this.$form.dialog({
            resizable: false,
            modal: true,
            width: 380,
            beforeClose: function() {
                $(this).find('form')[0].reset();
            },
            buttons: {
                'Отправить': function() {
                    var text_errors = '';
                    if ($('#comment').val() == '') {
                        text_errors += '<div>'+gettext('Comment is required.')+'</div>';
                    }
                    if ($('#email').val() == '') {
                        text_errors += '<div>'+gettext('E-mail is required.')+'</div>';
                    }
                    else if (! spelling.isValidEmail($('#email').val())) {
                        text_errors += '<div>'+gettext('E-mail is wrong.')+'</div>';
                    }

                    if (text_errors != ''){
                        spelling.alert(text_errors, gettext('Form has errors.'));
                        text_errors = '';
                        return;
                    }

                    $.post('/claims/', {ctx_left: selection.context_left,
                        selected: selection.context_error,
                        ctx_right: selection.context_right,
                        email: $('#email').val(),
                        notify: $('#notify').attr('checked'),
                        comment: $('#comment').val()},
                          function(xml) {
                              var text = $(xml).find('result').text();
                              if (text == 'ok') {
                                  spelling.alert(gettext('Message sent success!'));
                                  spelling.updateInformer();
                              }
                              else {
                                  spelling.alert(gettext('Something broken. Try later.'));
                              }

                          });
                    $(this).dialog('close');
                },
                'Отменить': function() {
                    $(this).dialog('close');
                }
            }
        });
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
            context_left = range.startContainer.nodeValue.substring(0, range.startOffset);
            context_error = userSelection.toString();
            context_right = range.endContainer.nodeValue.substring(range.endOffset);
        } else if (typeof userSelection == 'string') {
            // получаем текст документа (без \n и с нормализованными пробелами)
            bodyText = bodyEl.innerText.replace(/[ \n]+/g, ' ');

            // находим первое совпадение
            var index = bodyText.indexOf(userSelection);
            var context_start = index;
            var context_end = index + userSelection.length;
            // вычисляем контекст
            var counter = 5
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
     * Алерт на замену стандартному
     * @param message
     * @param title
     */
    alert: function(message, title) {

        title = title || gettext('Message');

        var $form = $('<div title="' + title + '" >' +
                '<div>' + message + '</div>' +
                '</div>');

        $form.dialog({
            resizable: false,
            modal: true,
            width: 300,
            buttons: {
                'Ок': function() {
                    $(this).dialog('close');
                }
            }
        });
    },
    /**
     * Валидация email
     * @param value
     */
    isValidEmail: function(value) {
        // contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
        return /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i.test(value);
    }

};