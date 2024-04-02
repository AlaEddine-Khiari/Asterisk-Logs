pipeline {
    agent any
    
    environment {
        PATH = "/usr/lib/jvm/java-17-openjdk-amd64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/vagrant/sonar-scanner-cli-4.6.2.2472-linux/bin:/home/vagrant/sonar-scanner-4.6.2.2472-linux/bin"
    }
    
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
                    sh "dd if=/dev/urandom of=/ext/recordings/test1.wav bs=1024 count=1024"
                    sh "dd if=/dev/urandom of=/ext/recordings/test2.wav bs=1024 count=1024"
                    sh "dd if=/dev/urandom of=/ext/recordings/test3.wav bs=1024 count=1024"
                    // Run unit tests
                    sh 'python3 -m unittest -p "Test_app.py"'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withEnv(["PATH+SONARQUBE_SCANNER=${scannerHome}/bin"]) {
                        sh 'sonar-scanner'
                    }
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
