from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppPagesConfig(AppConfig):
    name = 'app_pages'
    verbose_name = _('pages')
