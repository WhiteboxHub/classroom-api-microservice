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


        stage('Update Kubeconfig for EKS') {
            steps {
                sh '''
                export KUBECONFIG="C:/Users/dhira/.kube/config"
                kubectl config use-context Manisai@cwesion-v2.us-east-1.eksctl.io
                '''
            }
        }

        stage('Check Cluster Info') {
            steps {
                sh '''
                export KUBECONFIG="C:/Users/dhira/.kube/config"
                kubectl cluster-info
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    def filesToApply = [
                        "K8S_DIR/app-deployment.yaml",
                        "K8S_DIR/app-service.yaml",
                        "K8S_DIR/configmap.yaml",
                        "K8S_DIR/ingress.yaml",
                        "K8S_DIR/mongo-deployment.yaml",
                        "K8S_DIR/mongo-service.yaml",
                        "K8S_DIR/mysql-deployment.yaml",
                        "K8S_DIR/mysql-service.yaml",
                        "K8S_DIR/redis-deployment.yaml",
                        "K8S_DIR/redis-service.yaml",
                        "K8S_DIR/secret.yaml"
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