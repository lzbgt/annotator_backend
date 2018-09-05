from django.db import models
from annotator.common import IntegerEnum
from rest_framework.reverse import reverse

# Create your models here.

# type definitions
class ProjectType(IntegerEnum):
    ABSA = 1
    NER = 2
    BC = 3
    MCC = 4

class DBType(IntegerEnum):
    MONGO = 1
    MYSQL = 2
#
class SortChoices(IntegerEnum):
    DESC = 1
    ASC = 2

class Project(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.IntegerField(choices=ProjectType.choices(), default=int(ProjectType.ABSA))
    dbtype = models.IntegerField(choices=DBType.choices(), default=int(DBType.MONGO))
    dburi = models.CharField(max_length=512)
    content_field = models.CharField(max_length=128)
    sort_field = models.CharField(max_length=128)
    sort_type = models.IntegerField(choices=SortChoices.choices(), default=int(SortChoices.DESC))
    limit = models.IntegerField(default=-1)
    lastid = models.IntegerField(default=1)

    class Meta:
        db_table= 'project'

    def __str__(self):
        """A string representation of the model."""
        return self.name

from rest_framework import serializers

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    docs = serializers.SerializerMethodField('get_documents')

    def get_documents(self, obj):
        return reverse('doc-by-proj',
               args=[obj.pk], request=self.context['request'])

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'type',
            'dbtype',
            'dburi',
            'content_field',
            'sort_field',
            'sort_type',
            'limit',
            'docs'
        )