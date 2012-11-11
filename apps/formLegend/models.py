from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify

import formLegendField


class FormLegendField(models.Model):
    """
    docs
    """
    user = models.ForeignKey(User)
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
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'FormLegend Field'
        verbose_name_plural = 'FormLegend Fields'
        db_table = 'FormLegend Field'
        ordering = ['-date_created']


class FormLegendForm(models.Model):
    """
    A model class that represents a FormLegend form.

    mores docs to come...
    """
    user = models.ForeignKey(User)
    website = models.ForeignKey('FormLegendWebsite')
    form_name = models.CharField(max_length=50)
    form_url = models.URLField()
    result_emailed = models.BooleanField()
    email_to = models.EmailField()
    email_from = models.EmailField()
    email_subject = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    form_slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = 'FormLegend Form'
        verbose_name_plural = 'FormLegend Forms'
        db_table = 'FormLegend Form'
        ordering = ['-date_created']
        unique_together = (
            ('user', 'website', 'form_name'),
            ('user', 'website', 'form_url')
        )

    def save(self):
        """
        This method overrides djangos Model.save() to make sure the slug
        only gets created once to avoid broken urls. Then it calls the
        regular Model.save() method via super to retain functionality.
        """
        if not self.id:
            self.form_slug = slugify(self.form_name)
        super(FormLegendForm, self).save()

    def clean(self):
        """
        Thid method override Model.clean() to make sure that each user
        can only create 5 FormLegendForms.
        """
        new_form = self.__class__
        if (new_form.objects.count() > 4):
            raise ValidationError(
                "Users may only create 5 %s." % new_form.verbose_name_plural
            )
        super(FormLegendForm, self).clean()


class FormLegendWebsite(models.Model):
    """
    A model class that represents a FormLegend website.

    more docs to come...
    """
    user = models.ForeignKey(User)
    site_name = models.CharField(max_length=50)
    # THINK OF A WAY TO VALIDATE domain_name as a Fully qualified domain name
    domain_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    website_slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = 'FormLegend Website'
        verbose_name_plural = 'FormLegend Websites'
        db_table = 'FormLegend Website'
        ordering = ['-date_created']
        unique_together = (('user', 'site_name'), ('user', 'domain_name'),)

    def save(self):
        """
        This method overrides djangos Model.save() to make sure the slug
        only gets created once to avoid broken urls. Then it calls the
        regular Model.save() method via super to retain functionality.
        """
        if not self.id:
            self.website_slug = slugify(self.site_name)
        super(FormLegendWebsite, self).save()

    def clean(self):
        """
        Thid method override Model.clean() to make sure that each user
        can only create 5 FormLegendWebsites.
        """
        new_website = self.__class__
        if (new_website.objects.count() > 4):
            raise ValidationError(
                "Users may only create 5 %s." % new_website.verbose_name_plural
            )
        super(FormLegendWebsite, self).clean()
