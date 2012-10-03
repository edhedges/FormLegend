from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):
    """
    docs

    write crud functionality in functions
    """
    user = models.ForeignKey(User)
    form_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'FormLegend Form'
        verbose_name_plural = 'FormLegend Forms'
        db_table = 'FormLegend Form'

    #possibly pass in fields and other info below

    #def create_form(self, form):
        #asdf

    #def read_form(self, form):
        #asdf

    #def update_form(self, form):
        #adsf

    #def delete_form(self, form):
        #asdf


class Website(models.Model):
    """
    docs

    write crud functionality in functions
    """
    user = models.ForeignKey(User)
    form = models.ForeignKey('Form')
    site_name = models.CharField(max_length=50)
    domain_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'FormLegend Website'
        verbose_name_plural = 'FormLegend Websites'
        db_table = 'FormLegend Website'

    #def create_website(self, website):
        #asdf

    #def read_website(self, website):
        #asdf

    #def update_website(self, website):
        #adsf

    #def delete_website(self, website):
        #asdf
