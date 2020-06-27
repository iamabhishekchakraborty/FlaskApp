pipeline  {
   agent {
      dockerfile true
   }
   stages {
      stage('Verify Branch') {
         steps {
            echo "$GIT_BRANCH"
            echo "This job was triggered by a Git push to branch: ${env.BRANCH_NAME}"
            sh 'echo $JENKINS_USER'
         }
      }
      stage('Checks') {
         steps {
            sh 'pwd'
            sh 'ls -ltrh'
            sh 'docker info'
            sh 'echo ${BUILD_NUMBER}'
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
        sh "docker run -p 5000:5000 --name flask-app -d flask-app "
        echo '********* Deployment Stage Finished **********'
      }
    }
   }
}