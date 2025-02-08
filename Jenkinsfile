pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aman99jnvchd/system-monitor'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/aman99jnvchd/system-monitor.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    sh 'echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin'
                    sh 'docker push $IMAGE_NAME'
                }
            }
        }

        // stage('Deploy (Optional)') {
        //     steps {
        //         script {
        //             sh 'docker pull $IMAGE_NAME'
        //             sh 'docker run -d --rm -p 5000:5000 $IMAGE_NAME'
        //         }
        //     }
        // }
    }
}
