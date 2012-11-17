from django import forms

from formLegend.models import FormLegendWebsite, FormLegendForm


class FormLegendWebsiteForm(forms.ModelForm):
    """
    A simple ModelForm that renders a FormLegendWebsite object as a form
    for the user to be able to add and edit the fiels. The user and
    date_created field are excluded. They user tied to the model will
    receive it's value in the view which will go to the user logged in.
    The date_created is created on each model creation.
    """
    class Meta:
        model = FormLegendWebsite
        exclude = ('user', 'date_created',)


class FormLegendFormForm(forms.ModelForm):
    """
    docs
    """
    class Meta:
        model = FormLegendForm
        exclude = ('user', 'date_created',)
        widgets = {
            'email_to': forms.HiddenInput(),
            'email_from': forms.HiddenInput(),
            'email_subject': forms.HiddenInput(),
            'result_emailed': forms.CheckboxInput(
                attrs={
                    'id': 'resultEmailedID',
                    'onclick': "resultEmailedCheckboxClicked();"
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """
        Override the ModelForm.__init__() method to change the display
        text of the website object so that it shows up in a manner that
        is user friendly.
        """
        super(FormLegendFormForm, self).__init__(*args, **kwargs)
        self.fields['website'].label_from_instance = lambda obj: "%s" % (obj.site_name)

    def clean(self):
        cleaned_data = super(FormLegendFormForm, self).clean()
        email_result = cleaned_data.get('result_emailed')
        if email_result:
            pass
        else:
            pass
        return cleaned_data
