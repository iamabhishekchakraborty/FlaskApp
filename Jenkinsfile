node  {
      def build_ok = true
      def currentResult = 'SUCCESS'

      stage ('Git Checkout') {
            checkout scm
      }

      stage('Initialize') {
            def dockerHome = tool 'gcp-docker'
            env.PATH = "${dockerHome}/bin:${env.PATH}"
      }

      stage('Verify Branch') {
            sh 'echo $GIT_BRANCH'
            echo "This job was triggered by a Git push to branch: ${env.BRANCH_NAME}"
            sh 'echo $JENKINS_USER'
            sh 'echo ${BUILD_NUMBER}'
            sh 'echo ${BUILD_TAG}'
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
      finally {
            echo '********* Unit Test Application Test Report **********'
            sh  ''' source activate ${BUILD_TAG}
                    python3 -m pytest --verbose --junit-xml test-reports/unit_tests.xml
                '''
            always {junit allowEmptyResults: true, testResults: 'test-reports/unit_tests.xml'}
            currentResult = currentBuild.result
            sh 'echo $currentResult'
            echo '********* Finished **********'
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

      if(build_ok) {
        currentBuild.result = "SUCCESS"
      } else {
        currentBuild.result = "FAILURE"
      }
}