from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from .serializers import HeroSerializer
from .models import Hero


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer


class TestAPI(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'api under construction',
            'test': 'send request to /test for testing'
        }
        return Response(content)
