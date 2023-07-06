import re
from kubernetes import client, config


try:
    # use current context (in Pod)
    config.load_incluster_config()
except:
    # local kubeconfig (on laptop)
    config.load_kube_config()


v1 = client.CoreV1Api()
unique_images = {}

pod_list = v1.list_pod_for_all_namespaces(watch=False)
print(f'## total pods: {len(pod_list.items)}')

unique_images = set()

repository_list = ["gcr.io", "docker.io", "registry.k8s.io"]

for pod in pod_list.items:
    for container in pod.spec.containers:
        # if image in Pod not known - we add default docker.io prefix
        if not re.match(r'^(' + '|'.join(repository_list) + ')/', container.image):
            # print(f'Modify to default: {container.image} -> {repo}')
            image = f'docker.io/{container.image}'
        else:
            image = container.image
        unique_images.add(image)

def generate_config_yaml(unique_images):
    result = ""
    for image in unique_images:
        result += f"# {image}\n"
        if image.startswith('docker.io/'):
            repo, tag = image.split(':')
            result += f"{repo.split('/')[-1]}:\n"
            result += f"  dockerhub:\n"
            if image.count('/') == 1:  # WIP for images like docker.io/nginx:latest - need to use library/nginx instead of registry...
                result += f"    owner: library\n"
                result += f"    repo: {repo.split('/')[1]}\n"
            else:
                result += f"    owner: {repo.split('/')[1]}\n"
                result += f"    repo: {repo.split('/')[2]}\n"
            result += f"  version: {tag}\n"
        else:
            result += f"# registry [{image.split('/')[0]}] UNSUPPORTED now\n"
        result += "\n"
    return result

config_yaml = generate_config_yaml(unique_images=unique_images)
print(config_yaml)

def save_data_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            f.write(data)
    except IOError:
        print(f"Error write to file: [{filename}]")

filename = 'config.yaml'
save_data_to_file(config_yaml, filename)


def create_or_update_configmap(configmap_name, data, namespace='default'):
    # config.load_kube_config()
    api = client.CoreV1Api()

    body = {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {
            'name': configmap_name,
        },
        'data': data,
    }

    try:
        api.create_namespaced_config_map(namespace=namespace, body=body)
        print(f"ConfigMap '{configmap_name}' created.")
    except client.exceptions.ApiException as e:
        if e.status == 409:  # ConfigMap already exists, update it
            try:
                api.patch_namespaced_config_map(name=configmap_name, namespace=namespace, body=body)
                print(f"ConfigMap '{configmap_name}' updated.")
            except client.exceptions.ApiException as e:
                print(f"Failed to update ConfigMap '{configmap_name}': {e}")
        else:
            print(f"Failed to create or update ConfigMap '{configmap_name}': {e}")


def save_configmap_from_file(configmap_name, filename, namespace='default'):
    try:
        with open(filename, 'r') as f:
            data = {
                filename: f.read()
            }
            create_or_update_configmap(configmap_name, data, namespace)
    except IOError:
        print(f"Error reading file: '{filename}'")
        

# filename = 'config.yaml'
# configmap_name = 'scraper-configmap'
# save_configmap_from_file(configmap_name, filename, namespace='default')

# def save_configmap_from_data(configmap_name, data, namespace='default'):
#     create_or_update_configmap(configmap_name, data, namespace)

# data = {
#     'key1': 'value1',
#     'key2': 'value2'
# }
# configmap_name = 'scraper-configmap-2'
# save_configmap_from_data(configmap_name, data, namespace='default')
