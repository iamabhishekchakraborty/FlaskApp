#!groovy

node  {
      def build_ok = true
      def currentResult = ''
      def app
      def registry = "iamabhishekdocker/flask-app"
      def registryCredential = 'docker-hub-credentials'
      def project_id = 'pyweb-flask-project'
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
                    app = docker.build("iamabhishekdocker/flask-app:${env.BUILD_NUMBER}")
                    echo '********* Build Stage Finished **********'

                    currentResult = currentBuild.result
                    echo "docker build result: ${currentResult}"
          }

          stage('Unit Test Application') {
                // docker.image('qnib/pytest')
                app.inside {
                    sh 'make test_pytest'
                    sh 'make test_unittest'
                    sh 'py.test --verbose --junit-xml test-reports/unit_tests.xml tests/functional/test_flaskapp.py'
                    sh 'python3 -m pytest --verbose --junit-xml test-reports/unit_tests.xml'
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
                        stage('Sleeping') {
                            sleep 30
                        }
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
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        build_ok = false
        echo e.toString()
        throw e
      }
      finally {
            echo '********* Build Completed, Send Notification about Status**********'
            // Success or failure, always send notifications
            notifyBuild(currentBuild.result)
            echo "current build status: ${currentBuild.result}"
      }

      if(build_ok) {
        currentBuild.result = "SUCCESS"
      } else {
        currentBuild.result = "FAILED"
      }
}

def notifyBuild(String buildStatus) {
  echo '********* Sending Notification about Status Started**********'
  echo "current build status: ${buildStatus}"
  // build status of null means successful
  buildStatus = buildStatus ?: 'SUCCESS'

  // Default values
  def colorName = 'RED'
  def colorCode = '#FF0000'
  def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
  def summary = "${subject} (${env.BUILD_URL})"
  def details = """<p>Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""

  // Override default values based on build status
  if (buildStatus == 'STARTED') {
    color = 'YELLOW'
    colorCode = '#FFFF00'
  } else if (buildStatus == 'SUCCESS') {
    color = 'GREEN'
    colorCode = '#00FF00'
  } else {
    color = 'RED'
    colorCode = '#FF0000'
  }

  // Send notifications
  emailext (
      from: "Jenkins Admin<abhishek.chakraborthy@cesltd.com>"
      subject: subject,
      body: details,
      recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
    )
  echo '********* Sending Notification about Status Finished**********'
}