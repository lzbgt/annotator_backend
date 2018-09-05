from django.db import models
from annotator.common import IntegerEnum
from project.models import Project
from rest_framework.reverse import reverse
# Create your models here.

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # the original id in the source database
    oid = models.CharField(max_length=64)
    # document conent
    content = models.TextField(blank=False)
    ready = models.BooleanField(default=False)

    class Meta:
        db_table = 'document'
        indexes = [models.Index(fields=['ready',])]

# auxiliary class
class AnnoValueChoice(IntegerEnum):
    POS = 1
    NEG = -1
    NEU = 0

class Annotation(models.Model):
    doc = models.ForeignKey(Document, on_delete=models.CASCADE)
    pos_x = models.PositiveIntegerField()
    pos_y = models.PositiveIntegerField()
    # this can be derived from pos_x and y, thus duplication of infomation
    # content = models.CharField(max_length=60, blank=False)
    value = models.SmallIntegerField(default=int(AnnoValueChoice.NEU), choices=AnnoValueChoice.choices())

    class Meta:
        db_table = 'annotation'
        indexes = [
            models.Index(fields=['pos_x']),
        ]

from rest_framework import serializers
class DocumentSerializer(serializers.ModelSerializer):
    annos = serializers.SerializerMethodField('get_annotations')

    def get_annotations(self, obj):
        return reverse('anno-by-doc',
               args=[obj.pk], request=self.context['request'])
    class Meta:
        model = Document
        fields = (
            'id',
            'project',
            'oid',
            'content',
            'ready',
            'annos'
        )

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'id',
            'doc',
            'pos_x',
            'pos_y',
            'value'
        )
        # extra_kwargs = {
        #     'doc': {'required': False}
        # }
