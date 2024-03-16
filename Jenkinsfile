pipeline {
    agent any

    stages {
        stage('Getting project from Git') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: 'main']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/AlaEddine-Khiari/Asterisk-Logs']]])
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh "mkdir /app/asterisk/recordings/
                    sh "python3 -m unittest Test_Script.py"
                }
            }
        }
      
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t alaeddinekh/asterisk-logs:latest ."
                }
            }
        }

        stage('Push Image To Dockerhub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker_id', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                        sh 'docker push alaeddinekh/asterisk-logs:latest'
                    }
                }
            }
        }
        
        stage('Cleanup Up') {
            steps {
                Script{
                    sh "rm -d /app/asterisk/recordings"
                }
                cleanWs()  
            }
        }
    }

    post {
        success {
            mail to: 'khiarialaa@gmail.com',
                 from: 'zizoutejdin02@gmail.com',
                 subject: 'Build Finished - Success',
                 body: '''Dear Mr Ala, 
                         We are happy to inform you that your pipeline to build Asterisk-Logs Image was successful. 
                         Great work! 
                                         
                         Best regards,
                         -Jenkins Team-'''
        }
        
        failure {
            mail to: 'khiarialaa@gmail.com',
                 from: 'zizoutejdin02@gmail.com',
                 subject: 'Build Finished - Failure',
                 body: '''Dear Mr Ala, 
                         We are sorry to inform you that your pipeline to build Asterisk-Logs Image failed. 
                         Keep working! 

                         Best regards,
                         -Jenkins Team-'''
        }
    }
}
