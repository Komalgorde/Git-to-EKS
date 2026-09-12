pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
        ECR_URI = '680464296394.dkr.ecr.us-east-1.amazonaws.com/jenkins-fargate'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ECS_CLUSTER     = 'jenkins-fargate-cluster'
        ECS_SERVICE     = 'jenkins-fargate-service'
        ECS_TASK_FAMILY = 'jenkins-fargate-task'
    }
    stages {
        stage('checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Komalgorde/Git-to-ECS.git'
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
        stage('Create New Task Definition') {
    steps {
        sh '''
            aws ecs describe-task-definition \
                --task-definition "$ECS_TASK_FAMILY" \
                --region "$AWS_REGION" \
                --query 'taskDefinition' \
                --output json > task-definition.json

            jq --arg IMAGE "$ECR_URI:$IMAGE_TAG" \
                '.containerDefinitions[0].image = $IMAGE |
                 del(.taskDefinitionArn,
                     .revision,
                     .status,
                     .requiresAttributes,
                     .compatibilities,
                     .registeredAt,
                     .registeredBy)' \
                task-definition.json > new-task-definition.json

            aws ecs register-task-definition \
                --cli-input-json file://new-task-definition.json \
                --region "$AWS_REGION"
        '''
            }
        }
        stage('Deploy to ECS') {
            steps {
                 sh ''' aws ecs update-service \
                    --cluster $ECS_CLUSTER \
                    --service $ECS_SERVICE \
                    --task-definition $ECS_TASK_FAMILY \
                    --region $AWS_REGION

                aws ecs wait services-stable \
                    --cluster $ECS_CLUSTER \
                    --services $ECS_SERVICE \
                    --region $AWS_REGION
                '''
            }
        }
    }
}
