pipeline {
   stages {
      stage('Verify Branch') {
         steps {
            echo "$GIT_BRANCH"
         }
      }
      stage('Build Stage') {
      steps {
        echo '********* Build Stage Started **********'
        sh 'pip install -r requirements.txt'
        echo '********* Build Stage Finished **********'
        }
    }
    stage('Testing Stage') {
      steps {
        echo '********* Test Stage Started **********'
        sh 'python test.py'
        echo '********* Test Stage Finished **********'
      }
    }
    stage('Deployment Stage') {
      steps {
        echo '********* Deployment Stage Started **********'
        sh 'flask run'
        echo '********* Deployment Stage Finished **********'
      }
    }
   }
}