pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aman99jnvchd/system-monitor"
        DOCKER_CONTAINER = "system-monitor"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                /* Jenkins built-in step to wipe workspace */
                cleanWs()
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'master', url: 'https://github.com/aman99jnvchd/system-monitor.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    /* Stop and remove old container if exists */
                    sh "docker stop $DOCKER_CONTAINER || true"
                    sh "docker rm -f $DOCKER_CONTAINER || true"

                    /* Run new container */
                    sh "docker run -d --name $DOCKER_CONTAINER -p 8800:8800 $DOCKER_IMAGE"
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
