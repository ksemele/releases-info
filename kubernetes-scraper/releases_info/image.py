from dataclasses import dataclass
from datetime import datetime
import requests
from icecream import ic
from .types import Any


@dataclass
class Image:
    full_name: str
    registry: str
    namespace: str
    name: str
    tag: str
    docker_hub_url: str
    docker_hub_tag_url: str
    api_url: str

    @classmethod
    def from_string(cls, image_string: str) -> "Image":
        # docker.io/kindest/kindnetd:v20241212-9f82dd49
        # docker.io/postgres:14 -> library/postgres:14
        parts = image_string.split("/")
        registry = parts[0]  # docker.io
        image_with_tag = parts[-1]  # kindnetd:v20241212-9f82dd49 or postgres:14

        if len(parts) == 2:
            namespace = "library"
            name_with_tag = parts[1]
        else:
            namespace = parts[1]
            name_with_tag = parts[-1]

        name, tag = name_with_tag.split(":")

        repository = f"{namespace}/{name}"
        docker_hub_url = f"https://hub.docker.com/r/{repository}"
        docker_hub_tag_url = f"{docker_hub_url}/tags?name={tag}"
        api_url = f"https://hub.docker.com/v2/repositories/{repository}"

        return cls(
            full_name=image_string,
            registry=registry,
            namespace=namespace,
            name=name,
            tag=tag,
            docker_hub_url=docker_hub_url,
            docker_hub_tag_url=docker_hub_tag_url,
            api_url=api_url,
        )

    def get_api_tag_url(self) -> str:
        repository = f"{self.namespace}/{self.name}"
        return f"{self.api_url}/tags/{self.tag}"

    def get_repository(self) -> str:
        return f"{self.namespace}/{self.name}"

    def check_repository_tag(self, token: str | None = None) -> dict[str, Any]:
        """
        Check if tag exists in repository
        https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags~1%7Btag%7D/head

        Response Codes:
            200: Successful operation
            403: Forbidden
            404: Repository not found
        """
        try:
            url = f"https://hub.docker.com/v2/repositories/{self.get_repository()}/tags/{self.tag}"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(url, headers=headers, timeout=10)
            # ic(f"Response status: {response.status_code}")

            try:
                response_data = response.json()
            except:
                response_data = {}

            if response.status_code == 404:
                return {
                    "status": "error",
                    "message": f"Tag {self.tag} not found in repository {self.get_repository()}",
                    "repository": self.get_repository(),
                    "tag": self.tag,
                    "response": response_data.get("message", "Not found"),
                }

            if response.status_code == 403:
                return {
                    "status": "error",
                    "message": f"Forbidden access to repository {self.get_repository()}",
                    "repository": self.get_repository(),
                    "tag": self.tag,
                    "response": response_data.get("message", "Forbidden"),
                }

            if response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"Failed to check tag. Status code: {response.status_code}",
                    "repository": self.get_repository(),
                    "tag": self.tag,
                    "response": response_data.get("message", "Unknown error"),
                }

            return {
                "status": "success",
                "repository": self.get_repository(),
                "tag": response_data["name"],
                "last_updated": response_data.get("last_updated"),
                "size": response_data.get("full_size"),
                "digest": response_data.get("digest"),
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error checking tag: {str(e)}",
                "repository": self.get_repository(),
                "tag": self.tag,
            }

    def list_repository_tags(
        self,
        token: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, Any]:
        """
        Get list of tags for repository with pagination
        https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags/get

        Args:
            token: Optional Docker Hub bearer token
            page: Page number (default: 1)
            page_size: Number of items per page (default: 10, max: 100)

        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - count: Total number of results available
                - next: Link to next page of results if any
                - previous: Link to previous page of results if any
                - results: Array of tag objects
                - message: Error message if failed
                - detail: Error detail if failed

        Response Codes:
            200: Successful operation
            403: Forbidden
            404: Repository not found
        """
        try:
            url = f"https://hub.docker.com/v2/repositories/{self.get_repository()}/tags"
            params = {"page": page, "page_size": min(page_size, 100)}
            headers = {"Authorization": f"Bearer {token}"} if token else {}

            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code == 403:
                return {
                    "status": "error",
                    "message": response.json().get("message", "Access forbidden"),
                    "detail": response.json().get("detail", "No additional details"),
                }

            if response.status_code == 404:
                return {
                    "status": "error",
                    "message": response.json().get("message", "Not found"),
                    "detail": response.json().get("detail", "Repository not found"),
                }

            if response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"Failed to get tags. Status code: {response.status_code}",
                    "detail": response.text,
                }

            data = response.json()
            return {
                "status": "success",
                "count": data.get("count", 0),
                "results": [
                    {
                        "tag": tag["name"],
                        "last_pushed": tag.get("tag_last_pushed", "N/A"),
                    }
                    for tag in data.get("results", [])
                ],
                "page": page,
                "page_size": page_size,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting tags: {str(e)}",
                "detail": str(e),
            }
