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
                    echo "--- CONTENIDO DEL DIRECTORIO ACTUAL ---"
                    pwd
                    ls -la
                    ls -la ..
                    
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
                    sh "aws eks update-kubeconfig --region ${AWS_REGION} --name jenkins-cicd-cluster"
                    sh "sed -i 's|image:.*|image: ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|g' k8s/deployment.yaml"
                    sh "kubectl apply -f k8s/deployment.yaml"
                    sh "kubectl rollout status deployment/demo-app --timeout=120s"
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