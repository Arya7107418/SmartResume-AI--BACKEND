
from django.contrib import admin
from .models import UserProfile, Resume, Job, JobMatch
from .admin_sites import smart_resume_admin_site


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('location',)


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_date', 'is_active')
    list_filter = ('is_active', 'posted_date', 'source', 'location')
    search_fields = ('title', 'company', 'description', 'requirements')
    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected jobs as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected jobs as inactive"


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at', 'get_skills_count')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username', 'parsed_text')
    readonly_fields = ('parsed_text', 'skills', 'experience', 'education')
    actions = ['reprocess_resumes', 'export_as_csv']

    def get_skills_count(self, obj):
        return len(obj.skills) if obj.skills else 0
    get_skills_count.short_description = 'Skills Count'

    def reprocess_resumes(self, request, queryset):
        for resume in queryset:
            # process_resume(resume.id)
            pass
        self.message_user(request, f"{queryset.count()} resumes queued for reprocessing.")
    reprocess_resumes.short_description = "Reprocess selected resumes"

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="resumes.csv"'

        writer = csv.writer(response)
        writer.writerow(['User', 'Upload Date', 'Skills Count'])

        for resume in queryset:
            writer.writerow([
                resume.user.username,
                resume.uploaded_at,
                len(resume.skills) if resume.skills else 0
            ])
        return response
    export_as_csv.short_description = "Export selected resumes as CSV"


class MatchScoreListFilter(admin.SimpleListFilter):
    title = 'match score'
    parameter_name = 'match_score'

    def lookups(self, request, model_admin):
        return (
            ('90-100', '90% - 100%'),
            ('80-90', '80% - 90%'),
            ('70-80', '70% - 80%'),
            ('50-70', '50% - 70%'),
            ('0-50', 'Below 50%'),
        )

    def queryset(self, request, queryset):
        if self.value() == '90-100':
            return queryset.filter(match_score__gte=90, match_score__lte=100)
        if self.value() == '80-90':
            return queryset.filter(match_score__gte=80, match_score__lt=90)
        if self.value() == '70-80':
            return queryset.filter(match_score__gte=70, match_score__lt=80)
        if self.value() == '50-70':
            return queryset.filter(match_score__gte=50, match_score__lt=70)
        if self.value() == '0-50':
            return queryset.filter(match_score__lt=50)


class JobMatchAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'match_score', 'created_at')
    list_filter = ('created_at', MatchScoreListFilter)
    search_fields = ('user__username', 'job__title', 'job__company')


# Register with custom admin site
smart_resume_admin_site.register(UserProfile, UserProfileAdmin)
smart_resume_admin_site.register(Resume, ResumeAdmin)
smart_resume_admin_site.register(Job, JobAdmin)
smart_resume_admin_site.register(JobMatch, JobMatchAdmin)

# Register with default admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobMatch, JobMatchAdmin)
