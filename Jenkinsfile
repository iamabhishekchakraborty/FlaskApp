#!groovy

node  {
      def build_ok = true
      def currentResult = 'SUCCESS'
      def app
      def registry = "iamabhishekdocker/flask-app"
      def registryCredential = 'docker-hub-credentials'
      def project_id = pyweb-flask-project
      git url: 'https://github.com/iamabhishekchakraborty/FlaskApp.git'

      try {
          stage ('Git Checkout Source Code') {
                echo "Checking out source code"
                checkout scm
          }

          stage('Verify Branch and Print Env after source checkout') {
                echo "Branch Name: ${env.BRANCH_NAME}"
                echo "This job was triggered by a Git push to branch: "+ env.GIT_BRANCH
                sh 'echo ${USER}'
                sh 'echo ${BUILD_NUMBER}'
                sh 'echo ${BUILD_TAG}'
                sh 'echo ${BUILD_ID}'
                sh 'printenv'
          }

          stage('Initialize') {
                def dockerHome = tool 'gcp-docker'
                env.PATH = "${dockerHome}/bin:${env.PATH}"
          }

          stage('Build Docker') {
                    echo '********* Build Stage Started **********'
                    app = docker.build("gcr.io/"+{project_id}+"/flask-app:${env.BUILD_NUMBER}")
                    echo '********* Build Stage Finished **********'

                    currentResult = currentBuild.result
                    sh 'echo ${currentResult}'
          }

          stage('Unit Test Application') {
                // docker.image('qnib/pytest')
                app.inside {
                    sh 'make test_pytest'
                    sh 'make test_unittest'
                    sh 'py.test --verbose --junit-xml test-reports/unit_tests.xml tests/functional/test_flaskapp.py'
                    sh  'python3 -m pytest --verbose --junit-xml test-reports/unit_tests.xml'
                }
                // sh 'py.test --verbose --junit-xml test-reports/unit_tests.xml tests/functional/test_flaskapp.py'
                // sh  'python3 -m pytest --verbose --junit-xml test-reports/unit_tests.xml'
                // Archive unit tests for the future
                always {junit allowEmptyResults: true, fingerprint: true, testResults: 'test-reports/unit_tests.xml'}
                echo '********* Finished **********'
          }

          stage('Push Docker Image') {
                echo '********* Pushing docker image to docker hub **********'
                docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        app.push("${env.BUILD_NUMBER}")
                        // app.push("latest")
                }
                echo '********* Finished **********'
          }

          stage ('Push code to Master branch') {
                echo '********* Pushing latest code to master branch (git) Started **********'
                //sh 'make pull-merge-push'
                sshagent (credentials: ['github-jenkins-sshkey']) {
                    sh """git remote set-url origin git@github.com:iamabhishekchakraborty/FlaskApp.git
                          git checkout test
                          git pull
                          git checkout master
                          git pull origin master
                          git merge test
                          git status
                          git push origin master
                       """
                }
                echo '********* Finished **********'
          }

          stage ('Deploy') {
                echo '********* Deployment Stage Started **********'
                app.inside() {
                    echo "inside docker"
                    sh "hostname"
                    //sh 'make run TAG=${env.BUILD_NUMBER}'
                    timestamps {
                        stage "Sleeping"
                        sleep 60
                    }
                }
                //container('gcloud') {
                //    sh "gcloud compute zones --help"
                //}
                echo '********* Deployment Stage Finished **********'
          }

          stage ('Cleanup') {
                echo '********* Cleanup environment Started **********'
                echo '********* Cleanup environment Finished **********'
          }
      }
      catch(e) {
        build_ok = false
        echo e.toString()
      }
      finally {
            echo '********* Build and Test Success, Send Notification **********'
            success{
            mail to: 'abhishek.chakraborthy@cesltd.com'
                subject: "SUCCESSFUL: Build ${env.JOB_NAME}",
                body: "Build Successful ${env.JOB_NAME} build no: ${env.BUILD_NUMBER}\n\nView the log at:\n ${env.BUILD_URL}\n\nBlue Ocean:\n${env.RUN_DISPLAY_URL}"
        }
      }

      if(build_ok) {
        currentBuild.result = "SUCCESS"
      } else {
        currentBuild.result = "FAILURE"
      }
}