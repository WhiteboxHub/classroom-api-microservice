pipeline {
    agent any
    environment {
        microservices_api_repo = "${env.microservices_api_repo}"
        microservices_branch_name = "${env.microservices_branch_name}"
        microservices_docker_image = "${env.microservices_docker_image}"
        KUBECONFIG = "${env.KUBECONFIG}"
        eks_region = "${env.eks_region}"
        ecr_repo_uri = "${env.ecr_repo_uri}"
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${microservices_branch_name}",
                    url: "${microservices_api_repo}"
            }
        }
        stage('Docker build') {
            steps {
                sh '''
                echo "Building Docker image ...."
                docker build -t ${microservices_docker_image} .
                '''
            }
        }
        stage('Check AWS Credentials') {
            steps {
                script {
                    // Print the AWS_ACCESS_KEY_ID (the secret key will be masked if configured)
                    echo "AWS_ACCESS_KEY_ID: ${env.AWS_ACCESS_KEY_ID}"
                    echo "AWS_SECRETE_KEY_ID: ${env.AWS_SECRETE_KEY_ID}"
                    
                    // Run a simple AWS CLI command to verify credentials
                    sh 'aws sts get-caller-identity'
                }
            }
        }
        stage('Push to DockerHub/ECR') {
            steps {
                sh '''
                echo "Logging into Amazon ECR..."
                aws ecr get-login-password --region ${eks_region} | docker login --username AWS --password-stdin ${ecr_repo_uri}
                docker tag ${microservices_docker_image}:latest ${ecr_repo_uri}:${microservices_docker_image}
                docker push ${ecr_repo_uri}:${microservices_docker_image}
                '''
            }
        }
        stage('Check Kubectl installation') {
            steps {
                script {
                    sh 'kubectl version --client'
                    def context = sh(script: 'kubectl config current-context', returnStdout: true).trim()
                    echo "Current kubectl context: ${context}"
                }
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
                        sh "kubectl apply -f ${file} --namespace=${NAMESPACE}"
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