pipeline{
    agenty agent
    environment :{
        microservices-api-repo= "${env.microservices-api-repo}"
        microservices-branch-name="${env.microservices-branch-name}"
        microservices-docker-image= "${env.microservices-docker-image}"
        KUBECONFIG = "${env.KUBECONFIG}"
        eks-region="${env.eks-region}"
        ecr-repo-uri="${env.ecr-repo-uri}"
    }
    stages{
        stage('Checkout Code'){
            steps{
                git branch:"${microservices-branch-name}",
                url:"${microservices-api-repo}"
            }   
        }
        stage('Docker build'){
           steps{
            sh '''
            echo "Building Docker image ...."
            docker build -t ${microservices-docker-image}
            '''
           } 
       }
        stage('Push to DockerHub/ECR'){
            steps{
              sh '''
              echo "Logging into Amazon ECR..."
              aws ecr get-login-password --region ${eks-region} | docker login --username AWS --password-stdin ${ecr-repo-uri} 
              echo "Logging into Amazon ECR..."
              docker tag ${microservices-docker-image}:latest ${ecr-repo-uri}:${microservices-docker-image} 
              docker push ${ecr-repo-uri}:${microservices-docker-image}
             
              '''
            }

        }
        stage('Deploy to EKS'){

        }
    }
}