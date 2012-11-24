from django.contrib import admin
from formLegend.models import FormLegendWebsite, FormLegendForm,\
    FormLegendField, DynamicFormLegendForm, FormLegendFormData

admin.site.register(FormLegendWebsite)
admin.site.register(FormLegendForm)
admin.site.register(FormLegendField)
admin.site.register(DynamicFormLegendForm)
admin.site.register(FormLegendFormData)
