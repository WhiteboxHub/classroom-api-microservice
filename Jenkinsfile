pipeline{
    agenty agent
    environment :{
        microservices_api_repo= "${env.microservices_api_repo}"
        microservices_branch_name="${env.microservices_branch_name}"
        microservices_docker_image= "${env.microservices_docker_image}"
        KUBECONFIG = "${env.KUBECONFIG}"
        eks_region="${env.eks_region}"
        ecr_repo_uri="${env.ecr_repo_uri}"
    }
    stages{
        stage('Checkout Code'){
            steps{
                git branch:"${microservices_branch_name}",
                url:"${microservices_api_repo}"
            }   
        }
        stage('Docker build'){
           steps{
            sh '''
            echo "Building Docker image ...."
            docker build -t ${microservices_docker_image}
            '''
           } 
       }
        stage('Push to DockerHub/ECR'){
            steps{
              sh '''
              echo "Logging into Amazon ECR..."
              aws ecr get_login_password --region ${eks_region} | docker login --username AWS --password_stdin ${ecr_repo_uri} 
              echo "Logging into Amazon ECR..."
              docker tag ${microservices_docker_image}:latest ${ecr_repo_uri}:${microservices_docker_image} 
              docker push ${ecr_repo_uri}:${microservices_docker_image}
             
              '''
            }

        }
        stage('Deploy to EKS'){

        }
    }
}