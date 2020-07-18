# serverless deployment
## My Lambda for MobileNet V2
  - https://flte7grm73.execute-api.ap-south-1.amazonaws.com/dev/classify
  - curl -X POST https://flte7grm73.execute-api.ap-south-1.amazonaws.com/dev/classify 'content-type: multipart/form-data' -F =@<file_path>
  - If the above command does not work, use postman as shown in image below.
![](https://github.com/divyanshuraj6815/eva/blob/master/serverless_deployment/assignment-1.png)

## Installations to remember
- Install Latest version for node
- Install serverless
  - npm install -g serverless
- Install and Enable Docker
  - Visit: https://download.docker.com/linux/ubuntu/dists/bionic/pool/stable/amd64/
  - Download these 3 files (you should download latest version, below are the files I used):
      - docker-ce_19.03.9~3-0~ubuntu-bionic_amd64.deb
      - docker-ce-cli_19.03.9~3-0~ubuntu-bionic_amd64.deb
      - containerd.io_1.2.13-2_amd64.deb
  - use sudo dpkg -i containerd.io_1.2.13-2_amd64.deb for example to install containerd... Install all 3
  - sudo systemctl enable docker
  - sudo docker run hello-world
- Install Conda
  - Use this link to install conda
  - https://phoenixnap.com/kb/how-to-install-anaconda-ubuntu-18-04-or-20-04
- Initiate a new environment
  - conda create ––name ml-deployments python=3.8
  - conda activate ml-deployments
  - conda install pytorch==1.5.0 torchvision==0.6.0 cpuonly -c pytorch
- AWS Setup
  - Create IAM user and copy credentials
## Deployment
- serverless plugin install -n serverless-python-requirements
- npm run deploy
