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
            return Response({"message": "Your job has been successfully changed to ."})
        
        JobBasket.objects.create(candidate=candidate, job=job)
        return Response({"message": " added to your basket."})
    

class JobBasketList(ListAPIView):
    serializer_class = JobBasketListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return JobBasket.objects.all()
        return JobBasket.objects.filter(candidate__user=user)