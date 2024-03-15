from kubernetes import client, config  # , dynamic

# from kubernetes.client import api_client


try:
    # use current context (in Pod)
    config.load_incluster_config()
except:
    # local kubeconfig (on laptop)
    config.load_kube_config()

v1 = client.CoreV1Api()


def fetch_configmap_key(configmap_name, namespace, key):
    try:
        configmap = v1.read_namespaced_config_map(
            name=configmap_name,
            namespace=namespace,
            pretty="true",
            # allow_watch_bookmarks=allow_watch_bookmarks,
            # _continue=_continue,
            # field_selector=field_selector,
            # label_selector=label_selector,
            # limit=limit,
            # resource_version=resource_version,
            # resource_version_match=resource_version_match,
            # send_initial_events=send_initial_events,
            # timeout_seconds=timeout_seconds,
            # watch='true'
        )
        return configmap.data[key]
    except:
        # todo add except processing
        print(f"Failed to read ConfigMap '{configmap_name}'")
