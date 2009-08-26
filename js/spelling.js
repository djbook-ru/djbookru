// Отправка сообщения об ошибке в тексте
// Скрипт основан на системе найденной на сайте Лаборатории Касперского

var spelling = {

  init: function() {
    var it = this;
    parent.document.onkeypress = function(e) { return it.onkeypress(e); }
    it.pending_informer();
    window.status = 'claim module initialized...';
  },

  pending_informer: function() {
    var ajax_response = function(transport) {
      var xml = transport.responseXML.firstChild;
      check_result(false,
		   get_xml_item(xml, 'code'),
		   function() { $('spelling_error_count_pending').innerHTML = get_xml_item(xml, 'pending');
				$('spelling_error_count_assigned').innerHTML = get_xml_item(xml, 'assigned');
				$('spelling_error_count_fixed').innerHTML = get_xml_item(xml, 'fixed');
				$('spelling_error_count_invalid').innerHTML = get_xml_item(xml, 'invalid');
				$('readers_count').innerHTML = get_xml_item(xml, 'readers');
				window.status = 'Проверка очереди жалоб: OK'; },
		   function() { window.status = 'Проверка очереди жалоб: Ошибка'; });
    }
    
    var callback = function() {
      new Ajax.Request('/pending/',
		       { method: 'post', 
			 onSuccess: ajax_response, onFailure: ajax_response });
    }
    
    callback(); // для мгновенного обновления
    var pe = new PeriodicalExecuter(callback, 300);
  },

  onkeypress: function(e) {
    var it = this;
    var pressed=0;
    var we = null;
    if (window.event) we = window.event;
    else if (parent && parent.event) we = parent.event;
    if (we) { // IE & Opera
      pressed = we.keyCode==10 ||  // IE
      (we.keyCode == 13 && we.ctrlKey); // Opera 
    } else if (e) { // NN
      pressed = 
        (e.which==10 && e.modifiers==2) || // NN4
        (e.keyCode==0 && e.charCode==106 && e.ctrlKey) ||
        (e.keyCode==13 && e.ctrlKey) // Mozilla
    }
    if (pressed) {
      //alert('pressed');
      it.dosend();
      return false;
    }
  },

  strip: function(text) {
    text = ""+text;
    return text.replace("\r", "").replace("\n", "").replace(
      new RegExp("^\\s+|\\s+$", "g"), "");
  },
  
  dosend: function(recurrent) {
    var it = this;
    // проверка на древность браузера
    if (navigator.appName.indexOf("Netscape")!=-1 && 
	eval(navigator.appVersion.substring(0,1))<5) {
      return; // ничего не делаем
    }

    // получаем то, что выделил пользователь
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
	if (bodyText.charAt(context_start-1)==" ") counter--;
	context_start--;
      }
      counter = 5;
      while (counter > 0 && context_end < bodyText.length) {
	if (bodyText.charAt(context_end+1)==" ") counter--;
	context_end++;
      }
      // результат
      context_left = bodyText.slice(context_start, index);
      context_error = userSelection;
      context_right = bodyText.slice(index+userSelection.length, context_end);
    }
  
    // усечение данных
    if (context_error.length > 255) {
      alert('Нельзя выделять больше 255 символов!');
      return;
    }
    if (context_left.length > 255) context_left = context_left.substring(context_left.length-255);
    if (context_right.length > 255) context_right = context_right.substring(0, 255);

    // генерируем форму
    var textarea;
    var form = _dom('form',
		    [ _dom('div',
			   [ _txt('Форма сообщения об ошибке') ],
			   [['class', 'claim-title']]),
		      _dom('div',
			   [ _txt('Контекст ошибки'),
			     _dom('div',
				  [ _dom('span', _txt(context_left), []),
				    _dom('span', _txt(context_error), 
					 [['class', 'claim-error']]),
				    _dom('span', _txt(context_right), []) ],
				  [['class', 'padd border claim-context']]) ],
			   [['class', 'padd']]),
		      _dom('div',
			   [ _txt('E-почта'),
			     _dom('div',
				  email = _dom('input', [], [['type', 'text'], ['class', 'wide border']]),
				  [] ) ],
			   [['class', 'padd']]),
		      _dom('div',
			   [ notify = _dom('input', [], [['type', 'checkbox'], ['id', 'notify_id'], ['checked', 'true']]),
			     _dom('label', _txt('Уведомлять об изменении состояния вашего сообщения'), [['for', 'notify_id']])],
			   [['class', 'padd']]),
		      _dom('div',
			   [ _txt('Комментарий'),
			     _dom('div',
				  textarea = _dom('textarea', _txt('Ваш комментарий'), [['class', 'border claim-comment']]),
				  []) ],
			   [['class', 'padd']]),
		      _dom('div',
			   [ _dom('button', _txt('Отправить'), 
				  [['onclick', function() {
				      new Ajax.Request('/claim/',
						       { method: 'post',
							 parameters: 
							 { ctx_left: context_left,
							   selected: context_error,
							   ctx_right: context_right,
							   email: email.value,
							   notify: notify.checked,
							   comment: textarea.value },
							 onSuccess: function(transport) {
							   var response = transport.responseText || "нет ответа";
							   splashwidget.init('Успешно!', 2000);
							   it.pending_informer();
							 },
							 onFailure: function(transport) {
							   window.status = 'Что-то сломалось :(';
							   var response = transport.responseText;
							   splashwidget.init('Ошибка!' + response, 20000);
							 }
						       });
				      // уничтожаем объект
				      form.parentNode.removeChild(form);
				    }]]),
			     _dom('span', _txt(' '), []), // место между кнопками
			     _dom('button', _txt('Отменить'),
				  [['onclick', function() {
				      // уничтожаем объект
				      form.parentNode.removeChild(form);
				    }]]) ],
			   [['class', 'padd claim-button']]) ],
		    [['class', 'claim']]);
    document.getElementsByTagName('BODY')[0].appendChild(form);

    // позиционирование на середине экрана
    var gForm = getGeometry(form);
    form.style.top = (self.innerHeight / 2 - gForm.height / 2 + self.pageYOffset) + 'px';
    form.style.left = (self.innerWidth / 2 - gForm.width / 2) + 'px';

  }
}

