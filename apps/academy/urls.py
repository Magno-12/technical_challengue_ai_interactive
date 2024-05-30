from django.urls import include, path

from rest_framework import routers

from apps.academy.views.student_view import StudentViewSet
from apps.academy.views.application_view import ApplicationViewSet

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet, basename='student')
router.register(r'application', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
