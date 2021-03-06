
//-- added event "focus" to hooks

window.onload = function () {

  /*
  * This hook adds autosizing functionality
  * to your textarea
  */
  BehaveHooks.add(['keydown', 'focus'], function (data) {
    var numLines = data.lines.total,
      fontSize = parseInt(getComputedStyle(data.editor.element)['font-size']),
      padding = parseInt(getComputedStyle(data.editor.element)['padding']);
    data.editor.element.style.height = (((numLines * fontSize) + padding)) + 'px';
  });

  /*
  * This hook adds Line Number Functionality
  */
  BehaveHooks.add(['keydown', 'focus'], function (data) {
    var numLines = data.lines.total,
      house = document.getElementsByClassName('line-nums')[0],
      html = '',
      i;

    for (i = 0; i < numLines; i++) {
      html += '<div>' + (i + 1) + '</div>';
    }

    house.innerHTML = html;

  });

  var editor = new Behave({
    textarea: document.getElementById('editor'),
    replaceTab: true,
    softTabs: true,
    tabSize: 4,
    autoOpen: true,
    overwrite: true,
    autoStrip: true,
    autoIndent: true
  });

  txt_obj = document.getElementById('editor');

  setEditorFocus(txt_obj);
  triggerKeyDownEvent(txt_obj);

  txt_obj.addEventListener('paste', () => {
    setTimeout(() => triggerKeyDownEvent(txt_obj), 0)
  }, false);
};

function setEditorFocus(txt_obj) {
  // sometimes autofocs on textarea doesn't work => js as fallback
  function focusEditor() {
    txt_obj.focus();
  }
  setTimeout(() => focusEditor(), 500)
}

function triggerKeyDownEvent(element) {
  element.dispatchEvent(new KeyboardEvent('keydown', { 'key': '' }));
}


// -- copy base64 string to clipboard

function addCopyPasteListener() {
  var copyB64InputBtn = document.querySelector('.copyBtn');

  copyB64InputBtn.addEventListener('click', function(event) {
    var copyB64Input = document.querySelector('.b64input');
    copyB64Input.focus();
    copyB64Input.select();

    try {
      var success = document.execCommand('copy');
      var msg = success ? 'successfully' : 'unsuccessfully';
      console.log('text copied ' + msg);
    } catch (err) {
      console.log('Unknown error on copying text to clipboard');
    }
  });
}
