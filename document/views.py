from document import models
from rest_framework import generics

# placeholders
class ListDocument(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = models.DocumentSerializer

    # def perform_create(self, serializer):
    #     project = models.Project.objects.get(id=serializer._kwargs['data'].get('project_id', ''))
    #     serializer.save(project = project)

class DetailDocument(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Document.objects.all()
    serializer_class = models.DocumentSerializer
    def get_object(self):
        return self.queryset.get(id=self.kwargs['doc_id'])

class ListAnnotation(generics.ListCreateAPIView):
    queryset = models.Annotation.objects.all()
    serializer_class = models.AnnotationSerializer

class DetailAnnotation(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Annotation.objects.all()
    serializer_class = models.AnnotationSerializer

    def get_object(self):
        return self.queryset.filter.get(id=self.kwargs['id'])

# real functional view functions
class ListDocumentByProject(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = models.DocumentSerializer

    def get_queryset(self):
        return self.queryset.filter(project_id = self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = models.Project.objects.get(id = self.kwargs['project_id'])
        serializer.save(project = project)

class DetailDocumentByProject(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Document.objects.all()
    serializer_class = models.DocumentSerializer

    def get_object(self):
        project_id = self.kwargs['project_id']
        doc_id = self.kwargs['doc_id']
        return self.queryset.get(project_id = project_id, pk=doc_id)
    def pre_save(self, obj):
        obj.project_id = self.kwargs['project_id']

class ListAnnotationByDocument(generics.ListCreateAPIView):
    queryset = models.Annotation.objects.all()
    serializer_class = models.AnnotationSerializer

    def get_queryset(self):
        return self.queryset.filter(doc_id = self.kwargs['doc_id'])

    def perform_create(self, serializer):
        doc = models.Document.objects.get(id = self.kwargs['doc_id'])
        serializer.save(doc=doc)

class DetailAnnotationByDocument(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Annotation.objects.all()
    serializer_class = models.AnnotationSerializer

    def get_object(self):
        return self.queryset.get(doc_id = self.kwargs['doc_id'],  id = self.kwargs['id'])
    def pre_save(self, obj):
        obj.doc_id = self.kwargs['doc_id']

