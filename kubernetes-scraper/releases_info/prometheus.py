# from prometheus_client import Info
# from .kubernetes import *
from .config import *


# Creating a metric with specified labels
image_versions = Info(
    "kubernetes_image_versions", "Current image versions", ["image_name"]
)


def generate_metrics(images):
    for image in images:
        image_name, image_version = image.rsplit(":", 1)
        image_versions.labels(image_name=image_name).info({"version": image_version})
