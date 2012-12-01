from django import forms
from django.contrib.admin import widgets
from django.forms.extras import SelectDateWidget


"""
Constants for input types from:
https://docs.djangoproject.com/en/1.4/ref/forms/fields/#built-in-field-classes
https://docs.djangoproject.com/en/1.4/ref/forms/widgets/#built-in-widgets

Fields removed for first version: file input, date time input, time input
"""
CHECKBOX = 1
TEXT = 2
SELECT = 3
DATE = 4
SELECTMULTIPLE = 5
HIDDEN = 6
TEXTAREA = 7
CHECKBOXMULTIPLE = 8
RADIOMULTIPLE = 9
EMAIL = 10
DECIMAL = 11
INTEGER = 12

"""
Field descriptions used in select list for adding/editing a form
"""
DESCRIPTIONS = (
    (CHECKBOX, 'Check Box'),
    (TEXT, 'Single-Line Text'),
    (SELECT, 'Single-Select List'),
    (DATE, 'Date YYYY/MM/DD'),
    (SELECTMULTIPLE, 'Multi-Select List'),
    (HIDDEN, 'Hidden'),
    (TEXTAREA, 'Multi-Line Text'),
    (CHECKBOXMULTIPLE, 'Check Boxes'),
    (RADIOMULTIPLE, 'Radio Buttons'),
    (EMAIL, 'Email'),
    (DECIMAL, 'Decimal'),
    (INTEGER, 'Integer'),
)

"""
Key value pairs of fields
"""
FORM_LEGEND_FIELDS = {
    CHECKBOX: forms.BooleanField,
    TEXT: forms.CharField,
    SELECT: forms.ChoiceField,
    DATE: forms.DateField,
    SELECTMULTIPLE: forms.MultipleChoiceField,
    HIDDEN: forms.CharField,
    TEXTAREA: forms.CharField,
    CHECKBOXMULTIPLE: forms.MultipleChoiceField,
    RADIOMULTIPLE: forms.ChoiceField,
    EMAIL: forms.EmailField,
    DECIMAL: forms.DecimalField,
    INTEGER: forms.IntegerField,
}

"""
Widgets used for django form fields
"""
FORM_LEGEND_WIDGETS = {
    DATE: SelectDateWidget,
    HIDDEN: forms.HiddenInput,
    TEXTAREA: forms.Textarea,
    CHECKBOXMULTIPLE: forms.CheckboxSelectMultiple,
    RADIOMULTIPLE: forms.RadioSelect,
}

ALLOWS_CHOICES = {
    CHECKBOXMULTIPLE: True,
    SELECT: True,
    SELECTMULTIPLE: True,
    RADIOMULTIPLE: True
}
