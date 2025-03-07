# services/processor.py
from ..config import (
    List,
    Optional,
    aiohttp,
    asyncio,
    ic,
)
from .factory import ImageFactory
from ..models.image import BaseImage

class ImageProcessor:
    def __init__(self):
        self.factory = ImageFactory()
        self._processed_images: List[BaseImage] = []

    async def process_images(self, images: List[str]) -> List[BaseImage]:
        """Process images using their own methods"""

        self._processed_images = [
            self.factory.create_image(img)
            for img in images
            if self.factory.is_supported(img)
        ]

        if not self._processed_images:
            return []

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._process_single_image(session, image)
                for image in self._processed_images
            ]
            await asyncio.gather(*tasks)

        return self._processed_images


    async def _process_single_image(
        self, session: aiohttp.ClientSession, image: BaseImage
    ) -> None:
        """Process single image using its methods"""
        try:
            tag_check = await image.check_repository_tag(session)
            if tag_check["status"] != "success":
                image.error = tag_check["message"]
                return

            tasks = [
                image.get_digest(session),
                image.get_size(session),
                image.fetch_available_tags(session, tag_count=3),
            ]

            digest, size, tags = await asyncio.gather(*tasks)

            image.digest = digest
            image.size = size

        except Exception as e:
            image.error = f"Error processing image: {str(e)}"

    @property
    def processed_images(self) -> List[BaseImage]:
        """Get list of processed images"""
        return self._processed_images

    def get_successful_images(self) -> List[BaseImage]:
        """Get list of successfully processed images"""
        return [img for img in self._processed_images if not img.error]
