from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppLibraryConfig(AppConfig):
    name = 'app_library'
    verbose_name = _('library')
