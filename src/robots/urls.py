from django.urls import path

from robots.views import add_robot_controller

urlpatterns = [
    path("robots/", add_robot_controller, name="add_robot"),
]
