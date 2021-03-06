#!groovy

node() {
      currentBuild.result = "SUCCESS"
      def build_ok = true
      def app
      def registry = "iamabhishekdocker/flask-app"
      def registryCredential = 'docker-hub-credentials'
      def project_id = 'pyweb-flask-project'
      git url: 'https://github.com/iamabhishekchakraborty/FlaskApp.git'

      try {
          stage('Color Encoding') {
            // This displays colors using the 'xterm' ansi color map.
            ansiColor('xterm') {
                // Just some echoes to show the ANSI color.
                stage "\u001B[31mIn Red\u001B[0m Now not"
            }
          }
          stage ('Git Checkout Source Code') {
                // Clean before build
                cleanWs()
                echo "Checking out source code"
                checkout scm
                echo "Building ${env.JOB_NAME}..."
                //sh 'mvn clean install'
                def v = version()
                if (v) {
                    echo "Build Version: ${v}"
                }
                // copy source code from local file system and test
                // for a Dockerfile to build the Docker image
                git ('https://github.com/iamabhishekchakraborty/FlaskApp.git')
                if (!fileExists("Dockerfile")) {
                    error('Dockerfile missing.')
                }
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
                    //currentResult = currentBuild.result
                    echo "docker build result: ${currentBuild.result}"
          }

          stage('Unit Test Application') {
                env.NODE_ENV = "test"
                print "Environment will be : ${env.NODE_ENV}"
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
                            sleep 5
                        }
                    }
                }
                //docker.image("iamabhishekdocker/flask-app:${env.BUILD_NUMBER}").inside {
                //    sh "hostname"
                //}

                //container('gcloud') {
                //    sh "gcloud compute zones --help"
                //}
                // sh './deploy production'
                print "IMAGE: iamabhishekdocker/flask-app:${env.BUILD_NUMBER}"
                sh 'scripts/deploy-docker-heroku.sh iamabhishekdocker/flask-app:${BUILD_NUMBER} myflaskappsite'
                // sh 'make deploy-site-servers TAG=${BUILD_NUMBER}'
                echo '********* Deployment Stage Finished **********'
          }

          stage ('Cleanup') {
                echo '********* Cleanup environment Started **********'
                // deleteDir() /* clean up our workspace */
                // deleteDir does bad things in a docker context at the top level of the WS
                // Basically, docker gets confused because the mounted directory went away
                sh("rm -rf *")
                /*
                sh "docker stop $(docker ps -q)"    // Stop all containers
                sh "docker rm $(docker ps -a -q)"   // Remove all stopped containers
                sh "docker rmi $(docker images -q -f dangling=true)"  // Remove all dangling images
                */
                // sh("docker version")
                sh "docker system prune --all --force"   // Remove all unused containers, networks, images (both dangling and unreferenced), and optionally, volumes
                // sh "docker rmi ${app.id}"           // remove image created by the current build
                echo '********* Cleanup environment Finished **********'
          }
      }
      catch(e) {
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        build_ok = false
        echo "Error description: " + e.toString()
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

def version() {
    def matcher = readFile('Dockerfile') =~ 'FROM(.+)'
    matcher ? matcher[0][1] : null
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
      from: "Jenkins Admin<abhishek.chakraborthy@cesltd.com>",
      subject: subject,
      body: details,
      recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
    )
  echo '********* Sending Notification about Status Finished**********'
}