from project import models
from rest_framework import generics

class ListProject(generics.ListCreateAPIView):
    queryset = models.Project.objects.all()
    serializer_class = models.ProjectSerializer

class DetailProject(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Project.objects.all()
    serializer_class = models.ProjectSerializer