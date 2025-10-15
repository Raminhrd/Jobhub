from django.urls import path
from recruitment.views import *



urlpatterns = [
    path('job-list', JobPositionCreateListApiView.as_view()),
    path('job-retrieve', JobPositionRetrieveApiView.as_view()),
    path('candidate-create', CandidateCreateListApiView.as_view()),
    path('candidate-retrieve/<str:pk>', CandidateRetrieveApiView.as_view()),
    path('add-job/<str:job_id>', AddToJobBasketView.as_view()),
    path('my-job', JobBasketList.as_view()),
    path('auto-categorize/<str:job_id>/', AutoCategorizeCandidatesView.as_view()),
    path('grouped-candidates/<str:job_id>/', CandidateGroupedListView.as_view())
]