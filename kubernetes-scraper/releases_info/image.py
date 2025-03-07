# from dataclasses import dataclass
# from datetime import datetime
# import requests
# from icecream import ic
# from .types import Any


# @dataclass
# class Image:
#     full_name: str
#     registry: str
#     namespace: str
#     name: str
#     tag: str
#     docker_hub_url: str
#     docker_hub_tag_url: str
#     api_url: str

#     @classmethod
#     def from_string(cls, image_string: str) -> "Image":
#         # docker.io/kindest/kindnetd:v20241212-9f82dd49
#         # docker.io/postgres:14 -> library/postgres:14
#         parts = image_string.split("/")
#         registry = parts[0]  # docker.io
#         image_with_tag = parts[-1]  # kindnetd:v20241212-9f82dd49 or postgres:14

#         if len(parts) == 2:
#             namespace = "library"
#             name_with_tag = parts[1]
#         else:
#             namespace = parts[1]
#             name_with_tag = parts[-1]

#         name, tag = name_with_tag.split(":")

#         repository = f"{namespace}/{name}"
#         docker_hub_url = f"https://hub.docker.com/r/{repository}"
#         docker_hub_tag_url = f"{docker_hub_url}/tags?name={tag}"
#         api_url = f"https://hub.docker.com/v2/repositories/{repository}"

#         return cls(
#             full_name=image_string,
#             registry=registry,
#             namespace=namespace,
#             name=name,
#             tag=tag,
#             docker_hub_url=docker_hub_url,
#             docker_hub_tag_url=docker_hub_tag_url,
#             api_url=api_url,
#         )

#     def get_full_name(self) -> str:
#         """Get full image name including registry and tag"""
#         return self.full_name

#     def get_registry(self) -> str:
#         """Get registry domain"""
#         return self.registry

#     def get_namespace(self) -> str:
#         """Get namespace (owner or organization)"""
#         return self.namespace

#     def get_name(self) -> str:
#         """Get image name without registry and tag"""
#         return self.name

#     def get_tag(self) -> str:
#         """Get image tag"""
#         return self.tag

#     def get_repository(self) -> str:
#         """Get full repository path (namespace/name)"""
#         return f"{self.namespace}/{self.name}"

#     def get_docker_hub_url(self) -> str:
#         """Get Docker Hub web UI URL"""
#         return self.docker_hub_url

#     def get_docker_hub_tag_url(self) -> str:
#         """Get Docker Hub web UI URL for specific tag"""
#         return self.docker_hub_tag_url

#     def get_api_url(self) -> str:
#         """Get Docker Hub API base URL for this repository"""
#         return self.api_url

#     def get_api_tag_url(self) -> str:
#         """Get Docker Hub API URL for specific tag"""
#         return f"{self.api_url}/tags/{self.tag}"

#     def get_short_name(self) -> str:
#         """Get short name (repository:tag) without registry"""
#         return f"{self.get_repository()}:{self.tag}"

#     def __str__(self) -> str:
#         """String representation of the image"""
#         return self.full_name

#     def __repr__(self) -> str:
#         """Detailed string representation"""
#         return (
#             f"Image(registry: '{self.registry}', "
#             f"namespace: '{self.namespace}', "
#             f"name: '{self.name}', "
#             f"tag: '{self.tag}')"
#         )

#     def get_details(self) -> dict[str, str]:
#         """Get detailed information as dictionary"""
#         return {
#             "registry": self.registry,
#             "namespace": self.namespace,
#             "name": self.name,
#             "tag": self.tag,
#             "repository": self.get_repository(),
#             "full_name": self.full_name,
#             "docker_hub_url": self.docker_hub_url,
#             "api_url": self.api_url,
#         }

#     def check_repository_tag(
#         self, token: str | None = None, tag: str | None = None
#     ) -> dict[str, Any]:
#         """
#         Check if tag exists in repository using HEAD request
#         https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags~1%7Btag%7D/head

#         By default checks current tag of the image.

#         Response Codes:
#             200: Tag exists
#             403: Forbidden
#             404: Tag not found
#         """
#         if tag is None:
#             tag = self.tag

#         try:
#             url = (
#                 # f"https://hub.docker.com/v2/repositories/{self.get_repository()}/tags/{tag}"
#                 f"{self.api_url}/tags/{tag}"
#             )
#             headers = {"Authorization": f"Bearer {token}"} if token else {}

#             response = requests.head(url, headers=headers, timeout=10)

#             if response.status_code == 404:
#                 return {
#                     "status": "error",
#                     "message": f"Tag {tag} not found in repository {self.get_repository()}",
#                     "repository": self.get_repository(),
#                     "tag": tag,
#                 }

#             if response.status_code == 403:
#                 return {
#                     "status": "error",
#                     "message": f"Forbidden access to repository {self.get_repository()}",
#                     "repository": self.get_repository(),
#                     "tag": tag,
#                 }

#             if response.status_code != 200:
#                 return {
#                     "status": "error",
#                     "message": f"Failed to check tag. Status code: {response.status_code}",
#                     "repository": self.get_repository(),
#                     "tag": tag,
#                 }

#             return {
#                 "status": "success",
#                 "repository": self.get_repository(),
#                 "tag": tag,
#                 "last_modified": response.headers.get("Last-Modified"),
#                 "etag": response.headers.get("ETag"),
#             }

#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"Error checking tag: {str(e)}",
#                 "repository": self.get_repository(),
#                 "tag": tag,
#             }

#     def list_repository_tags(
#         self,
#         token: str | None = None,
#         page: int = 1,
#         page_size: int = 10,
#     ) -> dict[str, Any]:
#         """
#         Get list of tags for repository with pagination
#         https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags/get

#         Args:
#             token: Optional Docker Hub bearer token
#             page: Page number (default: 1)
#             page_size: Number of items per page (default: 10, max: 100)

#         Returns:
#             Dictionary containing:
#                 - status: "success" or "error"
#                 - count: Total number of results available
#                 - next: Link to next page of results if any
#                 - previous: Link to previous page of results if any
#                 - results: Array of tag objects
#                 - message: Error message if failed
#                 - detail: Error detail if failed

#         Response Codes:
#             200: Successful operation
#             403: Forbidden
#             404: Repository not found
#         """
#         try:
#             url = f"https://hub.docker.com/v2/repositories/{self.get_repository()}/tags"
#             params = {"page": page, "page_size": min(page_size, 100)}
#             headers = {"Authorization": f"Bearer {token}"} if token else {}

#             response = requests.get(url, params=params, headers=headers, timeout=10)

#             if response.status_code == 403:
#                 return {
#                     "status": "error",
#                     "message": response.json().get("message", "Access forbidden"),
#                     "detail": response.json().get("detail", "No additional details"),
#                 }

#             if response.status_code == 404:
#                 return {
#                     "status": "error",
#                     "message": response.json().get("message", "Not found"),
#                     "detail": response.json().get("detail", "Repository not found"),
#                 }

#             if response.status_code != 200:
#                 return {
#                     "status": "error",
#                     "message": f"Failed to get tags. Status code: {response.status_code}",
#                     "detail": response.text,
#                 }

#             data = response.json()
#             return {
#                 "status": "success",
#                 "count": data.get("count", 0),
#                 "results": [
#                     {
#                         "tag": tag["name"],
#                         "last_pushed": tag.get("tag_last_pushed", "N/A"),
#                     }
#                     for tag in data.get("results", [])
#                 ],
#                 "page": page,
#                 "page_size": page_size,
#             }

#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"Error getting tags: {str(e)}",
#                 "detail": str(e),
#             }


#     def get_sorted_tags(
#         self,
#         token: str | None = None,
#         tags: int = 10, # 1 - 100
#         reverse: bool = True,
#     ) -> dict[str, Any]:
#         """
#         Get sorted list of tags

#         Args:
#             token: Optional Docker Hub bearer token
#             page: Page number
#             page_size: Items per page
#             reverse: If True, sort newest first (default)
#         """
#         result = self.list_repository_tags(token=token, page_size=tags)

#         if result["status"] == "success" and result.get("results"):
#             result["results"] = sorted(
#                 result["results"], key=lambda x: x["last_pushed"], reverse=reverse
#             )

#         return result
