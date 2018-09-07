"""annotator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from document import views as dviews
from project import views as pviews
from . import views as views
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='文本标注系统在线API文档', public=False)),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/project/', pviews.ListProject.as_view(), name='project-list'),
    path('api/project/<int:pk>/', pviews.DetailProject.as_view(), name='project-detail'),
    path('api/project/<int:project_id>/document/', dviews.ListDocumentByProject.as_view(), name='doc-by-proj'),
    path('api/project/<int:project_id>/document/<int:doc_id>', dviews.DetailDocumentByProject.as_view()),
    path('api/document/', dviews.ListDocument.as_view()),
    path('api/document/<int:doc_id>', dviews.DetailDocument.as_view()),
    path('api/document/<int:doc_id>/annotation/', dviews.ListAnnotationByDocument.as_view(), name='anno-by-doc'),
    path('api/document/<int:doc_id>/annotation/<int:id>', dviews.DetailAnnotationByDocument.as_view()),
    path('api/annotation/', dviews.ListAnnotation.as_view()),
    path('api/annotation/<int:id>', dviews.DetailAnnotation.as_view()),
    path('api/tasks/', views.tasks, name="tasks"),
    path('api/document_bulk_del/', dviews.BulkDocumentDelete),
    path('api/document_bulk_ready/', dviews.BulkDocumentReady),
    path('api/annotation_bulk_del/', dviews.BulkAnnotationDelete),
    path('api/annotation_bulk_new/', dviews.BulkAnnotationAdd),
]
