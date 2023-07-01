import os
import requests
import sys
from datetime import datetime


docker_hub_registry = "https://hub.docker.com"
# docker_hub_repository = "library/nginx"

token = os.environ["DOCKER_PASSWORD"]

version_tag = "stable-alpine3.17"
# version_tag = "latest"
number_of_load_tags = 100 # 100 is max for free API

# response = requests.get(f"{docker_hub_registry}/v2/repositories/{docker_hub_repository}/tags?ordering=last_updated&page_size={number_of_load_tags}", headers={"Authorization": f"Bearer {token}"})

# current_tag_found = False
# tags = response.json()["results"]
# formatted_tags = [{"name": tag["name"], "last_updated": datetime.strptime(tag["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")} for tag in tags]
# for tag in formatted_tags:
#     if tag['name'] == version_tag:
#         print(f"{tag['name']}\t{tag['last_updated']} <- current tag")
#         current_tag_found = True
#         break
#     else:
#         print(f"{tag['name']}\t{tag['last_updated']}")

# if current_tag_found == False:
#     print(f'Tag [{version_tag}] not found in last [{number_of_load_tags}] tags')

## config reader
import yaml


def fetch_config_yaml(file_path):
    """Fetch config.yaml."""
    with open(file_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as e:
            print(f"Error while reading YAML file: {e}")
            return None



def _fetch_all_releases(docker_hub_repository) -> dict:
    print(docker_hub_repository)
    url_releases = f"{docker_hub_registry}/v2/repositories/{docker_hub_repository}/tags?ordering=last_updated&page_size={number_of_load_tags}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url_releases, headers=headers)
        if response.status_code == 404:
            print(f'[{docker_hub_repository}] is not found in {docker_hub_registry}')
            return None
    except response.Error as e:
        print(f'ERROR in _fetch_all_releases(): {e}')
        return None

    return response.json()


def _dockerhub_date_format(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y")


def _tag_exist_in_releases(tag, releases):
    # print(releases)
    tag_found = False
    tags = releases["results"]
    formatted_tags = [{"name": t["name"], "last_updated": _dockerhub_date_format(t["last_updated"])} for t in tags]

    # for item in releases["results"]:
    #     images = item['name']
    #     digest = item['digest']
    #     print("Images:", images)
    #     print("Digest:", digest)
    #     print("---")
    # last_release_date = formatted_tags[0]['last_updated']

    for t in formatted_tags:
        if t['name'] == tag:
            print(f"{t['name']}\t{t['last_updated']} <- current tag")
            tag_found = True
            break
        else:
            # print(f"{t['name']}\t{t['last_updated']}")
            pass
    if tag_found == False:
        print(f"[{tag}] NOT FOUND in last [{len(releases['results'])}] releases.")
    return tag_found



def _days_of_missed_releases(current_tag_date, latest_tag_date):
    try:
        # latest_tag_date = _(latest_tag_date, "%d.%m.%Y")
        # current_tag_date = datetime.datetime.strptime(current_tag_date, "%d.%m.%Y")
        days_delta = (latest_tag_date - current_tag_date).days
    except TypeError:
        days_delta = "unidentified"
    except ValueError:
        days_delta = "unidentified"
    return days_delta


def _number_of_missed_releases(all_releses, current_tag):
    pass

config = fetch_config_yaml('config.yaml')
if config:
    services = config.get('services', {})
    service_list = [{'name': service, 'details': details} for service, details in services.items()]
    dockerhub_list = [{'name': service, 'details': details} for service, details in services.items() if 'dockerhub' in details]  # todo
    # registry_list = [{'name': service, 'details': details} for service, details in services.items() if 'registry' in details]
    
    print("")
    print("Service List:")
    for service in service_list:
        # print(f"- Name: {service['name']}")
        # print(f"  Details: {service['details']}")
        # print()
        repo = f"{service['details']['dockerhub']['owner']}/{service['details']['dockerhub']['repo']}"
        # try:
            # _fetch_all_releases(docker_hub_repository=repo)
        # except:
            # print("error in _fetch")
        service_releases = _fetch_all_releases(docker_hub_repository=repo)
        print(f"SEARCH: [{service['details']['version']}]")
        
        if service_releases:
            latest_tag_date = _dockerhub_date_format(service_releases['results'][0]['last_updated'])

            if _tag_exist_in_releases(tag=service['details']['version'],releases=service_releases):
                current_tag_date = service_releases.get(service['details']['version'])
                days_of_missed_releases = _days_of_missed_releases(current_tag_date=current_tag_date,latest_tag_date=latest_tag_date)
                print(f"{current_tag_date} {latest_tag_date} DAYS: {days_of_missed_releases}")
                pass

    # print("\nDockerhub List:")
    # for service in dockerhub_list:
    #     print(f"- Name: {service['name']}")
    #     print(f"  Details: {service['details']}")
    #     print()
