from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.template.defaultfilters import slugify

import formLegendField


class DynamicFormLegendForm(models.Model):
    user = models.ForeignKey(User)
    fl_form = models.OneToOneField('FormLegendForm', related_name='formLegendFormD')
    form_key = models.CharField(max_length=50, blank=True)
    form_script = models.TextField(blank=True)
    form_html = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Dynamic FormLegend Form'
        verbose_name_plural = 'Dynamic FormLegend Forms'
        db_table = 'Dynamic FormLegend Form'
        ordering = ['-date_created']


class FormLegendField(models.Model):
    """
    docs
    """
    user = models.ForeignKey(User)
    form = models.ForeignKey('FormLegendForm', related_name='formLegendForm')
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
    field_initial_value = models.CharField(max_length=100, blank=True)
    field_help_text = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'FormLegend Field'
        verbose_name_plural = 'FormLegend Fields'
        db_table = 'FormLegend Field'
        ordering = ['date_created']

    def clean(self):
        """
        Thid method override Model.clean() to make sure that each can
        only create 12 FormLegenFields for each of their 3
        FormLegendForms for each of their 5 FormLegendWebsites.

        This probably will not be called because the javascript should
        prevent the user from creating more than 12 FormLegenFields.
        """
        if not self.pk:
            if (self.form.formLegendForm.all().count() > 11):
                raise ValidationError(
                    'Users may only create 11 %s per %s.' % (
                        self._meta.verbose_name_plural,
                        self.form._meta.verbose_name_plural
                    )
                )
            super(FormLegendField, self).clean()


class FormLegendForm(models.Model):
    """
    A model class that represents a FormLegend form.

    mores docs to come...
    """
    user = models.ForeignKey(User)
    website = models.ForeignKey('FormLegendWebsite', related_name='formLegendWebsite')
    form_name = models.CharField(max_length=50)
    form_url = models.URLField()
    result_emailed = models.BooleanField()
    email_to = models.EmailField(blank=True)
    email_from = models.EmailField(blank=True)
    email_subject = models.CharField(blank=True, max_length=50)
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
        Thid method override Model.clean() to make sure that each can
        only create 3 FormLegendForms for each of their 5
        FormLegendWebsites.
        """
        if not self.pk:
            try:
                if (self.website.formLegendWebsite.all().count() > 2):
                    raise ValidationError(
                        'Users may only create 3 %s per %s.' % (
                            self._meta.verbose_name_plural,
                            self.website._meta.verbose_name
                        )
                    )
                super(FormLegendForm, self).clean()
            except FormLegendWebsite.DoesNotExist:
                raise ValidationError(
                    'Please choose a website for this FormLegend Form'
                )


class FormLegendWebsite(models.Model):
    """
    A model class that represents a FormLegend website.

    more docs to come...
    """
    user = models.ForeignKey(User)
    site_name = models.CharField(max_length=50)
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
        if not self.pk:
            new_website = self.__class__
            if (new_website.objects.count() > 4):
                raise ValidationError(
                    'Users may only create 5 %s.' % self._meta.verbose_name_plural
                )
            super(FormLegendWebsite, self).clean()
