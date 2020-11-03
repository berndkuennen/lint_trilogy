
//-- added event "focus" to hooks

window.onload = function(){
			
  /*
   * This hook adds autosizing functionality
   * to your textarea
   */
  BehaveHooks.add(['keydown','focus'], function(data){
  	var numLines = data.lines.total, 
  	    fontSize = parseInt( getComputedStyle(data.editor.element)['font-size'] ),
  	    padding  = parseInt( getComputedStyle(data.editor.element)['padding'] );
	data.editor.element.style.height = (((numLines*fontSize)+padding))+'px';
  });
  			
  /*
   * This hook adds Line Number Functionality
   */
  BehaveHooks.add(['keydown','focus'], function(data){
  	var numLines = data.lines.total,
    		house = document.getElementsByClassName('line-nums')[0],
  		html = '',
  		i;
  	
  	for(i=0; i<numLines; i++){
  		html += '<div>'+(i+1)+'</div>';
  	}
  	
  	house.innerHTML = html;
  
  });
  			
  var editor = new Behave({
    	textarea: 	document.getElementById('editor'),
  	replaceTab: 	true,
	softTabs: 	true,
        tabSize: 	4,
  	autoOpen:	true,
  	overwrite: 	true,
  	autoStrip: 	true,
  	autoIndent: 	true
  });
};



function setEditorFocus() {
  // sometimes autofocs on textarea doesn't work => js as fallback
  txt_obj = document.getElementById('editor');
  function focusEditor() {
    txt_obj.focus();
  }
  setTimeout( "focusEditor()", 500) ;
}

