from rest_framework import viewsets, authentication, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from boards.models import Board
from .serializers import HeroSerializer, BoardSerializer
from .models import Hero


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer


class BoardViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]

    queryset = Board.objects.all().order_by('id')
    serializer_class = BoardSerializer


class TestAPI(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'beta, admin access only',
            'test': 'send request to /test for testing'
        }
        return Response(content)
