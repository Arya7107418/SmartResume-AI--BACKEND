# resume_analyzer/dashboard.py
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Avg
from django.urls import reverse
from admin_tools.dashboard import modules, Dashboard
from .models import Resume, Job, JobMatch, UserProfile

class SmartResumeDashboard(Dashboard):
    def init_with_context(self, context):
        # Add stats module
        self.children.append(modules.DashboardModule(
            title=_('System Statistics'),
            pre_content='''
            <div class="dashboard-stats">
                <div class="stat-box">
                    <h3>Users</h3>
                    <p class="big-number">%s</p>
                </div>
                <div class="stat-box">
                    <h3>Resumes</h3>
                    <p class="big-number">%s</p>
                </div>
                <div class="stat-box">
                    <h3>Jobs</h3>
                    <p class="big-number">%s</p>
                </div>
                <div class="stat-box">
                    <h3>Avg Match</h3>
                    <p class="big-number">%s%%</p>
                </div>
            </div>
            ''' % (
                UserProfile.objects.count(),
                Resume.objects.count(),
                Job.objects.count(),
                int(JobMatch.objects.aggregate(Avg('match_score'))['match_score__avg'] or 0)
            )
        ))
        
        # Recent activity
        self.children.append(modules.RecentActions(
            title=_('Recent Activity'),
            limit=10
        ))
        
        # Links
        self.children.append(modules.LinkList(
            title=_('Quick Links'),
            children=[
                {
                    'title': _('Resume Analysis'),
                    'url': reverse('admin:resume_analyzer_resume_changelist'),
                    'external': False,
                },
                {
                    'title': _('Job Matches'),
                    'url': reverse('admin:resume_analyzer_jobmatch_changelist'),
                    'external': False,
                },
                {
                    'title': _('User Management'),
                    'url': reverse('admin:auth_user_changelist'),
                    'external': False,
                },
            ]
        ))