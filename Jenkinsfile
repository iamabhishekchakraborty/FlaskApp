pipeline {
   agent any
   stages {
      stage('Verify Branch') {
         steps {
            echo "$GIT_BRANCH"
         }
      }
      stage('Environment setup') {
      steps {
        echo '********* Build Stage Started **********'
        sh 'export APP_SETTINGS="config.DevelopmentConfig"'
        echo '********* Build Stage Finished **********'
        }
    }
      stage('Install requirements') {
      steps {
        echo '********* Build Stage Started **********'
        sh 'pip3 install -r requirements.txt'
        echo '********* Build Stage Finished **********'
        }
    }
    stage('Run script') {
      steps {
        echo '********* Deployment Stage Started **********'
        sh 'python3 app.py'
        echo '********* Deployment Stage Finished **********'
      }
    }
   }
}