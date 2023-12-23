from prometheus_client import Info

# Creating a metric
image_versions = Info("kubernetes_image_versions", "Current image versions")

# List of images
images = [
    "registry.k8s.io/etcd:3.5.7-0",
    "docker.io/nginx:latest",
    "ghcr.io/fluxcd/kustomize-controller:v1.1.1",
]

for image in images:
    image_name, image_version = image.rsplit(":", 1)

    # We set the metric values.
    image_versions.labels(image_name=image_name).info({"version": image_version})
