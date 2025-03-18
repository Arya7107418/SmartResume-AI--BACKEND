from django.shortcuts import render

# Create your views here.
# resume_analyzer/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserProfile, Resume, Job, JobMatch
from .serializers import UserProfileSerializer, ResumeSerializer, JobSerializer, JobMatchSerializer
from django.contrib.auth.models import User

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        # Here you would call a function to process the resume
        # process_resume(resume.id)

class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobMatchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return JobMatch.objects.filter(user=self.request.user).order_by('-match_score')

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdminUser]  # Only admin can manage jobs directly

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_resume(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    # Create resume
    resume = Resume.objects.create(
        user=request.user,
        file=file
    )
    
    # Process resume (this would be a background task)
    # process_resume(resume.id)
    
    return Response({'message': 'Resume uploaded successfully', 'id': resume.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_matched_jobs(request):
    matches = JobMatch.objects.filter(user=request.user).order_by('-match_score')
    serializer = JobMatchSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    user_count = User.objects.count()
    resume_count = Resume.objects.count()
    job_count = Job.objects.count()
    match_count = JobMatch.objects.count()
    
    return Response({
        'user_count': user_count,
        'resume_count': resume_count,
        'job_count': job_count,
        'match_count': match_count
    })

# views.py (add this at bottom)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt  # Testing ke liye, production me use mat karna
def analyze_resume(request):
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        if resume:
            # Resume processing logic yahaan aayega
            return JsonResponse({
                "message": "Resume received successfully!",
                "filename": resume.name
            })
        return JsonResponse({"error": "No resume uploaded"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)
