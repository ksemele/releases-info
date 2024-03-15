import re
from .kubernetes import *
from .setup import *


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


if __name__ == "__main__":
    unique_images = get_unique_images_from_pods()
    # print(unique_images) ## todo

    config_yaml = concat_images_to_str(images=unique_images)
    print(config_yaml)
    filename = "config.yaml"
    print(f"{CONFIG_NAME}")
    save_data_to_file(config_yaml, filename)

    # filename = 'config.yaml'
    configmap_name = "scraper-configmap"
    save_configmap_from_file(configmap_name, filename, namespace="default")
