# from os import name
# from releases_info import *


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

from releases_info import scraper
# main.py
import asyncio
from releases_info.services.processor import ImageProcessor
from icecream import ic


async def main():
    images = scraper.get_all_images(prometheus_url=prometheus_url)
    # ic(images, len(images))
    unique_images = scraper.get_unique_images(prometheus_url=prometheus_url)
    # ic(unique_images, len(unique_images))
    dockerhub_images = scraper.get_unique_dockerhub_images(
        prometheus_url=prometheus_url
    )
    dockerhub_images = [
        "docker.io/kindest/kindnetd:v20241212-9f82dd49",
        "docker.io/rabbitmq:3.13.0", # library image
        "docker.io/rabbitmq:14.0.0", # invalid tag
    ]
    processor = ImageProcessor()
    await processor.process_images(dockerhub_images)

    ic(processor._processed_images)
    # ic(processor.get_successful_images())

if __name__ == "__main__":
    prometheus_host = "http://prometheus-operated.default.svc.cluster.local"
    prometheus_host = "http://localhost"
    prometheus_port = 9090
    prometheus_url = f"{prometheus_host}:{prometheus_port}"
    # main()
    asyncio.run(main())
