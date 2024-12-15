from django.urls import path

from robots.views import (
    add_robot_controller,
    download_view,
    load_robots_info_controller,
)

urlpatterns = [
    path("", add_robot_controller, name="add_robot"),
    path("info/", load_robots_info_controller, name="save_robots_info"),
    path("download/<path:file_path>/", download_view, name="download_robots_info_file"),
]
