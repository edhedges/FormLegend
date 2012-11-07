from django.db import models
from django.contrib.auth.models import User

import formLegendField


class FormLegendField(models.Model):
    form = models.ForeignKey('FormLegendForm')
    field_label = models.CharField(max_length=100)
    field_type = models.IntegerField(choices=formLegendField.DESCRIPTIONS)
    field_is_hidden = models.BooleanField(default=False)
    field_is_required = models.BooleanField(default=True)
    field_has_choices = models.BooleanField(default=False)
    field_choices = models.CharField(
        max_length=500,
        blank=True,
        help_text="Please enter fields choices separated by commas. If choices"
        " themselves must have commas, please surround with grave accents "
        "(e.g. `dear, anonymous`, `hello, there`, howdy)."
    )
    field_initial_value = models.CharField(max_length=100)
    field_help_text = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'FormLegend Field'
        verbose_name_plural = 'FormLegend Fields'
        db_table = 'FormLegend Field'


class FormLegendForm(models.Model):
    """
    docs

    write crud functionality in functions
    """
    website = models.ForeignKey('FormLegendWebsite')
    form_name = models.CharField(max_length=50)
    form_url = models.URLField()
    result_emailed = models.BooleanField()
    email_to = models.EmailField()
    email_from = models.EmailField()
    email_subject = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'FormLegend Form'
        verbose_name_plural = 'FormLegend Forms'
        db_table = 'FormLegend Form'


class FormLegendWebsite(models.Model):
    """
    docs

    write crud functionality in functions
    """
    user = models.ForeignKey(User)
    site_name = models.CharField(max_length=50)
    domain_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'FormLegend Website'
        verbose_name_plural = 'FormLegend Websites'
        db_table = 'FormLegend Website'
