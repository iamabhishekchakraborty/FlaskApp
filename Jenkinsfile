pipeline {
   agent any
   stages {
      stage('Verify Branch') {
         steps {
            echo "$GIT_BRANCH"
            echo "This job was triggered by a Git push to branch: ${env.BRANCH_NAME}"
         }
      }
      stage('Build Docker') {
      steps {
        echo '********* Build Stage Started **********'
        sh '"docker build -t flask-app ."'
        echo '********* Build Stage Finished **********'
        }
    }
      stage('Run docker') {
      steps {
        echo '********* Deployment Stage Started **********'
        sh "docker run -p 8000:8000 --name flask-app -d flask-app "
        echo '********* Deployment Stage Finished **********'
      }
    }
   }
}