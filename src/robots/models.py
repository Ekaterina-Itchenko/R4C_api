from django.db import models


class RobotModel(models.Model):
    name = models.CharField(max_length=2, blank=False, null=False, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "models"


class RobotVersion(models.Model):
    model = models.ForeignKey(to="RobotModel", on_delete=models.CASCADE, related_name="versions")
    version = models.CharField(max_length=2, blank=False, null=False)

    class Meta:
        unique_together = ("model", "version")
        db_table = "versions"

    def __str__(self) -> str:
        return f"{self.model.name} - {self.version}"


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    version = models.ForeignKey(to="RobotVersion", on_delete=models.CASCADE, related_name="robots")
    created = models.DateTimeField(blank=False, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "robots"

    def __str__(self) -> str:
        return f"{self.version.model.name} - {self.version.version} (SN: {self.serial})"
