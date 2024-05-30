from django.urls import include, path

from rest_framework import routers

from apps.academy.views.student_view import StudentViewSet

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]
