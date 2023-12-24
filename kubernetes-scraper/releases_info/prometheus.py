from prometheus_client import Info
from .kubernetes_auth import *
import releases_info.constants as const
from .setup import ic


# Creating a metric with specified labels
image_versions = Info(
    "kubernetes_image_versions", "Current image versions", ["image_name"]
)


def generate_metrics(images):
    for image in images:
        image_name, image_version = image.rsplit(":", 1)
        image_versions.labels(image_name=image_name).info({"version": image_version})


def read_configmap(configmap_name, namespace=const.NAMESPACE):
    try:
        config_map = v1.read_namespaced_config_map(
            name=configmap_name, namespace=namespace
        )
        ic(config_map.data['versions'])

    except:
    # todo add except processing
        print(f"Failed to read ConfigMap '{configmap_name}'")
