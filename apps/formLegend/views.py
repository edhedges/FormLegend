from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView,\
    DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from formLegend.models import FormLegendWebsite, FormLegendForm
from formLegend.forms import FormLegendWebsiteForm, FormLegendFormForm,\
    FormLegendFormFormSet


class LogInRequiredMixin(object):
    """
    Class view that can be inherited to require a user be logged in.
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
        authenticated_user = self.request.user
        fl_websites = FormLegendWebsite.objects.filter(user=authenticated_user)
        fl_forms = FormLegendForm.objects.filter(user=authenticated_user)
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'fl_websites': fl_websites,
            'fl_forms': fl_forms
        })
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
        to their form.
        """
        context = super(AddFormView, self).get_context_data(**kwargs)
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
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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
        formLegendFormFormSet so the user can edit the form.
        """
        context = super(EditFormView, self).get_context_data(**kwargs)
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
