pipeline {
    agent any

    stages {
        stage('Switch Traffic to Stable (Green)') {
            steps {
                sh '''
                kubectl patch service sentiment-api-service -p '{"spec":{"selector":{"app":"sentiment-api","slot":"green"}}}'
                sudo pkill -f port-forward || true
                sudo systemctl restart k8s-portforward
                '''
            }
        }
    }
}
