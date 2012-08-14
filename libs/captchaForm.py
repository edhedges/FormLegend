from captcha.fields import CaptchaField
from registration.backends.default import DefaultBackend
from registration.forms import RegistrationFormUniqueEmail


class CaptchaRegistrationForm(RegistrationFormUniqueEmail):
    captcha = CaptchaField(label="Are you human?")


class CaptchaRegistrationBackend(DefaultBackend):
    def get_form_class(self, request):
        return CaptchaRegistrationForm
