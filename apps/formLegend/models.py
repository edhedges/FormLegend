from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):
    """
    docs

    write crud functionality in functions
    """
    user = models.ForeignKey(User)
    form_name = models.CharField(max_length=50)
    form_url = models.URLField()
    form_fields = models.CommaSeparatedIntegerField(max_length=100)

    class Meta:
        verbose_name = 'FormLegend Form'
        verbose_name_plural = 'FormLegend Forms'
        db_table = 'FormLegend Form'


class Website(models.Model):
    """
    docs

    write crud functionality in functions
    """
    user = models.ForeignKey(User)
    form = models.ForeignKey('Form')
    site_name = models.CharField(max_length=50)
    domain_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'FormLegend Website'
        verbose_name_plural = 'FormLegend Websites'
        db_table = 'FormLegend Website'
