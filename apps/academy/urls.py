from django.urls import include, path

from rest_framework import routers

from apps.academy.views.student_view import StudentViewSet
from apps.academy.views.application_view import ApplicationViewSet
from apps.academy.views.assignment_views import AssignmentViewSet

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet, basename='student')
router.register(r'application', ApplicationViewSet, basename='application')
router.register(r'assignment', AssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]
