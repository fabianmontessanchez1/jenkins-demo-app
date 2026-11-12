pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  namespace: jenkins
spec:
  serviceAccountName: jenkins-agent-sa
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command: ['tail']
    args: ['-f', '/dev/null']
    volumeMounts:
    - name: aws-creds
      mountPath: /root/.aws
  - name: kubectl
    image: amazon/aws-cli:latest
    command: ['tail']
    args: ['-f', '/dev/null']
  volumes:
  - name: aws-creds
    emptyDir: {}
'''
        }
    }
    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '233036212796.dkr.ecr.us-east-1.amazonaws.com'
        IMAGE_NAME = 'jenkins-demo-app'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout Código') {
            steps {
                echo "Código fuente sincronizado correctamente en el workspace."
            }
        }
        stage('Pruebas Unitarias') {
            steps {
                container('kubectl') {
                    sh 'echo "Ejecutando pruebas unitarias de la aplicación..."'
                    // Aquí agregarías tus comandos de test, por ejemplo: pytest o npm test
                }
            }
        }
        stage('Construir y Subir Docker Image a ECR') {
            steps {
                container('kaniko') {
                    sh """
                    /kaniko/executor --context=dir://. \
                        --dockerfile=Dockerfile \
                        --destination=${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
                        --destination=${ECR_REGISTRY}/${IMAGE_NAME}:latest \
                        --no-push-cache
                    """
                }
            }
        }
        stage('Desplegar en EKS') {
        steps {
            container('kubectl') {
                sh """
                # Descargar e instalar kubectl en el contenedor de AWS CLI
                curl -sLO "https://dl.k8s.io/release/\$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                chmod +x kubectl
                mv kubectl /usr/local/bin/

                # Configurar kubeconfig, actualizar imagen y desplegar
                aws eks update-kubeconfig --region us-east-1 --name jenkins-cicd-cluster
                sed -i 's|image:.*|image: ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|g' k8s/deployment.yaml
                kubectl apply -f k8s/deployment.yaml
                """
            }
        }
    }
    }
    post {
        success {
            echo "¡Pipeline ejecutado exitosamente! Desplegado en EKS con la versión ${IMAGE_TAG}"
        }
        failure {
            echo "El pipeline falló durante la ejecución."
        }
    }
}