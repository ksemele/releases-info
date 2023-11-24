from .constants import *

from icecream import ic

ic.enable()
ic.configureOutput(includeContext=True)

from kubernetes import client, config

try:
    # use current context (in Pod)
    config.load_incluster_config()
except:
    # local kubeconfig (on laptop)
    config.load_kube_config()


v1 = client.CoreV1Api()