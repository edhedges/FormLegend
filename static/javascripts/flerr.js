/* docs */
function renderFormLegendError() {
  var fl_div = document.getElementById('fl_form');
  if (typeof(fl_div) != 'undefined' && fl_div !== null) {
    fl_div.innerHTML = "<p style='display: block; background-color: white; color: red;'>There was an error when retrieving your FormLegend Form. Please make sure that you have created a form and followed the installation instructions correctly.</p>";
  }
}window.onload = renderFormLegendError;