from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import fields
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, DetailView,\
    UpdateView, DeleteView, RedirectView
from django.views.decorators.clickjacking import xframe_options_exempt

from formLegend.models import FormLegendWebsite, FormLegendForm,\
    FormLegendField, DynamicFormLegendForm, FormLegendFormData
from formLegend.forms import FormLegendWebsiteForm, FormLegendFormForm,\
    DynamicFormLegendFormForm, FormLegendFormDataForm

import formLegendField


def saveDynamicFormLegendForm(authenticated_user, form_legend_form):
    """
    docs
    """
    form_fields = FormLegendField.objects.filter(
        user=authenticated_user,
        form=form_legend_form
    )
    field_list = createFieldList(form_fields)
    form_instance = DynamicFormLegendFormForm(field_list)
    print 'form_instance'
    print form_instance
    print 'form_instance as p'
    print form_instance.as_p()
    form_html = generateFormHtml(form_instance)
    print 'form html' + form_html
    df_obj, df_was_created = DynamicFormLegendForm.objects.get_or_create(
        user=authenticated_user,
        fl_form=form_legend_form
    )
    df_obj.form_html = form_html
    if df_was_created:
        df_obj.form_key = authenticated_user.username + "-" + str(df_obj.pk)
        df_obj.form_script = generateUserFormScript(df_obj.form_key)
    df_obj.save()


def createFieldList(form_fields):
    """
    docs
    """
    field_list = []
    for field in form_fields:
        field_label = field.field_label.lower().replace(' ', '_')
        field_class = formLegendField.FORM_LEGEND_FIELDS[field.field_type]
        field_instance = getattr(fields, field_class.__name__)()
        if field.field_is_required:
            field_list.append(DynamicFormField(field.field_type, field_label, field_instance, True))
        else:
            field_list.append(DynamicFormField(field.field_type, field_label, field_instance, False))
    return field_list


def generateFormHtml(form_instance):
    """
    docs
    """
    form_html_components = []
    form_html_components.append("<form>")
    form_html_components.append(form_instance.as_p())
    form_html_components.append("<input type='button' onclick='submitFLForm(this)' value='Submit' />")
    form_html_components.append("</form>")
    form_html = ''.join(form_html_components)
    return form_html


def generateUserFormScript(form_key):
    """
    docs
    """
    form_script_components = []
    form_script_components.append("<div id='fl_form' class='%s'></div>\n" % form_key)
    form_script_components.append("<script type='text/javascript'>\n")
    form_script_components.append("  var fl_form_key = '%s';\n" % form_key)
    form_script_components.append("  (function() {\n")
    form_script_components.append("    var fl_script = document.createElement('script'); fl_script.type = 'text/javascript'; fl_script.async = true;\n")
    form_script_components.append("    fl_script.src = 'http://127.0.0.1:8000/form-script/' + fl_form_key + '/fl.js';\n")
    form_script_components.append("    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(fl_script);\n")
    form_script_components.append("  })();\n")
    form_script_components.append("</script>\n")
    form_script_components.append("<noscript>Please enable javascript to view the Form.</noscript>")
    form_script = ''.join(form_script_components)
    return form_script


class DynamicFormField(object):
    """
    docs
    """
    def __init__(self, field_type, field_label, field_class, is_required):
        self.field_type = field_type
        self.field_label = field_label
        self.field_class = field_class
        self.is_required = is_required


class LogInRequiredMixin(object):
    """
    Class view mixin that can be inherited to require a user be logged
    in.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        This method is decorated with the login_required method
        decorator that makes sure specific views/templates are only
        accessible if the user is authenticated and if they aren't they
        are redirected to the LOGIN_URL in settings.py.
        """
        return super(LogInRequiredMixin, self).dispatch(*args, **kwargs)


class XFrameExemptMixin(object):
    """
    Class view mixin that can be inherited to exempt a view from xframe
    restriction brought on by XFrameOptionsMiddleware.
    """

    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        """
        This method is decorated with the xframe_options_exempt method
        decorator that makes sure specific views/templates are exempt
        from the xframe restrictions brought on by djangos
        XFrameOptionsMiddleware. This is used by views that do cross
        domain and iframe talking.
        """
        return super(XFrameExemptMixin, self).dispatch(*args, **kwargs)


class DashboardView(LogInRequiredMixin, TemplateView):
    """
    Class view that handles the request to the /dashboard/
    """
    template_name = 'formLegend/dashboard.html'

    def get_context_data(self, **kwargs):
        """
        This method makes sure to pass the correct context to the users
        dashboard. This includes their websites and forms.
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        authenticated_user = self.request.user
        fl_websites = FormLegendWebsite.objects.filter(user=authenticated_user)
        fl_forms = FormLegendForm.objects.filter(user=authenticated_user)
        context['fl_websites'] = fl_websites
        context['fl_forms'] = fl_forms
        return context


class AddWebsiteView(LogInRequiredMixin, CreateView):
    """
    Class view that handles the request to /websites/add/. This page
    give the user the ability to add a website to their FormLegend
    account.
    """
    model = FormLegendWebsite
    form_class = FormLegendWebsiteForm
    template_name = 'formLegend/add_fl_website.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        """
        This method overrides form_valid from the ModelFormMixin and
        makes sure the autenticated user is bound to it.
        """
        fl_website_form = form.save(commit=False)
        fl_website_form.user = self.request.user
        fl_website_form.save()
        return super(AddWebsiteView, self).form_valid(form)


class EditWebsiteView(LogInRequiredMixin, UpdateView):
    """
    Class view that handles the request to a specific FormLegendWebsite
    object and renders a form populated with that objects values for
    editing purposes.
    """
    model = FormLegendWebsite
    slug_field = 'website_slug'
    form_class = FormLegendWebsiteForm
    template_name = 'formLegend/edit_fl_website.html'
    success_url = '/dashboard/'


class DeleteWebsiteView(LogInRequiredMixin, DeleteView):
    """
    Class view that handles the request to a specific FormLegendWebsite
    object and asks whether or not the user would like to delete that
    website. A yes deletes the website and a no will just go back to the
    users dashboard.
    """
    model = FormLegendWebsite
    slug_field = 'website_slug'
    template_name = 'formLegend/delete_fl_website.html'
    success_url = '/dashboard/'


class AddFormView(LogInRequiredMixin, CreateView):
    """
    docs
    """
    model = FormLegendForm
    form_class = FormLegendFormForm
    template_name = 'formLegend/add_fl_form.html'
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        """
        This method overrides get_context_data and makes sure that if
        the user hasn't added any website than that is specified as well
        as passing formLegendFormFormSet so the user can add form fields
        to their form. Formset for FormLegendForm and FormLegendField
        declared in view so the 'extra' parameter can be different for
        Add and Edit.
        """
        context = super(AddFormView, self).get_context_data(**kwargs)
        FormLegendFormFormSet = inlineformset_factory(
            FormLegendForm,
            FormLegendField,
            can_delete=False,
            extra=0,
            max_num=12,
            exclude=('user',)
        )
        no_websites = True
        authenticated_user = self.request.user
        fl_websites = FormLegendWebsite.objects.filter(user=authenticated_user)
        if fl_websites:
            no_websites = False
        context['no_websites'] = no_websites
        if self.request.POST:
            context['formLegendFormFormset'] = FormLegendFormFormSet(self.request.POST)
        else:
            context['formLegendFormFormset'] = FormLegendFormFormSet()
        return context

    def form_valid(self, form):
        """
        This method overrides form_valid and makes sure the
        authenticated user is bound to both the FormLegendForm and
        FormLegenField instances that are saved here.
        """
        context = self.get_context_data()
        fl_form_formset = context['formLegendFormFormset']
        if fl_form_formset.is_valid():
            fl_form_form = form.save(commit=False)
            fl_form_form.user = self.request.user
            fl_form_form.save()
            fl_field_forms = fl_form_formset.save(commit=False)
            for field_form in fl_field_forms:
                field_form.user = self.request.user
                field_form.form_id = fl_form_form.pk
                field_form.save()
            print fl_form_form.pk
            print fl_form_form
            saveDynamicFormLegendForm(self.request.user, fl_form_form)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class InstallFormView(LogInRequiredMixin, DetailView):
    """
    docs
    """
    model = FormLegendForm
    slug_field = 'form_slug'
    template_name = 'formLegend/install_fl_form.html'

    def get_context_data(self, **kwargs):
        """
        docs
        """
        context = super(InstallFormView, self).get_context_data(**kwargs)
        authenticated_user = self.request.user
        try:
            fl_form_info = DynamicFormLegendForm.objects.get(
                user=authenticated_user,
                fl_form=self.object
            )
        except DynamicFormLegendForm.DoesNotExist:
            fl_form_info = 'No information available.'
        context['fl_form_info'] = fl_form_info
        return context


class EditFormView(LogInRequiredMixin, UpdateView):
    """
    docs
    """
    model = FormLegendForm
    slug_field = 'form_slug'
    form_class = FormLegendFormForm
    template_name = 'formLegend/edit_fl_form.html'
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        """
        This method overrides get_context_data and passes
        formLegendFormFormSet so the user can edit the form. Formset for
        FormLegendForm and FormLegendField declared in view so the
        'extra' parameter can be different for Add and Edit.
        """
        context = super(EditFormView, self).get_context_data(**kwargs)
        FormLegendFormFormSet = inlineformset_factory(
            FormLegendForm,
            FormLegendField,
            extra=0,
            max_num=12,
            exclude=('user',)
        )
        if self.request.POST:
            context['formLegendFormFormset'] = FormLegendFormFormSet(self.request.POST, instance=self.object)
        else:
            context['formLegendFormFormset'] = FormLegendFormFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """
        This method overrides form_valid and makes sure the
        authenticated user is bound to both the FormLegendForm and
        FormLegenField instances that are saved here.
        """
        context = self.get_context_data()
        fl_form_formset = context['formLegendFormFormset']
        if fl_form_formset.is_valid():
            fl_form_form = form.save(commit=False)
            fl_form_form.user = self.request.user
            fl_form_form.save()
            fl_field_forms = fl_form_formset.save(commit=False)
            for field_form in fl_field_forms:
                field_form.user = self.request.user
                field_form.form_id = fl_form_form.pk
                field_form.save()
            saveDynamicFormLegendForm(self.request.user, fl_form_form)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class DeleteFormView(LogInRequiredMixin, DeleteView):
    """
    docs
    """
    model = FormLegendForm
    slug_field = 'form_slug'
    template_name = 'formLegend/delete_fl_form.html'
    success_url = '/dashboard/'


class JSRedirectView(XFrameExemptMixin, RedirectView):
    """
    docs
    """

    def get_redirect_url(self, **kwargs):
        """
        docs
        """
        self.url = '/static/javascripts/fl.js'
        error_url = '/static/javascripts/flerr.js'
        df_key = kwargs['slug']
        df_key_tup = df_key.partition('-')
        df_user_name = df_key_tup[0]
        fl_form_id = df_key_tup[2]
        referer_url = self.request.META['HTTP_REFERER']
        try:
            user_obj = User.objects.get(username=df_user_name)
        except User.DoesNotExist:
            return error_url
        try:
            df_obj = DynamicFormLegendForm.objects.get(
                user=user_obj,
                fl_form=fl_form_id,
                form_key=df_key
            )
        except DynamicFormLegendForm.DoesNotExist:
            return error_url
        fl_form_url = df_obj.fl_form.form_url
        if referer_url == fl_form_url:
            return self.url
        else:
            return error_url


class FormLegendProviderView(XFrameExemptMixin, CreateView):
    """
    docs
    """
    model = FormLegendFormData
    form_class = FormLegendFormDataForm
    template_name = 'formLegend/form_provider.html'
    success_url = '/provider/success-url/'

    def get_context_data(self, **kwargs):
        """
        docs
        """
        context = super(FormLegendProviderView, self).get_context_data(**kwargs)
        df_slug = self.request.path.partition('/provider/')
        df_key = df_slug[2][:-1]
        df_key_tup = df_key.partition('-')
        df_user_name = df_key_tup[0]
        fl_form_id = df_key_tup[2]
        if fl_form_id == 'url':
            print 'form submission successful'
            # need to handle for result being emailed
            context['success'] = 'Form submission success'
            return context
        else:
            try:
                user_obj = User.objects.get(username=df_user_name)
                context['user_obj'] = user_obj
            except User.DoesNotExist:
                context['fl_error'] = 'User does not exist'
            try:
                df_obj = DynamicFormLegendForm.objects.get(
                    user=user_obj,
                    fl_form=fl_form_id,
                    form_key=df_key
                )
                context['df_obj'] = df_obj
            except:
                context['fl_error'] = 'Form does not exist'
            return context

    def form_valid(self, form):
        """
        docs
        """
        context = self.get_context_data()
        user_obj = context['user_obj']
        user_form = form.save(commit=False)
        user_form.user = user_obj
        df_obj = context['df_obj']
        user_form.fl_form = df_obj
        user_form.save()
        print 'form submission saved'
            # need to handle for result being emailed
        return super(FormLegendProviderView, self).form_valid(form)
