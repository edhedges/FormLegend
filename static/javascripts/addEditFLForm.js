/* Docs */
$(document).ready(function() {resultEmailedCheckboxClicked();});

/* Docs */
function submitClicked() {
  if($('#resultEmailedID').not(':checked')) {
    $('.hiddenFormElementGroup input:hidden').prop('value', '');
  }
}

/* Docs */
function resultEmailedCheckboxClicked() {
  var isChecked = $('#resultEmailedID').is(':checked');
  var shownClassStr = 'formElementGroup', hiddenClassStr = 'hiddenFormElementGroup', classChangedStr = 'classWasChanged';
  if(isChecked) {
    $('.' + hiddenClassStr).addClass(classChangedStr + ' ' + shownClassStr).removeClass(hiddenClassStr);
    $('.' + shownClassStr + ' input:hidden').prop('type', 'text');
  }
  else {
    $('.' + classChangedStr).addClass(hiddenClassStr).removeClass(shownClassStr + ' ' +  classChangedStr);
    $('.' + hiddenClassStr + ' input:text').prop('type', 'hidden');
  }
}