from django.apps import AppConfig


class RobotsConfig(AppConfig):
    name = "robots"

    def ready(self) -> None:
        import robots.signals.inform_users_about_robot_is_ready  # noqa F401
