# Classroom API Microservice

## Overview
Classroom API Microservice provides a scalable and efficient way to manage student data using containerized microservices with Docker and Kubernetes. The API supports authentication and CRUD operations on student data.

## Getting Started

### Clone the Repository
```sh
git clone git@github.com:WhiteboxHub/classroom-api-microservice.git
cd classroom-api-microservice
```

### Run with Docker Compose
#### Build and start services:
```sh
docker-compose up --build
```
#### Start services in detached mode:
```sh
docker-compose up -d
```
#### Enable watch mode for changes:
```sh
docker compose up --watch
```

### Run with Kubernetes and Minikube
#### Start Minikube:
```sh
minikube start
```
#### Deploy services:
```sh
kubectl apply -f k8s/
```
#### Check running pods:
```sh
kubectl get pods
```
#### Get service URL:
```sh
minikube service student-service --url
```

## API Documentation
Access Swagger UI for API documentation:
```sh
http://127.0.0.1:8000/docs
```

## Authentication
Obtain an authentication token:
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=password'
```

## API Endpoints
### Get Students
```sh
curl -X 'GET' 'http://127.0.0.1:8000/students/' \
  -H 'Authorization: Bearer your_jwt_token'
```

### Create a New Student
```sh
curl -X 'POST' 'http://127.0.0.1:8000/students/' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_jwt_token' \
  -d '{
    "name": "John Doe",
    "age": 12,
    "grade": "6th"
}'
```

## Stopping Services
### Stop and remove Docker containers:
```sh
docker-compose down
```
### Delete Kubernetes resources:
```sh
kubectl delete -f k8s/
```

## Logs and Debugging
### View Docker container logs:
```sh
docker logs -f container_name
```
### View Kubernetes pod logs:
```sh
kubectl logs pod_name
```

---

## License
This project is licensed under the MIT License.

## Contributors
- Whitebox Learning
