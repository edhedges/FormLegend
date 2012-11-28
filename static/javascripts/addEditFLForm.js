/* Docs */
$(document).ready(function() {
  resultEmailedCheckboxClicked();
  var fieldCount = $('.formLegendField').length;
  var deleteFieldButton = "<input class='deleteFieldButton' onclick='deleteFieldClicked(this)' type='button' value='Delete Field' />";
  $('.formLegendField').each(function()  {
    $(deleteFieldButton).appendTo($(this));
  });
});

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

/* Docs */
function addFieldClicked() {
  var newFieldHtml;
  var fieldCount = $('.formLegendField').length;
  if(fieldCount < 12) {
    newFieldHtml = "<div class='formLegendField'>" +
      "<input type='hidden' name='formLegendForm-" + fieldCount + "-id' id='id_formLegendForm-" + fieldCount + "-id'>" +
      "<div class='formElementGroup'>" +
      "<label>Field Label</label>" +
      "<input id='id_formLegendForm-" + fieldCount + "-field_label' type='text' name='formLegendForm-" + fieldCount + "-field_label' maxlength='100'>" +
      "</div>" +
      "<div class='formElementGroup'>" +
        "<label>Field Type</label>" +
        "<select name='formLegendForm-" + fieldCount + "-field_type' id='id_formLegendForm-" + fieldCount + "-field_type'>" +
          "<option value=' selected='selected'>---------</option>" +
          "<option value='1'>Check Box</option>" +
          "<option value='2'>Single-Line Text</option>" +
          "<option value='3'>Single-Select List</option>" +
          "<option value='4'>Date YYYY/MM/DD</option>" +
          "<option value='5'>Date YYYY/MM/DD and Time HH:MM:SS</option>" +
          "<option value='6'>Multi-Select List</option>" +
          "<option value='7'>Hidden</option>" +
          "<option value='8'>Time HH:MM:SS</option>" +
          "<option value='9'>Multi-Line Text</option>" +
          "<option value='10'>Check Boxes</option>" +
          "<option value='11'>Radio Buttons</option>" +
          "<option value='12'>Email</option>" +
          "<option value='13'>Decimal</option>" +
          "<option value='14'>Integer</option>" +
        "</select>" +
      "</div>" +
      "<div class='formElementGroup'>" +
        "<label>Field Is Required&nbsp;</label>" +
        "<input checked='checked' type='checkbox' name='formLegendForm-" + fieldCount + "-field_is_required' id='id_formLegendForm-" + fieldCount + "-field_is_required'>" +
      "</div>" +
      "<div class='formElementGroup'>" +
        "<label>Field Has Choices&nbsp;</label>" +
        "<input type='checkbox' name='formLegendForm-" + fieldCount + "-field_has_choices' id='id_formLegendForm-" + fieldCount + "-field_has_choices'>" +
      "</div>" +
      "<div class='formElementGroup'>" +
        "<label>Field Choices</label>" +
        "<span class='help_text'>Please enter fields choices separated by commas. If choices themselves must have commas, please surround with grave accents (e.g. `dear, anonymous`, `hello, there`, howdy).</span>" +
        "<input id='id_formLegendForm-" + fieldCount + "-field_choices' type='text' name='formLegendForm-" + fieldCount + "-field_choices' maxlength='500'>" +
      "</div>" +
      "<div class='formElementGroup'>" +
        "<label>Field Initial Value</label>" +
        "<input id='id_formLegendForm-" + fieldCount + "-field_initial_value' type='text' name='formLegendForm-" + fieldCount + "-field_initial_value' maxlength='100'>" +
      "</div>" +
      "<div class='formElementGroup'>" +
        "<label>Field Help Text</label>" +
        "<input id='id_formLegendForm-" + fieldCount + "-field_help_text' type='text' name='formLegendForm-" + fieldCount + "-field_help_text' maxlength='150'>" +
      "</div>" +
      "<input class='deleteFieldButton' onclick='deleteFieldClicked(this)' type='button' value='Delete Field' />" +
    "</div>";
    $('#id_formLegendForm-TOTAL_FORMS').attr('value', fieldCount + 1);
  }
  else newFieldHtml = "<span id='noMoreFields' class='errors'>Each FormLegendForm may only contain 12 FormLegendFields.</span>";
  if($('#noMoreFields').length === 0) $(newFieldHtml).insertBefore('.addFieldButton');
}

/* Docs */
function deleteFieldClicked(deleteButton) {
  var formLegendField = deleteButton.parentNode;
  var fieldCount = $('.formLegendField').length;
  $(formLegendField).children('.hideMe').children('input').attr('checked', true);
  $(formLegendField).css('visibility', 'hidden');
  $(formLegendField).css('position', 'absolute');
}