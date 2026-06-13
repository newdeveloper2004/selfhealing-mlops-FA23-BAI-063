pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
        IMAGE_UNSTABLE = "areebishaq24/sentiment-api:unstable"
        IMAGE_STABLE = "areebishaq24/sentiment-api:stable"
    }

    stages {
        stage('Fetch') {
            steps {
                checkout scm
            }
        }

        stage('Build and Run') {
            steps {
                sh 'docker build -t sentiment-unstable-local .'
                sh 'docker rm -f sentiment-test-container || true'
                sh 'docker run -d --name sentiment-test-container -p 5000:5000 sentiment-unstable-local'
                sh 'sleep 60'
            }
        }

        stage('Unit Test') {
            steps {
                sh 'docker exec sentiment-test-container pytest tests/test_api.py -v'
            }
        }

        stage('UI Test') {
            steps {
                sh 'docker exec sentiment-test-container pytest tests/test_ui.py -v'
            }
        }

        stage('Build and Push') {
            steps {
                sh 'docker rm -f sentiment-test-container || true'

                sh 'docker build -t $IMAGE_UNSTABLE .'

                sh '''
                rm -rf stable-build
                git clone -b stable-fallback https://github.com/newdeveloper2004/selfhealing-mlops-FA23-BAI-063.git stable-build
                docker build -t $IMAGE_STABLE ./stable-build
                '''

                sh 'echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin'
                sh 'docker push $IMAGE_UNSTABLE'
                sh 'docker push $IMAGE_STABLE'
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                kubectl apply -f k8s/pvc.yaml
                kubectl apply -f k8s/blue-deployment.yaml
                kubectl apply -f k8s/green-deployment.yaml
                kubectl apply -f k8s/service.yaml
                sudo pkill -f port-forward || true
                sudo systemctl restart k8s-portforward
                '''
            }
        }
    }
}
