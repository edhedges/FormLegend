from django import forms

import models


class FormLegendWebsiteForm(forms.ModelForm):
    """
    docs
    """
    class Meta:
        model = models.FormLegendWebsite
        exclude = ('user', 'date_created',)


class FormLegendFormForm(forms.ModelForm):
    """
    docs
    """
    class Meta:
        model = models.FormLegendForm
        exclude = ('user', 'date_created',)

    def __init__(self, *args, **kwargs):
        """
        Override the ModelForm.__init__() method to change the display
        text of the website object so that it shows up in a manner that
        is user friendly.
        """
        super(FormLegendFormForm, self).__init__(*args, **kwargs)
        self.fields['website'].label_from_instance = lambda obj: "%s" % (obj.site_name)
