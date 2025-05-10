from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.views import KnowledgeBaseViewSet, QueryRequestViewSet
from rest_framework import routers


# Create a router and register our viewsets with it
router = routers.SimpleRouter()
router.register(r"knowledge-base", KnowledgeBaseViewSet, basename="knowledge-base")
router.register(r"query-request", QueryRequestViewSet, basename="query-request")

# The API URLs are determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]
