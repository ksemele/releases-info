# from releases_info import *


# # ic(constants.CONFIG_NAME)
# # scraper.elda()
# # # r.scraper.elda()

# unique_images = scraper.get_unique_images()
# # ic(unique_images) ## todo

# config_yaml = scraper.generate_config_yaml(unique_images=unique_images)
# filename = "config.yaml"
# scraper.save_data_to_file(config_yaml, filename)

# # filename = 'config.yaml'
# configmap_name = "scraper-configmap"
# create_or_update_configmap_from_file(configmap_name, filename, namespace="default")

# configmap_data = fetch_configmap(configmap_name=CONFIGMAP_NAME, namespace=NAMESPACE, key=filename)
# # items = v1.list_namespaced_config_map(
# #         namespace="default",
# #         pretty="true")
# ic(configmap_data)


# Example of running Prometheus http server with base metrics
from prometheus_client import Info
import random
import time

# Creating a metric with specified labels
image_versions = Info(
    "kubernetes_image_versions", "Current image versions", ["image_name"]
)

images = [
    "registry.k8s.io/etcd:3.5.7-0",
    "docker.io/nginx:latest",
    "ghcr.io/fluxcd/kustomize-controller:v1.1.1",
]

for image in images:
    image_name, image_version = image.rsplit(":", 1)

    # # Setting metric values
    image_versions.labels(image_name=image_name).info({"version": image_version})

from prometheus_client import start_http_server

if __name__ == "__main__":
    PROMETHEUS_PORT = 8000
    print(
        f"Start http server with Prometheus metrics: http://localhost:{PROMETHEUS_PORT}"
    )
    start_http_server(PROMETHEUS_PORT)
    while True:
        time.sleep(100)
