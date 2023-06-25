import os
import requests
import sys
from datetime import datetime


docker_hub_registry = "https://hub.docker.com"
docker_hub_repository = "library/nginx"
# docker_hub_repository = "nginx"

token = os.environ["DOCKER_PASSWORD"]

version_tag = "stable-alpine3.17"
# version_tag = "latest"
number_of_load_tags = 100 # 100 is max for free API

response = requests.get(f"{docker_hub_registry}/v2/repositories/{docker_hub_repository}/tags?ordering=last_updated&page_size={number_of_load_tags}", headers={"Authorization": f"Bearer {token}"})

current_tag_found = False
tags = response.json()["results"]
formatted_tags = [{"name": tag["name"], "last_updated": datetime.strptime(tag["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")} for tag in tags]
for tag in formatted_tags:
    if tag['name'] == version_tag:
        print(f"{tag['name']}\t{tag['last_updated']} <- current tag")
        current_tag_found = True
        break
    else:
        print(f"{tag['name']}\t{tag['last_updated']}")

if current_tag_found == False:
    print(f'Tag [{version_tag}] not found in last [{number_of_load_tags}] tags')