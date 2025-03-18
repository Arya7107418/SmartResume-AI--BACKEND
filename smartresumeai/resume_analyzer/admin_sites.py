# Create a new file: resume_analyzer/admin_site.py
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class SmartResumeAdminSite(AdminSite):
    site_title = _('SmartResumeAI Admin')
    site_header = _('SmartResumeAI Administration')
    index_title = _('Dashboard')

smart_resume_admin_site = SmartResumeAdminSite(name='smartresume_admin')