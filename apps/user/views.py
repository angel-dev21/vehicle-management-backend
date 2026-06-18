from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserCreateSerializer
from backend.permissions import IsAdmin, IsSelfOrAdmin

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserCreateSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'destroy']:
            return [IsAdmin()]
        return [IsSelfOrAdmin()]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=204)
    
    