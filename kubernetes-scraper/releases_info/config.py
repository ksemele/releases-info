# releases_info/config.py
import random
import time
import json
from prometheus_client import Info
from prometheus_client import start_http_server
from kubernetes import client, config
from icecream import ic


def setup_debug():
    """Setup debug output configuration"""
    ic.enable()
    ic.configureOutput(includeContext=True)


def setup_kubernetes():
    """Setup kubernetes configuration"""
    try:
        # use current context (in Pod)
        config.load_incluster_config()
    except:
        # local kubeconfig (on laptop)
        config.load_kube_config()
    return client.CoreV1Api()


# Инициализация
setup_debug()
v1 = setup_kubernetes()

# Экспортируем все нужные переменные и функции
__all__ = [
    "v1",
    "Info",
    "start_http_server",
    "random",
    "time",
    "json",
    "ic",
    ]
