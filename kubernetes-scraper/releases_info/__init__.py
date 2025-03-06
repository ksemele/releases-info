# releases_info/__init__.py
from .kubernetes import *
from .scraper import *
from .dockerhub_releases import *
from .prometheus import *
from .constants import *
from .config import setup_debug, setup_kubernetes

setup_debug()
v1 = setup_kubernetes()

__all__ = [
    "v1",
    "NAMESPACE",
    "CONFIGFILE_NAME",
    "CONFIGMAP_NAME",
    "PROMETHEUS_PORT",
    "get_unique_images_from_pods",
    "create_or_update_configmap",
    "create_or_update_configmap_from_file",
    "query_prometheus",
    "dockerhub_releases",
]
