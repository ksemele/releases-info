import os
import requests
import sys
import yaml
from datetime import datetime
import releases_info.constants as const
from .kubernetes import *
from .setup import ic


docker_hub_registry = "https://hub.docker.com"
token = os.environ.get("DOCKER_PASSWORD")
number_of_load_tags = os.environ.get(
    "DOCKER_NUMBER_OF_LOAD_TAGS", 100
)  # 100 is max for free API


def fetch_config_yaml(file_path):
    """Fetch config.yaml."""
    with open(file_path, "r") as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as e:
            print(f"Error while reading YAML file: {e}")
            return None


def _fetch_all_releases(docker_hub_repository) -> dict:
    # print(docker_hub_repository)
    url_releases = f"{docker_hub_registry}/v2/repositories/{docker_hub_repository}/tags?ordering=last_updated&page_size={number_of_load_tags}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url_releases, headers=headers)
        if response.status_code == 404:
            print(f"[{docker_hub_repository}] is not found in {docker_hub_registry}")
            return None
    except response.Error as e:
        print(f"ERROR in _fetch_all_releases(): {e}")
        return None
    return response.json()


def _dockerhub_date_format(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y")


def _get_formatted_releases(releases):
    tags = releases["results"]
    formatted_releases = [
        {"name": t["name"], "last_updated": _dockerhub_date_format(t["last_updated"])}
        for t in tags
    ]

    return formatted_releases


def _tag_exist_in_releases(tag, releases):
    return any(t["name"] == tag for t in releases["results"])


def _days_of_missed_releases(current_tag_date, latest_tag_date):
    try:
        date_current = datetime.strptime(current_tag_date, "%d.%m.%Y")
        date_latest = datetime.strptime(latest_tag_date, "%d.%m.%Y")

        difference = date_latest - date_current
        days_delta = difference.days
    except TypeError:
        days_delta = "unidentified"
    except ValueError:
        days_delta = "unidentified"
    return days_delta


# idk how correct count this...
def _number_of_missed_releases(releases, current_tag):
    pass


# will return object or None
def _get_tag_object(tag, releases):
    return next((t for t in releases["results"] if t["name"] == tag), None)


def _get_tag_release_date(tag, releases):
    tag_release_date = None
    if _tag_exist_in_releases(tag=tag, releases=releases):
        current_tag = _get_tag_object(tag, releases)
        # tag_release_date = current_tag['last_updated']
        tag_release_date = _dockerhub_date_format(current_tag["last_updated"])
    else:
        raise ValueError(f"[{tag}] Not exist in releases")  # in last 100 releases
    return tag_release_date


def get_services_releases(services):
    # services = config.values()
    # print(services)
    # print()
    # service_list = [{'name': service, 'details': details} for service, details in services]

    # dockerhub_list = [{'name': service, 'details': details} for service, details in services.items() if 'dockerhub' in details]  # todo

    # print("")
    # print("Service List:")
    result_releases_list = {}
    for service, data in services.items():
        current_tag = data.get("version")
        dockerhub = data.get("dockerhub")
        repo = (
            f"{data.get('dockerhub').get('owner')}/{data.get('dockerhub').get('repo')}"
        )
        service_releases = _fetch_all_releases(docker_hub_repository=repo)
        if service_releases:
            # I use first elem of list because I get tags sorted in _fetch_all_releases()
            # Maybe 'latest' will be more correct
            latest_tag_date = _dockerhub_date_format(
                service_releases["results"][0]["last_updated"]
            )

            if _tag_exist_in_releases(tag=current_tag, releases=service_releases):
                current_tag_date = _get_tag_release_date(
                    tag=current_tag, releases=service_releases
                )
                days_of_missed_releases = _days_of_missed_releases(
                    current_tag_date=current_tag_date, latest_tag_date=latest_tag_date
                )
                # print(
                #     f"{service}:{current_tag}\t{current_tag_date} -> {service_releases['results'][0]['name']}\t{latest_tag_date}\toutdated: [{days_of_missed_releases}] days"
                # )
                result_releases_list[str(f'{service}:{current_tag}')] = current_tag_date

                pass
            else:
                ic(current_tag, "Not exist")

    # ic.configureOutput(includeContext=False)
    # ic.configureOutput(prefix=f"{service}:{current_tag}\t{current_tag_date} -> {service_releases['results'][0]['name']}\t{latest_tag_date}\toutdated: [{days_of_missed_releases}] days\n")
    ic(result_releases_list)

    # print("\nDockerhub List:")
    # for service in dockerhub_list:
    #     print(f"- Name: {service['name']}")
    #     print(f"  Details: {service['details']}")
    #     print()
