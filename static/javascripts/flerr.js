/* docs */
function renderFormLegendError() {
  var fl_div = document.getElementById('fl_form');
  if (typeof(fl_div) != 'undefined' && fl_div !== null) {
    fl_div.innerHTML = "<p style='display: block; background-color: white; color: red;'>There was a problem with your FormLegend markup.</p>";
  }
}window.onload = renderFormLegendError;