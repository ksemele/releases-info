# import os
# import requests
# import sys
# import yaml
# from datetime import datetime
# from .config import *
# from .image import Image
# from .types import Any

# # https://docs.docker.com/docker-hub/api/latest/
# #
# docker_hub_registry = "https://hub.docker.com"
# token = os.environ.get("DOCKER_PASSWORD")
# number_of_load_tags = os.environ.get(
#     "DOCKER_NUMBER_OF_LOAD_TAGS", 100
# )  # 100 is max for free API


# def _fetch_all_releases(docker_hub_repository) -> dict:
#     # print(docker_hub_repository)
#     url_releases = f"{docker_hub_registry}/v2/repositories/{docker_hub_repository}/tags?ordering=last_updated&page_size={number_of_load_tags}"
#     headers = {"Authorization": f"Bearer {token}"}

#     try:
#         response = requests.get(url_releases, headers=headers)
#         if response.status_code == 404:
#             print(f"[{docker_hub_repository}] is not found in {docker_hub_registry}")
#             return None
#     except response.Error as e:
#         print(f"ERROR in _fetch_all_releases(): {e}")
#         return None
#     return response.json()


# def _dockerhub_date_format(date):
#     return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y")


# # def _get_formatted_releases(releases):
# #     tags = releases["results"]
# #     formatted_releases = [
# #         {"name": t["name"], "last_updated": _dockerhub_date_format(t["last_updated"])}
# #         for t in tags
# #     ]

# #     return formatted_releases


# def _tag_exist_in_releases(tag, releases):
#     return any(t["name"] == tag for t in releases["results"])


# def _days_of_missed_releases(current_tag_date, latest_tag_date):
#     # try:
#     #     date_current = datetime.strptime(current_tag_date, "%d.%m.%Y")
#     #     date_latest = datetime.strptime(latest_tag_date, "%d.%m.%Y")

#     #     difference = date_latest - date_current
#     #     days_delta = difference.days
#     # except TypeError:
#     #     days_delta = "unidentified"
#     # except ValueError:
#     #     days_delta = "unidentified"
#     # return days_delta
#     pass


# # idk how correct count this...
# def _number_of_missed_releases(releases, current_tag):
#     pass


# # # will return object or None
# # def _get_tag_object(tag, releases):
# #     return next((t for t in releases["results"] if t["name"] == tag), None)


# def _get_tag_release_date(tag, releases):
#     tag_release_date = None
#     # if _tag_exist_in_releases(tag=tag, releases=releases):
#     #     current_tag = _get_tag_object(tag, releases)
#     #     # tag_release_date = current_tag['last_updated']
#     #     tag_release_date = _dockerhub_date_format(current_tag["last_updated"])
#     # else:
#     #     raise ValueError(f"[{tag}] Not exist in releases")  # in last 100 releases
#     return tag_release_date


# ## WIP New funcs
# def _search_image_tag(img: Image) -> bool:
#     """
#     Check if image tag exists in repository

#     Args:
#         img: Image object to check

#     Returns:
#         bool: True if tag exists, False otherwise
#     """
#     result = img.check_repository_tag()
#     # ic(result)

#     if result["status"] == "success":
#         print(f"✅ Tag found: {img.tag} in {img.get_repository()}")
#         return True
#     else:
#         print(f"❌ {result['message']}")
#         if "response" in result:
#             print(f"   API response: {result['response']}")
#         return False


# def process_single_image(image: str) -> dict[str, Any]:
#     """Process a single docker image and return its status"""
#     try:
#         img = Image.from_string(image)
#         success = _search_image_tag(img)
#         # success = img.check_repository_tag()
#         # ic(success)
#         latest = img.list_repository_tags(page_size=3)
#         ic(latest)

#         ic(img.get_sorted_tags(tags=3))
#         ic(img.get_sorted_tags(tags=3, reverse=False))

#         return {
#             "image": img,
#             "status": "success" if success else "error",
#             "timestamp": datetime.now(),
#         }
#     except Exception as e:
#         return {
#             "image": image,
#             "status": "error",
#             "error": str(e),
#             "timestamp": datetime.now(),
#         }


# # def get_image_tag(image: str) -> list:
# #     """Get list tags for a docker image"""
# #     img = Image.from_string(image)
# #     releases = _fetch_all_releases(img.get_repository())
# #     if releases is None:
# #         return {"status": "error", "message": "Repository not found"}
# #     tags = _get_formatted_releases(releases)
# #     return {"status": "success", "tags": tags}
