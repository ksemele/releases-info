# models/docker_image.py
from ..config import (
    dataclass,
    Dict,
    Any,
    Optional,
    aiohttp,
)
from .image import BaseImage

@dataclass
class DockerImage(BaseImage):
    namespace: str = "library"
    docker_hub_url: str = ""
    docker_hub_tag_url: str = ""

    @classmethod
    def from_string(cls, image_string: str) -> "DockerImage":
        """Parse docker image string into DockerImage object"""
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

    def get_repository(self) -> str:
        """Get full repository path (namespace/name)"""
        return f"{self.namespace}/{self.name}"

    def get_docker_hub_url(self) -> str:
        """Get Docker Hub web UI URL"""
        return self.docker_hub_url

    def get_docker_hub_tag_url(self) -> str:
        """Get Docker Hub web UI URL for specific tag"""
        return self.docker_hub_tag_url

    def get_api_tag_url(self) -> str:
        """Get Docker Hub API URL for specific tag"""
        return f"{self.api_url}/tags/{self.tag}"

    async def check_repository_tag(
        self,
        session: aiohttp.ClientSession,
        token: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        if tag is None:
            tag = self.tag

        try:
            url = f"{self.api_url}/tags/{tag}"
            headers = {"Authorization": f"Bearer {token}"} if token else {}

            async with session.head(url, headers=headers) as response:
                if response.status == 404:
                    return {"status": "error", "message": f"Tag {tag} not found"}

                if response.status == 403:
                    return {"status": "error", "message": "Access forbidden"}

                if response.status != 200:
                    return {
                        "status": "error",
                        "message": f"Failed to check tag. Status: {response.status}",
                    }

                return {
                    "status": "success",
                    "last_modified": response.headers.get("Last-Modified"),
                    "etag": response.headers.get("ETag"),
                }

        except Exception as e:
            return {"status": "error", "message": f"Error checking tag: {str(e)}"}

    async def get_digest(self, session: aiohttp.ClientSession) -> Optional[str]:
        try:
            async with session.get(f"{self.api_url}/tags/{self.tag}") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("images", [{}])[0].get("digest")
                return None
        except Exception:
            return None

    async def get_size(self, session: aiohttp.ClientSession) -> Optional[int]:
        try:
            async with session.get(f"{self.api_url}/tags/{self.tag}") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("full_size")
                return None
        except Exception:
            return None
