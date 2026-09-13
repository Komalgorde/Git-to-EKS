pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
        ECR_URI = '680464296394.dkr.ecr.us-east-1.amazonaws.com/jenkins-ecr'
        IMAGE_TAG = "${BUILD_NUMBER}"
        EKS_CLUSTER     = 'eks-devops-lab'
        EKS_DEPLOYMENT     = 'myapp-deployment'
        EKS_CONTAINER     = 'myapp'
    }
    stages {
        stage('checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Komalgorde/Git-to-EKS.git'
            }
        }
        //stage('Install Dependencies') {
         //   steps {
           //     sh ''' python3 -m venv venv
             //   ./venv/bin/pip install flask '''
            //}
        //}

        // stage('test') {
        //   steps {
        //     sh './venv/bin/python -m py_compile app.py'
        //}
        //}
        //stage('build') {
        //  steps {
        //    sh 'nohup ./venv/bin/python app.py > app.log 2>&1 &'
        //  sleep 5
        //sh 'curl http://localhost:5000'
        //}
        //}
        stage('build docker') {
            steps {
                sh 'docker build -t myapp:$IMAGE_TAG .'
            }
        }
        stage('build image') {
            steps {
                sh 'docker images'
            }
        }
        // stage('run container') {
        //   steps {
        //     sh 'docker rm -f myapp || true'
        //   sh 'docker run -d --name myapp -p 5000:5000 myapp:v1'
        //}
        // }
        stage('Log in ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION |
                docker login --username AWS --password-stdin $ECR_URI
                '''
            }
        }
        stage('Push to ECR..') {
            steps {
                sh '''
                docker tag myapp:$IMAGE_TAG $ECR_URI:$IMAGE_TAG
                docker push $ECR_URI:$IMAGE_TAG
                '''
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                 sh """
                    aws eks update-kubeconfig --name $EKS_CLUSTER --region $AWS_REGION
                    kubectl set image deployment/$EKS_DEPLOYMENT $EKS_CONTAINER=$ECR_URI:$IMAGE_TAG
                    kubectl rollout status deployment/$EKS_DEPLOYMENT
                """
            }
        }
    }
}
