from django.contrib import admin
from formLegend.models import FormLegendWebsite, FormLegendForm,\
    FormLegendField, DynamicFormLegendForm

admin.site.register(FormLegendWebsite)
admin.site.register(FormLegendForm)
admin.site.register(FormLegendField)
admin.site.register(DynamicFormLegendForm)
