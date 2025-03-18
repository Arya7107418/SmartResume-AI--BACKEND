from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
from resume_analyzer.admin_sites import smart_resume_admin_site
from django.contrib import admin

# DRF router setup
router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'resumes', views.ResumeViewSet, basename='resume')
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'matches', views.JobMatchViewSet, basename='match')

urlpatterns = [
    path('admin/', admin.site.urls),  # Default Django admin
    path('dashboard/', smart_resume_admin_site.urls),  # Custom admin site
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('upload-resume/', views.upload_resume, name='upload-resume'),
    path('matched-jobs/', views.get_matched_jobs, name='matched-jobs'),
    path('analyze-resume', views.analyze_resume, name='analyze-resume'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
