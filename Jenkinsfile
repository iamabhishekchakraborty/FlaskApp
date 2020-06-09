pipeline {
   agent any
   stages {
      stage('Verify Branch') {
         steps {
            echo "$GIT_BRANCH"
         }
      }
      stage('Build Stage') {
      steps {
        echo '********* Build Stage Started **********'
        bat 'pip install -r requirements.txt'
        echo '********* Build Stage Finished **********'
        }
    }
    stage('Deployment Stage') {
      steps {
        echo '********* Deployment Stage Started **********'
        bat 'flask run'
        echo '********* Deployment Stage Finished **********'
      }
    }
   }
}