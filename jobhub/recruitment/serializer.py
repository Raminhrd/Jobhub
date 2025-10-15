from rest_framework.serializers import ModelSerializer, StringRelatedField
from recruitment.models import *


class JobPositionSerializer(ModelSerializer):
    title = StringRelatedField()
    class Meta:
        model = JobPosition
        fields = '__all__'


class CandidateSerializer(ModelSerializer):
    job = StringRelatedField()
    class Meta:
        model = Candidate
        fields = '__all__'


class JobBasketListSerializer(ModelSerializer):
    candidate = StringRelatedField()
    job = StringRelatedField ()
    class Meta:
        model = JobBasket
        fields = '__all__'