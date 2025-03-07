# services/factory.py
from typing import Optional
from ..models.docker_image import DockerImage


class ImageFactory:
    SUPPORTED_REGISTRIES = ["docker.io"]

    @classmethod
    def create_image(cls, image_string: str) -> Optional[DockerImage]:
        registry = image_string.split("/")[0]

        if registry == "docker.io":
            return DockerImage.from_string(image_string)

        return None

    @classmethod
    def is_supported(cls, image_string: str) -> bool:
        registry = image_string.split("/")[0]
        return registry in cls.SUPPORTED_REGISTRIES
