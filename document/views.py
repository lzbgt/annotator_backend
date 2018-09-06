from document import models
from rest_framework import generics
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

# placeholders
class ListDocument(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = models.DocumentSerializer
    filter_backends = (OrderingFilter,DjangoFilterBackend)

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
    filter_backends = (OrderingFilter,DjangoFilterBackend)

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


# bulk apis

class BulkDeleteSerializer(serializers.Serializer):
    """Your Custom Serializer"""
    # Gets a list of Integers
    ids = serializers.ListField(child=serializers.IntegerField())


# post: {'ids': [1,2,3]}
@api_view(['POST'])
def BulkDocumentDelete(request):
    try:
        docs_serializer = BulkDeleteSerializer(data=request.data)
        docs_serializer.is_valid(raise_exception=True)
        doc_ids = docs_serializer.data['ids']

        docs = models.Document.objects.filter(pk__in=doc_ids)
        docs._raw_delete(docs.db)
        return Response(status=204)
    except Exception as e:
        return Response({'code':500, 'msg': '{}'.format(e)}, status=500)

@api_view(['POST'])
def BulkAnnotationDelete(request):
    try:
        docs_serializer = BulkDeleteSerializer(data=request.data)
        docs_serializer.is_valid(raise_exception=True)
        doc_ids = docs_serializer.data['ids']

        docs = models.Annotation.objects.filter(pk__in=doc_ids)
        docs._raw_delete(docs.db)
        return Response(status=204)
    except Exception as e:
        return Response({'code':500, 'msg': '{}'.format(e)}, status=500)


# post: {'annos':[{doc_id, 2, 4, -1}, ]}
@api_view(['POST'])
def BulkAnnotationAdd(request):
    MAX_BULK_SIZE = 100
    annos=request.data.get('annos')
    if not annos:
        return Response({'code': 400, 'msg': ''})
    sz = len(annos)
    if sz > MAX_BULK_SIZE or sz == 0:
        return Response({'code': 400, 'msg': 'invalid size: {}, must in range (0, {})'.format(sz, MAX_BULK_SIZE)}, status=400)

    try:
        objs = [models.Annotation(doc=models.Document.objects.get(id=e['doc']), pos_x = e['pos_x'], pos_y=e['pos_y'], value=e['value'],id=e.get('id')) for e in annos]
    except Exception as e:
        return Response({'code': 400, 'msg': '{}'.format(e)})

    update = []
    create = []
    for o in objs:
        if o.id is None:
            create.append(o)
        else:
            update.append(o)

    try:
        models.Annotation.objects.bulk_create(create)
        for u in update:
            u.save()
        return Response({'code':200, 'msg':''}, status=200)
    except Exception as e:
        return Response({'code': 400, 'msg': '{}'.format(e)})

