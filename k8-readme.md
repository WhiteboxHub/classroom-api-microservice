# FastAPI Microservice Deployment Guide

## Deployment Steps

### 1️⃣ Apply ConfigMaps and Secrets
```sh
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
```

### 2️⃣ Deploy MySQL, Redis, and MongoDB
```sh
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml
kubectl apply -f k8s/mongo-deployment.yaml
kubectl apply -f k8s/mongo-service.yaml
```

### 3️⃣ Deploy FastAPI App
```sh
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
```

### 4️⃣ Deploy Ingress (Optional)
```sh
kubectl apply -f k8s/ingress.yaml
```

---

## Deploy on Minikube (Local)

### Prerequisites
- ✅ Install [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- ✅ Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- ✅ Install [Docker](https://docs.docker.com/get-docker/)

### 1️⃣ Start Minikube
```sh
minikube start
```

### 2️⃣ Enable Ingress Controller
```sh
minikube addons enable ingress
```

### 3️⃣ Build and Load Docker Image to Minikube
```sh
eval $(minikube docker-env)
docker build -t fastapi-microservice:latest .
```

### 4️⃣ Apply Kubernetes YAML Files
```sh
kubectl apply -f k8s/
```

### 5️⃣ Get Minikube IP & Test
```sh
minikube ip
```
Add the output IP to `/etc/hosts`:
```sh
echo "$(minikube ip) fastapi.local" | sudo tee -a /etc/hosts
```

### 6️⃣ Access FastAPI
```sh
curl http://fastapi.local
```

---

## Deploy on AWS EKS (Cloud)

### Prerequisites
- ✅ Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- ✅ Install [eksctl](https://eksctl.io/)
- ✅ Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- ✅ Install [Docker](https://docs.docker.com/get-docker/)

### 1️⃣ Create an EKS Cluster
```sh
eksctl create cluster --name fastapi-cluster --region us-west-2 --nodes 2
```

### 2️⃣ Push Docker Image to AWS ECR
```sh
aws ecr create-repository --repository-name fastapi-microservice

# Authenticate Docker with ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <your_account_id>.dkr.ecr.us-west-2.amazonaws.com

# Tag and Push Image
docker tag fastapi-microservice:latest <your_account_id>.dkr.ecr.us-west-2.amazonaws.com/fastapi-microservice:latest
docker push <your_account_id>.dkr.ecr.us-west-2.amazonaws.com/fastapi-microservice:latest
```

### 3️⃣ Update `app-deployment.yaml`
Edit `app-deployment.yaml`, update the image with the ECR URL:
```yaml
containers:
  - name: fastapi-app
    image: <your_account_id>.dkr.ecr.us-west-2.amazonaws.com/fastapi-microservice:latest
```

### 4️⃣ Apply Kubernetes Configs
```sh
kubectl apply -f k8s/
```

### 5️⃣ Set Up Ingress Controller
```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/aws/deploy.yaml
```

### 6️⃣ Get Ingress External IP
```sh
kubectl get ingress
```
Copy the external IP and test:
```sh
curl http://<external-ip>
```

---

## Deploy Using Helm

### 1️⃣ Install Helm
```sh
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 2️⃣ Package and Install the Helm Chart
```sh
cd helm/fastapi-chart
helm install fastapi-microservice .
```

### 3️⃣ Verify the Deployment
```sh
kubectl get pods
kubectl get svc
```

### 4️⃣ Get Ingress URL
```sh
kubectl get ingress
```
Access the API:
```sh
curl http://fastapi.local
```

---

## ✅ Summary

| Step                | Minikube (Local)                | AWS EKS (Cloud)                |
|---------------------|--------------------------------|--------------------------------|
| Start Cluster      | `minikube start`               | `eksctl create cluster`       |
| Enable Ingress     | `minikube addons enable ingress` | `kubectl apply -f ingress-nginx` |
| Build Image       | `docker build`                  | `docker push to AWS ECR`       |
| Deploy            | `kubectl apply -f k8s/`        | `kubectl apply -f k8s/`        |
| Access            | `fastapi.local`                | `curl http://<external-ip>`    |

| Step               | Command |
|--------------------|-------------------------------|
| Install Helm      | `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3` |
| Package Chart     | `cd helm/fastapi-chart && helm package .` |
| Deploy with Helm  | `helm install fastapi-microservice .` |
| Verify Deployment | `kubectl get pods` |
| Access API        | `curl http://fastapi.local` |

