pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aman99jnvchd/system-monitor"
    }

    stages {
        stage('Clone Repository') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'github-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                    eval "$(ssh-agent -s)"
                    ssh-add $SSH_KEY
                    git clone git@github.com:aman99jnvchd/system-monitor.git
                    '''
                }
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
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker image prune -f'
        }
        success {
            echo "✅ Build, push, and deployment successful!"
        }
        failure {
            echo "❌ Build or deployment failed!"
        }
    }
}
