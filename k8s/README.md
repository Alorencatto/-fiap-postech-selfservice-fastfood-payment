# Kubernetes
This document represents a general brief of our k8s architecture, including how the containers are organized, how the communication are managed and how we ensure the system resilience.

You can execute your cluster choosing between minikube, kind or kubernetes
## K8s Architechture
![alt text](k8s-archtechture.png)

## Minikube
```shell
minikube start --mount-string "$HOME/minikube/postgres-data:/data" --driver=docker --install-addons=true --kubernetes-version=stable
minikube stop
minikube delete
```
## Kind
```shell
brew install kind

kind create cluster
kind get clusters

- Pausing cluster
docker stop kind-control-plane

- Resume cluster 
docker start kind-control-plane
```

## Enable metrics on cluster
```shell
kubectl apply -f cluster/components.yml

kubectl get deployment metrics-server -n kube-system

kubectl top node
```

## Building image
```shell
docker build --platform=linux/amd64 -t alorencatto/fiap-postech-selfservice-fastfood:0.6.0 .
docker push alorencatto/fiap-postech-selfservice-fastfood:0.6.0
```

## Applying manifests
```shell
kubectl apply -f namespace/ns.yml

-- Application
kubectl apply -f code/secret.yml -n postech
kubectl apply -f code/deployment.yml -n postech
kubectl apply -f code/service.yml -n postech
kubectl apply -f code/nodeport-service.yml -n postech
kubectl apply -f hpa/fiap-postech-selfservice-fastfood-hpa.yml -n postech

-- Postgres
kubectl apply -f postgres/pv.yml -n postech
kubectl apply -f postgres/secret.yml -n postech
kubectl apply -f postgres/pvc.yml -n postech
kubectl apply -f postgres/deployment.yml -n postech
kubectl apply -f postgres/service.yml -n postech

-- Migration Job
kubectl apply -f job/migration.yml -n postech

-- Get resources
kubectl get deployments -n postech
kubectl get pods -n postech

kubectl get svc -n postech
kubectl get pv -n postech
kubectl get pvc -n postech
kubectl get secrets -n postech

kubectl get jobs -n postech
kubectl get hpa -n postech

kubectl describe service nginx-service -n postech
kubectl describe deployment postgres-deployment -n postech
kubectl describe pv postgres-pv -n postech

kubectl top pod -n postech

-- Exposing services
kubectl port-forward service/svc-nodeport-fiap-postech-selfservice-fastfood --address 0.0.0.0 8000:8000 -n postech

-- Rollout restart
kubectl apply -f code/deployment.yml -n postech
kubectl rollout restart deployment fiap-postech-selfservice-fastfood -n postech
```

## Logging
```shell

kubectl get events --all-namespaces  --sort-by='.metadata.creationTimestamp'

kubectl logs fiap-postech-selfservice-fastfood-7499fffdcb-k4jf6 -n postech
kubectl logs fiap-postech-selfservice-fastfood-nginx-deployment-55d6d96n7h6m -n postech
kubectl logs postgres-deployment-857594b99c-tq8kn -n postech
kubectl logs fiap-postech-selfservice-fastfood-migrations-7kkg5 -n postech
```

## Housekeeping
```shell
kubectl delete -f namespace/ns.yml

kubectl delete -f code/secret.yml -n postech
kubectl delete -f code/deployment.yml -n postech
kubectl delete -f code/service.yml -n postech
kubectl delete -f code/nodeport-service.yml -n postech
kubectl delete -f hpa/fiap-postech-selfservice-fastfood-hpa.yml -n postech

kubectl delete -f job/migration.yml -n postech

kubectl delete -f postgres/pv.yml -n postech
kubectl delete -f postgres/secret.yml -n postech
kubectl delete -f postgres/deployment.yml -n postech
kubectl delete -f postgres/pvc.yml -n postech
kubectl delete -f postgres/service.yml -n postech
```

## Stress test
```shell
k6 run scripts/stress-test/test-api.js

kubectl describe deployment fiap-postech-selfservice-fastfood -n postech
```