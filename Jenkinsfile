pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aman99jnvchd/system-monitor"
        EC2_USER = "ubuntu"
        EC2_HOST = "65.0.179.193"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/aman99jnvchd/system-monitor.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST <<EOF
                    echo "🔄 Pulling latest image..."
                    sudo docker pull $DOCKER_IMAGE:latest

                    echo "🛑 Stopping and removing existing container..."
                    sudo docker stop my_app || true
                    sudo docker rm my_app || true

                    echo "🚀 Running new container..."
                    sudo docker run -d --name my_app -p 80:5000 --restart unless-stopped $DOCKER_IMAGE:latest
                    EOF
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build, push, and deployment successful!"
        }
        failure {
            echo "❌ Build or deployment failed!"
        }
    }
}
