pipeline {
   agent any
   stages {
      stage('Verify Branch') {
         steps {
            echo "$GIT_BRANCH"
         }
      }
      stage('Build Docker') {
      steps {
        echo '********* Build Stage Started **********'
        sh '"sudo docker build -t flask-app ."'
        echo '********* Build Stage Finished **********'
        }
    }
      stage('Environment setup') {
      steps {
        echo '********* Build Stage Started **********'
        sh 'export APP_SETTINGS="config.DevelopmentConfig"'
        echo '********* Build Stage Finished **********'
        }
    }
      stage('Run docker') {
      steps {
        echo '********* Deployment Stage Started **********'
        sh "sudo docker run -p 8000:8000 --name flask-app -d flask-app "
        echo '********* Deployment Stage Finished **********'
      }
    }
   }
}