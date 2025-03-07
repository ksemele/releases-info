# releases_info/config.py
import random
import time
import json
from prometheus_client import Info
from prometheus_client import start_http_server
from kubernetes import client, config
from icecream import ic
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod


def setup_debug():
    """Setup debug output configuration"""
    ic.enable()
    ic.configureOutput(includeContext=True)


def setup_kubernetes():
    """Setup kubernetes configuration"""
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    return client.CoreV1Api()


setup_debug()
v1 = setup_kubernetes()

__all__ = [
    "v1",
    "Info",
    "start_http_server",
    "random",
    "time",
    "json",
    "ic",
    "aiohttp",
    "asyncio",
    "Dict",
    "Any",
    "Optional",
    "List",
    "dataclass",
    "datetime",
    "ABC",
    "abstractmethod",
]
