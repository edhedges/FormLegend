from django import forms
from django.core.mail import send_mail

from formLegend.models import FormLegendWebsite, FormLegendForm,\
    FormLegendFormData

import FormLegendField as formLegendField


class FormLegendFormDataForm(forms.ModelForm):
    """
    docs
    """
    class Meta:
        model = FormLegendFormData
        exclude = ('user', 'fl_form', 'form_key', 'date_created')

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        docs
        """
        form_data = super(FormLegendFormDataForm, self).save(commit=False)
        if commit:
            form_data.save()
            fl_form_obj = form_data.fl_form.fl_form
            should_email = fl_form_obj.result_emailed
            if should_email:
                subject = fl_form_obj.email_subject
                message = form_data.form_data
                sender = fl_form_obj.email_from
                recipient = [fl_form_obj.email_to]
                if sender == '':
                    sender = 'eddiehedges@gmail.com'
                if subject == '':
                    subject == 'Form Legend Form: %s Submission' % fl_form_obj.form_name
                send_mail(subject, message, sender, recipient)
        return form_data


class DynamicFormLegendFormForm(forms.Form):
    """
    docs
    """
    def __init__(self, field_list, *args, **kwargs):
        """
        docs
        """
        super(DynamicFormLegendFormForm, self).__init__(*args, **kwargs)
        for field in field_list:
            if(field.field_type in formLegendField.FORM_LEGEND_WIDGETS):
                widget_class = formLegendField.FORM_LEGEND_WIDGETS[field.field_type]
                if widget_class.__name__ == 'SelectDateWidget':
                    self.fields[field.field_label] = field.field_class
                    widget_instance = getattr(forms.extras, widget_class.__name__)()
                else:
                    self.fields[field.field_label] = field.field_class
                    widget_instance = getattr(forms.widgets, widget_class.__name__)()
                self.fields[field.field_label].widget = widget_instance
            else:
                self.fields[field.field_label] = field.field_class
            css_classes = ''
            class_name = field.field_class.__class__.__name__
            if class_name == 'DateField':
                css_classes += 'date_field '
            if class_name == 'EmailField':
                css_classes += 'email_field '
            if class_name == 'DecimalField':
                css_classes += 'decimal_field '
            if class_name == 'IntegerField':
                css_classes += 'integer_field '
            if field.is_required:
                css_classes += 'required_field'
            self.fields[field.field_label].widget.attrs['class'] = css_classes
            if field.initial_value:
                self.fields[field.field_label].initial = field.initial_value
            if field.help_text:
                self.fields[field.field_label].help_text = field.help_text
            if field.has_choices and field.field_type in formLegendField.ALLOWS_CHOICES:
                self.fields[field.field_label].choices = field.choices


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
