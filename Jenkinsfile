node  {
      def build_ok = true

      stage ('Git Checkout') {
            checkout scm
      }

      stage('Initialize') {
            def dockerHome = tool 'gcp-docker'
            env.PATH = "${dockerHome}/bin:${env.PATH}"
      }

      stage('Verify Branch') {
            echo "$GIT_BRANCH"
            echo "This job was triggered by a Git push to branch: ${env.BRANCH_NAME}"
            sh 'echo $JENKINS_USER'
            sh 'echo ${BUILD_NUMBER}'
      }

      try {
          stage('Build Docker') {
                echo '********* Build Stage Started **********'
                def app
                app = docker.build("flask-app")
                echo '********* Build Stage Finished **********'
          }
      }
      catch(e) {
        build_ok = false
        echo e.toString()
      }

      stage('Push Docker Image') {
            echo '********* Pushing docker image to docker hub **********'
            echo '********* Finished **********'
      }

      stage ('Deploy') {
            echo '********* Deployment Stage Started **********'
            echo '********* Deployment Stage Finished **********'
      }

      stage('Run docker') {
            echo '********* Deployment Stage Started **********'
            sh "docker run -p 5000:5000 --name flask-app -d flask-app "
            echo '********* Deployment Stage Finished **********'
      }
}