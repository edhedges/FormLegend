from django import forms
from django.forms.extras import SelectDateWidget

"""
Constants for input types from:
https://docs.djangoproject.com/en/1.4/ref/forms/fields/#built-in-field-classes
https://docs.djangoproject.com/en/1.4/ref/forms/widgets/#built-in-widgets
"""
CHECKBOX = 1
TEXT = 2
SELECT = 3
DATE = 4
DATETIME = 5
SELECTMULTIPLE = 6
HIDDEN = 7
TIME = 8
TEXTAREA = 9
CHECKBOXMULTIPLE = 10
RADIOMULTIPLE = 11
EMAIL = 12
DECIMAL = 13
INTEGER = 14

"""
Field descriptions used in select list for adding/editing a form
"""
DESCRIPTIONS = (
    (CHECKBOX, 'Check Box'),
    (TEXT, 'Single-Line Text'),
    (SELECT, 'Single-Select List'),
    (DATE, 'Date YYYY/MM/DD'),
    (DATETIME, 'Date YYYY/MM/DD and Time HH:MM:SS'),
    (SELECTMULTIPLE, 'Multi-Select List'),
    (HIDDEN, 'Hidden'),
    (TIME, 'Time HH:MM:SS'),
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
    DATETIME: forms.DateTimeField,
    SELECTMULTIPLE: forms.MultipleChoiceField,
    HIDDEN: forms.CharField,
    TIME: forms.TimeField,
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
