# from os import name
# from releases_info import *


# # unique_images = scraper.get_unique_images()
# # # ic(unique_images) ## todo

# # config_yaml = scraper.generate_config_yaml(unique_images=unique_images)
# # filename = "config.yaml"
# # scraper.save_data_to_file(config_yaml, filename)

# # # filename = 'config.yaml'
# # configmap_name = "scraper-configmap"
# # create_or_update_configmap_from_file(configmap_name, filename, namespace="default")

# # configmap_data = fetch_configmap_key(configmap_name=CONFIGMAP_NAME, namespace=NAMESPACE, key=filename)
# # # items = v1.list_namespaced_config_map(
# # #         namespace="default",
# # #         pretty="true")
# # ic(configmap_data)


# # images = [  # placeholder
# #     "registry.k8s.io/etcd:3.5.7-0",
# #     "docker.io/nginx:latest",
# #     "ghcr.io/fluxcd/kustomize-controller:v1.1.1",
# # ]

# if __name__ == "__main__":
#     unique_images = get_unique_images_from_pods()
#     ic(unique_images)
#     all_images = concat_images_to_str(images=unique_images)
#     configmap_data = {"versions": all_images}
#     create_or_update_configmap(
#         configmap_name=CONFIGMAP_NAME, configmap_data=configmap_data, namespace=NAMESPACE
#     )
#     save_str_to_file(data=all_images,filename='config.yaml')

#     generate_metrics(unique_images)
#     versions = fetch_configmap_key(configmap_name=CONFIGMAP_NAME, namespace=NAMESPACE, key="versions")
#     # ic(versions)
#     print(
#         f"Start http server with Prometheus metrics: http://localhost:{PROMETHEUS_PORT}"
#     )
#     start_http_server(PROMETHEUS_PORT)
#     while True:
#         time.sleep(100)
#         exit(0)


# main.py
from releases_info import (
    get_all_images,
    get_unique_images_from_pods,
    create_or_update_configmap_from_file,
    NAMESPACE,
    CONFIGMAP_NAME,
    dockerhub_releases as docker,
)
from releases_info import dockerhub_releases as docker
from releases_info import scraper
from icecream import ic


def main():
    # images = scraper.get_all_images(prometheus_url="http://prometheus-operated.default.svc.cluster.local", prometheus_port=9090)
    images = scraper.get_all_images(prometheus_url=prometheus_url) # need port-forwarding
    # ic(images, len(images))

    unique_images = scraper.get_unique_images(prometheus_url=prometheus_url)
    ic(unique_images, len(unique_images))

    dockerhub_images = scraper.get_unique_dockerhub_images(prometheus_url=prometheus_url)
    dockerhub_images = [
        "docker.io/kindest/kindnetd:v20241212-9f82dd49",
        "docker.io/rabbitmq:14.0.0", # invalid tag
        "docker.io/rabbitmq:3.13.0", # library image
    ]
    ic(dockerhub_images, len(dockerhub_images))

    for image in dockerhub_images:
        result = docker.process_single_image(image)
        # ic(result)
        if result["status"] == "success":
            ic(result['image'].full_name)
        else:
            ic(result.get('error', 'Unknown error'))


if __name__ == "__main__":
    prometheus_host = "http://localhost"
    prometheus_port = 9090
    prometheus_url = f"{prometheus_host}:{prometheus_port}"
    main()
