from django import forms

import models
import formLegendField


class AddAWebsite(forms.ModelForm):

    class Meta:
        model = models.FormLegendWebsite


class FormMakerForm(forms.ModelForm):

    class Meta:
        model = models.FormLegendForm
