# models/image.py
from ..config import (
    ABC,
    abstractmethod,
    dataclass,
    datetime,
    Dict,
    Any,
    Optional,
    List,
    aiohttp,
)


@dataclass
class BaseImage(ABC):
    full_name: str
    registry: str
    name: str
    tag: str
    api_url: str
    digest: Optional[str] = None
    size: Optional[int] = None
    last_updated: Optional[str] = None
    error: Optional[str] = None
    available_tags: Optional[List[str]] = None

    def __post_init__(self):
        """Initialize optional fields"""
        self.error = None

    @classmethod
    @abstractmethod
    def from_string(cls, image_string: str) -> "BaseImage":
        """Parse image string into Image object"""
        pass

    @abstractmethod
    async def check_repository_tag(
        self,
        session: aiohttp.ClientSession,
        token: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_repository_tags(
        self, session: aiohttp.ClientSession, tag_count: int = 1
    ) -> Dict[str, Any]:
        pass

    async def fetch_available_tags(
        self, session: aiohttp.ClientSession, tag_count: int = 10
    ) -> List[str]:
        """Fetch and store available tags"""
        try:
            tags_info = await self.get_repository_tags(session, tag_count)
            if tags_info["status"] == "success":
                self.available_tags = [
                    result["tag"]
                    for result in tags_info.get("results", [])
                ]
                return self.available_tags
            return []
        except Exception as e:
            self.error = f"Error fetching tags: {str(e)}"
            return []

    @abstractmethod
    async def get_digest(self, session: aiohttp.ClientSession) -> Optional[str]:
        pass

    @abstractmethod
    async def get_size(self, session: aiohttp.ClientSession) -> Optional[int]:
        pass

    # common methods
    def get_full_name(self) -> str:
        """Get full image name including registry and tag"""
        return self.full_name

    def get_registry(self) -> str:
        """Get registry domain"""
        return self.registry

    def get_name(self) -> str:
        """Get image name without registry and tag"""
        return self.name

    def get_tag(self) -> str:
        """Get image tag"""
        return self.tag

    def get_api_url(self) -> str:
        """Get api url"""
        return self.api_url

    def get_details(self) -> Dict[str, str]:
        """Get detailed information as dictionary"""
        return {
            "full_name": self.full_name,
            "registry": self.registry,
            "name": self.name,
            "tag": self.tag,
        }

    def __str__(self) -> str:
        """String representation of the image"""
        return self.full_name

    def __repr__(self) -> str:
        """Detailed string representation"""
        return (
            f"{self.__class__.__name__}(registry: '{self.registry}', "
            f"name: '{self.name}', "
            f"tag: '{self.tag}')"
        )
