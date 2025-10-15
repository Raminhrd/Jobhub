from django.shortcuts import render
from recruitment.models import *
from recruitment.serializer import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone


class JobPositionCreateListApiView(ListCreateAPIView):
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
        

class JobPositionRetrieveApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer    


class CandidateCreateListApiView(ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [AllowAny()]
    

class CandidateRetrieveApiView(RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Candidate.objects.all()
        return Candidate.objects.filter(user=self.request.user)
    

class AddToJobBasketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        user = request.user

        candidate = Candidate.objects.filter(user=user).first()
        if not candidate:
            return Response({"error": "Candidate profile not found."})

        job = JobPosition.objects.filter(id=job_id).first()
        if not job:
            return Response({"error": "This job does not exist."})

        if not job.is_open:
            return Response({"error": "Registration for this job is closed or full."})
        
        if job.remaining_capacity <= 0:
            return Response({"error": "This job has no remaining capacity."})

        basket = JobBasket.objects.filter(candidate__user=user).first()

        if basket:
            time_diff = timezone.now() - basket.created_at

            if time_diff > timedelta(hours=24):
                return Response({"error": "You can no longer change your job after 24 hours."})
            
            basket.job = job
            basket.created_at = timezone.now()
            basket.save()

            candidate.job = job
            candidate.save()

            return Response({"message": "Your job has been successfully changed to ."})
        
        JobBasket.objects.create(candidate=candidate, job=job)
        job.decrease_capacity()
        return Response({"message": " added to your basket."})
    

class JobBasketList(ListAPIView):
    serializer_class = JobBasketListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return JobBasket.objects.all()
        return JobBasket.objects.filter(candidate__user=user)
    

class AutoCategorizeCandidatesView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, job_id):
        try:
            job = JobPosition.objects.get(id=job_id)
            candidates = Candidate.objects.filter(job=job).order_by('-gpa')

            if not candidates.exists():
                return Response({"error": "No candidates found for this job."})

            category_number = 1
            for candidate in candidates:
                candidate.category = category_number
                candidate.save()
                category_number = 1 if category_number == 3 else category_number + 1

            return Response({"message": f"Candidates have been categorized successfully."})
        
        except JobPosition.DoesNotExist:
            return Response({"error": "Job not found."})
        

class CandidateGroupedListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, job_id):
        try:
            job = JobPosition.objects.get(id=job_id)
            grouped = {}

            for i in range(1, 4):
                grouped[f"Category {i}"] = list(
                    Candidate.objects.filter(job=job, category=i)
                    .order_by('-gpa')
                    .values('first_name', 'last_name', 'education_level', 'gpa'))

            return Response({"job": job.title,"total_candidates": Candidate.objects.filter(job=job).count(),"groups": grouped})

        except JobPosition.DoesNotExist:
            return Response({"error": "Job not found."})
