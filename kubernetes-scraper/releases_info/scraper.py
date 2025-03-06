import re
from .config import *
from .constants import *  # добавляем импорт констант
__all__ = [
    "get_unique_images_from_pods",
    "concat_images_to_str",
    "save_str_to_file",
    "create_or_update_configmap",
    "create_or_update_configmap_from_file",
    
    "get_all_images",
    "get_unique_images",
    "get_unique_dockerhub_images",
]

def get_unique_images_from_pods():
    unique_images = {}

    pod_list = v1.list_pod_for_all_namespaces(watch=False)
    print(f"## total pods: {len(pod_list.items)}")

    unique_images = set()

    repository_list = ["ghcr.io", "docker.io", "registry.k8s.io", "quay.io"]

    for pod in pod_list.items:
        for container in pod.spec.containers:
            ic(container.image)
            # if image in Pod not known - we add default docker.io prefix
            if not re.match(r"^(" + "|".join(repository_list) + ")/", container.image):
                ic(f"Modify to default: {container.image} -> docker.io/{container.image}")
                image = f"docker.io/{container.image}"
            else:
                image = container.image
            # sometimes we can find Pod with image like 'nginx'
            # need to add 'latest' tag for that (or throw an exception idk)
            if ":" not in image:
                image = f"{image}:latest"
            unique_images.add(image)
    return unique_images


def concat_images_to_str(images):
    result = ""
    for image in images:
        result += f"{image}\n"
    ic(type(result))
    return result


def save_str_to_file(data: str, filename: str) -> None:
    try:
        with open(filename, "w") as f:
            f.write(data)
    except IOError:
        print(f"Error write to file: [{filename}]")


def create_or_update_configmap(configmap_name: str, configmap_data, namespace: str) -> None:
    api = client.CoreV1Api()

    body = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": configmap_name,
        },
        "data": configmap_data,
    }

    try:
        api.create_namespaced_config_map(namespace=namespace, body=body)
        print(f"ConfigMap '{configmap_name}' created.")
    except client.exceptions.ApiException as e:
        if e.status == 409:  # ConfigMap already exists, update it
            try:
                api.patch_namespaced_config_map(
                    name=configmap_name, namespace=namespace, body=body
                )
                print(f"ConfigMap '{configmap_name}' updated.")
            except client.exceptions.ApiException as e:
                print(f"Failed to update ConfigMap '{configmap_name}': {e}")
        else:
            print(f"Failed to create or update ConfigMap '{configmap_name}': {e}")


def create_or_update_configmap_from_file(configmap_name, filename, namespace=NAMESPACE):
    try:
        with open(filename, "r") as f:
            configmap_data = {filename: f.read()}
            create_or_update_configmap(configmap_name, configmap_data, namespace)
    except IOError:
        print(f"Error reading file: '{filename}'")


# def save_configmap_from_data(configmap_name, data, namespace='default'):
#     create_or_update_configmap(configmap_name, data, namespace)

# data = {
#     'key1': 'value1',
#     'key2': 'value2'
# }
# configmap_name = 'scraper-configmap-2'
# save_configmap_from_data(configmap_name, data, namespace='default')

# curl -G 'http://prometheus-operated.default.svc.cluster.local:9090/api/v1/query' --data-urlencode 'query=count by (container, image) (kube_pod_container_info)' | jq

from prometheus_api_client import PrometheusConnect
import json
import requests
from .types import Any, List, Dict
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def query_prometheus(prometheus_url: str, query: str) -> Dict[str, Any]:
    try:
        response = requests.get(
            url=f"{prometheus_url}/api/v1/query",
            params={"query": query},
            verify=False,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return {}


def get_all_images(prometheus_url: str) -> List[str]:
    """
    Get list of images from Prometheus.

    Args:
        prometheus_url: Base URL of Prometheus server with port (e.g., "http://localhost:9090")

    Returns:
        List[str]: List of image names
    """
    query = "count by (container, image) (kube_pod_container_info)"
    result = query_prometheus(prometheus_url, query)

    images = []
    if result and "data" in result and "result" in result["data"]:
        for metric in result["data"]["result"]:
            if "metric" in metric and "image" in metric["metric"]:
                images.append(metric["metric"]["image"])

    return images

def get_unique_images(prometheus_url: str) -> List[str]:
    return list(set(get_all_images(prometheus_url)))

def get_unique_dockerhub_images(prometheus_url: str) -> List[str]:
    return list(set([img for img in get_all_images(prometheus_url) if img.startswith("docker.io/")]))
