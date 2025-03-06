# tests/test_image.py
import pytest
from releases_info.image import Image


@pytest.fixture
def sample_images():
    return [
        "docker.io/kindest/kindnetd:v20241212-9f82dd49",
        "docker.io/postgres:14",
        "docker.io/grafana/grafana:11.5.2",
        "docker.io/bitnami/postgresql:17.4.0-debian-12-r4",
    ]


def test_image_from_string_with_namespace():
    """Test parsing image with namespace"""
    image_str = "docker.io/kindest/kindnetd:v20241212-9f82dd49"
    img = Image.from_string(image_str)

    assert img.full_name == image_str
    assert img.registry == "docker.io"
    assert img.namespace == "kindest"
    assert img.name == "kindnetd"
    assert img.tag == "v20241212-9f82dd49"
    assert img.get_repository() == "kindest/kindnetd"
    assert (
        img.get_api_tag_url()
        == "https://hub.docker.com/v2/repositories/kindest/kindnetd/tags/v20241212-9f82dd49"
    )


def test_image_from_string_library():
    """Test parsing official image (library)"""
    image_str = "docker.io/postgres:14"
    img = Image.from_string(image_str)

    assert img.full_name == image_str
    assert img.registry == "docker.io"
    assert img.namespace == "library"
    assert img.name == "postgres"
    assert img.tag == "14"
    assert img.get_repository() == "library/postgres"
    assert (
        img.get_api_tag_url()
        == "https://hub.docker.com/v2/repositories/library/postgres/tags/14"
    )


def test_image_urls_generation():
    """Test URLs generation"""
    image_str = "docker.io/grafana/grafana:11.5.2"
    img = Image.from_string(image_str)

    assert img.docker_hub_url == "https://hub.docker.com/r/grafana/grafana"
    assert (
        img.docker_hub_tag_url
        == "https://hub.docker.com/r/grafana/grafana/tags?name=11.5.2"
    )
    assert img.api_url == "https://hub.docker.com/v2/repositories/grafana/grafana"


@pytest.mark.parametrize(
    "image_string",
    [
        "docker.io/kindest/kindnetd:v20241212-9f82dd49",
        "docker.io/postgres:14",
        "docker.io/grafana/grafana:11.5.2",
        "docker.io/bitnami/postgresql:17.4.0-debian-12-r4",
    ],
)
def test_image_parsing(image_string):
    """Test parsing different image formats"""
    img = Image.from_string(image_string)
    assert img.full_name == image_string
    assert img.registry == "docker.io"
    assert "/" in img.get_repository()
