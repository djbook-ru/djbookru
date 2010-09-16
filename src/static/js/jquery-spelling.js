$(function() {

    spelling.startInformer()

    $('html').bind('keypress', function(e) {

        if (e.keyCode == 13 && e.ctrlKey) {
            spelling.showForm();
        }

    })
});

var spelling  = {
    /**
     * Обновление статуса перевода
     */
    startInformer: function() {
        var updateInformer = function() {

          $.get('/claims/pending/', function(xml){
              var $xml = $(xml);
              $('#spelling_error_count_pending').html($xml.find('pending').text());
              $('#spelling_error_count_assigned').html($xml.find('assigned').text());
              $('#spelling_error_count_fixed').html($xml.find('fixed').text());
              $('#spelling_error_count_invalid').html($xml.find('invalid').text());
              //$('#readers_count').html($xml.find('readers').text());
          }, 'xml');

        }

        updateInformer();
        setInterval(updateInformer, 30000);
    },

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

        var $form = $('<div title="Форма сообщения об ошибке" >' +
                '<form id="spelling_form">' +
                '<p><label>Контекст ошибки</label>' +
                '<span class="display">' + context_error + '</span>' +
                '</p>' +
                '<p><label>Комментарий</label>' +
                '<textarea id="comment" />' +
                '</p>' +
                '<p><label>E-mail</label>' +
                '<input type="text" id="email"></p>' +
                '<p><input type="checkbox"  id="notify" />' +
                '<label>Уведомлять об изменении состояния вашего сообщения</label></p>' +
                '</div>');

        $form.dialog({
            resizable: false,
            modal: true,
            width: 380,
            close: function(event, ui) {
                is_show = false
            },
            buttons: {
                'Отправить': function() {
                    $.post('/claims/', {ctx_left: selection.context_left,
							   selected: selection.context_error,
							   ctx_right: selection.context_right,
							   email: $('#email').val(),
							   notify: $('#notify').attr('checked'),
							   comment: $('#comment').val()},
                            function(xml){
                                var text = $xml.find('result').text();
                                if (text == 'ok'){
                                    spelling.alert('Ваше сообщение успешно отправлено!');
                                }
                                else{
                                    spelling.alert('К сожалению при отправке произошла ошибка. Попробуйте повторить позже.');
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
     * Возвращает массив с текстами ошибки и ее обрамления
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
            this.alert('Нельзя выделять больше 255 символов!');
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

        title = title || 'Сообщение';

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
    }

};