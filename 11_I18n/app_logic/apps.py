from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppLogicConfig(AppConfig):
    name = 'app_logic'
    verbose_name = _('logic')
