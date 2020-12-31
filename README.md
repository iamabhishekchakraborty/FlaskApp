# FlaskApp

1. push changes (and commit) to git
   - create new branch with name <test>, adding all of the changes that you have made in master branch to this new branch
		```bash
		git checkout -b <test> origin/master
		git add .
		git commit -m "<comments for the changes made>"
		```
   - creates your <test> on origin which is being followed with your branch. The -u is the same as --set-upstream
		```bash
		git push -u origin <test>
		```
2. jenkins builds and tests the changes 
3. if test passes jenkins pushes the code to master branch
		```bash
		git checkout test
		git pull
		git checkout master
		git pull origin master
		git merge --no-ff --no-commit test
		git status
		git commit -m 'merge test branch'
		git push origin master
		```
	Note: if the entire git operation is to be carried out by sh script need to make the script executable.
		```bash
		git update-index --chmod=+x scripts/pull-merge-push-gitbranch.sh   
		git commit -m "<comments>"
		git ls-files --stage (just to verify the chmod changes)
		git push -u origin <test branch>
		```  
4. deploy docker image to site servers 
5. send notification once the jenkins build is completed with the outcome of the build

# Set up Jenkins on Google Compute Engine so that it will be available on static IP
Steps to create GCE Virtual Machine
1. Enter the name of instance
2. Set region and zone
3. Machine configuration — Machine Family: General-Purpose; Generation: First; Machine type: n1-standard-1 (change according to number of services it's required to run)
4. Boot Disk — Ubuntu 18.04 LTS; Boot disk type: Standard Persistent disk
5. Firewall — check both allow HTTP traffic, allow HTTPS traffic
6. Networking, tab enter http-server,https-server in Network tag(network tag assign on VM to apply firewall on particular VM)
7. On the security tab, check SSH Keys-Block project-wide SSH keys and enter the entire key data generated
Link - https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#gcloud-or-api
Hit Create. It will take a couple of minutes to create a VM


# Creating Firewall rules - to control incoming or outgoing traffic to an instance. By default, incoming traffic from outside your network is blocked.
1. Go to Firewall under VPC network in Networking section of navigation and create a firewall with the following values:
2. Enter the name of the firewall as you want
3. Ensure the network, priority, direction of traffic, action on match, targets is the default, 1000, ingress, allow and specified target tags respectively.
4. For Target tags — enter http-server,https-server
5. For Source filter — IP ranges and 0.0.0.0/0 in Source IP ranges(Traffic is only allowed from sources within these IP address ranges)
6. For Protocols and ports — Specified protocols and ports must be selected and then check tcp and enter 8080
7. Hit Create

# Install & Run Jenkins
1. SSH to the VM
2. Jenkins is Java coded, we need to install Java first
		```bash
		sudo apt update
		sudo apt install openjdk-8-jdk
		```
   - Confirm the installation of Java
		```bash
		java -version
		```   
3. Add repository key to the system which we do by importing the GPG keys of the Jenkins
    wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
    Now to verify that it worked, run this command to list the keys added
		```bash
		apt-key list
		```
4. Append the Debian package repository address to the server’s sources.list 
    deb https://pkg.jenkins.io/debian-stable binary/
		```bash
		sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
		```
5. Install Jenkins package
		```bash
		sudo apt update
		sudo apt install jenkins
		``` 
6. Start Jenkins  
		```bash
		sudo systemctl start jenkins
		```
7. Command for verification that Jenkins started successfully
		```bash
		sudo systemctl status jenkins
	    ```
8. Adjust our firewall rules so that we can reach it from a web browser
		```bash
		sudo ufw enable (enable ufw)
		```
9. Jenkins runs on the port 8080, so let’s open that port using ufw  
		```bash
		sudo ufw allow 8080
		```
10. Check ufw’s status to confirm the new rules:
		```bash
		sudo ufw status
		```    
11. Open enter https://<External_IP of instance>:8080 in browser 
    or run curl -vvv <External_IP of instance>:8080                 

Link - https://www.jenkins.io/doc/book/installing/#debianubuntu
Link - https://medium.com/faun/jenkins-on-google-compute-engine-611bd86e295b

## Verify Jenkins Version
1. Go to your /var/lib/jenkins/ there will be a file called config.xml. View the config.xml and there should be a xml entry called:
<version>YourVersionNumber</version>
2. Or from Jenkins home screen, navigate to Manage Jenkins -> About Jenkins. You will see the version number there.

##Note: When you turn UFW on it denies any incoming connection. So, you need to disable it for port 22 and then you will be SSH to your machine again. To do so, you should edit your instance and run a Startup Script.
1. Stop and Edit the instance
2. For Custom metadata option and Click Add item 
3. Type startup-script as a key and Copy and paste the command as a value
		```bash
		#! /bin/bash
		sudo ufw allow 22
		```
4. Reboot the instance


##If you want to run docker as non-root user then you need to add it to the docker group.
1. Create the docker group if it does not exist
    ```bash
    sudo groupadd docker
    ```
2. Add your user to the docker group.
    ```bash
    sudo usermod -aG docker <username>
    ```
3. Run the following command or Logout and login again and run (that doesn't work you may need to reboot your machine first)
    ```bash
    newgrp docker
    ```
4. Verify
    ```bash
    docker run hello-world
    ```

# Setting up Chrome Remote Desktop for Linux on Compute Engine
Steps needed to set up the Chrome Remote Desktop service on a Debian Linux virtual machine (VM) instance on Compute Engine. 
Chrome Remote Desktop allows you to remotely access applications with a graphical user interface from a local computer or mobile device
1. Create a headless Compute Engine VM instance to run Chrome Remote Desktop on.
2. Install and configure the Chrome Remote Desktop service on the VM instance.
3. Set up an X Window System desktop environment in the VM instance.
4. Connect from your local computer to the desktop environment on the VM instance (https://remotedesktop.google.com/).

Link - https://cloud.google.com/solutions/chrome-desktop-remote-on-compute-engine

# Setting up Google Cloud SDK
##Try installing google-cloud-sdk from anything other than apt to avoid - 
    ERROR: (gcloud.components.update) 
    You cannot perform this action because the Cloud SDK component manager 
    is disabled for this installation.
##Install the Google Cloud SDK, initialize it, and run core gcloud commands from the command-line refer - 
    https://cloud.google.com/sdk/docs/quickstart-linux

# Setting up to deploy docker image to site servers (Heroku)
Containerise Python Flask using Docker and deploy it onto Heroku
Python Flask application can be directly deployed onto Heroku but to have more control and features we will containerise the Python application using Docker and then deploy the Docker container onto Heroku.
This also gives more control over the languages, frameworks, and libraries used to run the app.
Note: key difference from the usual Flask application is we get the port from Heroku. Without this, Heroku would not be able to bind the port
Make sure to have a working Docker installation (eg. docker ps) and that you’re logged in to Heroku (heroku login).
1. Login to Heroku container
	heroku container:login
2. Get code by cloning the python code
	git clone https://github.com/iamabhishekchakraborty/FlaskApp.git
3. create a new Heroku application (Navigate to the app’s directory)
	heroku create <yourappname>
4. create the container onto Heroku (run this from the project folder). Build the image and push to Container Registry - registry.heroku.com	
	ex: heroku container:push <process-type> (make sure that the directory contains a Dockerfile)
	heroku container:push web --app <yourappname>
5. release the container
	heroku container:release web --app <yourappname>

##Pushing an existing image
To push an image to Heroku, such as one pulled from Docker Hub, tag it and push it according to this naming template:
	docker tag <image> registry.heroku.com/<app>/<process-type>
	docker push registry.heroku.com/<app>/<process-type>

Reference - 
https://devcenter.heroku.com/categories/deploying-with-docker
https://devcenter.heroku.com/articles/container-registry-and-runtime
https://medium.com/@ksashok/containerise-your-python-flask-using-docker-and-deploy-it-onto-heroku-a0b48d025e43

	
## License
[MIT](https://choosealicense.com/licenses/mit/)        