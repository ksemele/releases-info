from os import name
from releases_info import *


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

# configmap_data = fetch_configmap_key(configmap_name=CONFIGMAP_NAME, namespace=NAMESPACE, key=filename)
# # items = v1.list_namespaced_config_map(
# #         namespace="default",
# #         pretty="true")
# ic(configmap_data)


# images = [  # placeholder
#     "registry.k8s.io/etcd:3.5.7-0",
#     "docker.io/nginx:latest",
#     "ghcr.io/fluxcd/kustomize-controller:v1.1.1",
# ]

if __name__ == "__main__":
    unique_images = get_unique_images_from_pods()
    ic(unique_images)
    all_images = concat_images_to_str(images=unique_images)
    configmap_data = {"versions": all_images}
    create_or_update_configmap(
        configmap_name=CONFIGMAP_NAME, configmap_data=configmap_data, namespace=NAMESPACE
    )
    save_str_to_file(data=all_images,filename='config.yaml')

    generate_metrics(unique_images)
    versions = fetch_configmap_key(configmap_name=CONFIGMAP_NAME, namespace=NAMESPACE, key="versions")
    # ic(versions)
    print(
        f"Start http server with Prometheus metrics: http://localhost:{PROMETHEUS_PORT}"
    )
    start_http_server(PROMETHEUS_PORT)
    while True:
        time.sleep(100)
        exit(0)
