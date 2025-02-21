pipeline {
    agent any
    environment {
        microservices_api_repo = "${env.microservices_api_repo}"
        microservices_branch_name = "${env.microservices_branch_name}"
        microservices_docker_image = "${env.microservices_docker_image}"
        KUBECONFIG = "${env.KUBECONFIG}"
        eks_region = "${env.eks_region}"
        ecr_repo_uri = "${env.ecr_repo_uri}"
        DOCKER_HUB_USERNAME = "${env.DOCKER_HUB_USERNAME}"
        DOCKER_HUB_TAGNAME = "${env.DOCKER_HUB_TAGNAME}"
    }
    // chekout
    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${microservices_branch_name}", url: "${microservices_api_repo}"
            }
        }
        stage('Docker build') {
            steps {
                sh '''
                    echo "Building Docker image ...."
                    docker build -t ${microservices_docker_image} .
                    docker tag ${microservices_docker_image} ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_TAGNAME}:${microservices_docker_image}
                '''
            }
        }
        stage('Check AWS Credentials') {
            steps {
                script {
                    echo "AWS_ACCESS_KEY_ID: ${env.AWS_ACCESS_KEY_ID}"
                    echo "AWS_SECRET_ACCESS_KEY: ${env.AWS_SECRET_ACCESS_KEY}"
                    sh 'aws sts get-caller-identity'
                }
            }
        }
        stage('Push to DockerHub/ECR') {
            steps {
                withCredentials([string(credentialsId: 'DOCKER_HUB_PASSWORD', variable: 'DOCKER_HUB_PASS')]) {
                    sh '''
                        echo "$DOCKER_HUB_PASS" | docker login -u ${DOCKER_HUB_USERNAME} --password-stdin
                        docker push ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_TAGNAME}:${microservices_docker_image}
                    '''
                }
            }
        }
         stage('Check Kubernetes Context') {
            steps {
                withCredentials([file(credentialsId: 'EKS_CONFIG11', variable: 'KUBECONFIG')]) {
                    sh 'kubectl config get-contexts'
                    sh 'kubectl config current-context'
                    sh 'kubectl get namespaces'
                }
            }
        }
        stage('Debug Workspace') {
    steps {
        sh 'pwd'       
        sh 'ls -R
    }
}

        stage('Deploy to EKS') {
            steps {
                script {
                    def filesToApply = [
                        "K8S/app-deployment.yaml",
                        "K8S/app-service.yaml",
                        "K8S/configmap.yaml",
                        "K8S/ingress.yaml",
                        "K8S/mongo-deployment.yaml",
                        "K8S/mongo-service.yaml",
                        "K8S/mysql-deployment.yaml",
                        "K8S/mysql-service.yaml",
                        "K8S/redis-deployment.yaml",
                        "K8S/redis-service.yaml",
                        "K8S/secret.yaml"
                    ]
                    for (def file : filesToApply) {
                        echo "Applying ${file}"
                        sh "kubectl apply -f ${file} --namespace=${env.NAMESPACE}"
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Deployment success'
        }
        failure {
            echo 'Deployment failure'
        }
    }
}