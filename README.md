# Promethues server and a webapp deployment 

### Environment Setup
 - You would need ansible, git ,aws cli, eksctl, kubectl, docker, iam-authenticator installed.
 - Do aws configure with user credentials towards your aws account.
 - $(aws ecr get-login --no-include-email --region eu-west-1) to get access to ECR repository which was manually created.

### Deploy AWS EKS cluster
 
   ```` 
   eksctl create cluster --name website --version 1.12 --nodegroup-name standard-workers --node-type t3.medium --nodes 1 --nodes-min 1 --nodes-max 2 --node-ami auto
   ````
### Build and Deploy webapp

   ````
   cd website
   docker-compose build
   docker tag website:latest 851966755265.dkr.ecr.eu-west-1.amazonaws.com/sumit:website
   docker push 851966755265.dkr.ecr.eu-west-1.amazonaws.com/sumit:website
   kubectl create -f template.yml 
   ````
   ````
    kubectl get service  
   ````  
   Fetch the EXTERNAL-IP column from your webapp and paste that in server/promethues.yml.

### Deploy Promethues Server
   ````
   cd server
   docker-compose build
   docker tag promserver:latest 851966755265.dkr.ecr.eu-west-1.amazonaws.com/sumit:promserver
   docker push 851966755265.dkr.ecr.eu-west-1.amazonaws.com/sumit:promserver
   ansible-playbook deploy-cf.yaml
   ````
### Endpoints

 Prometheus server is available at. 
   - http://proms-Publi-1HYRY587Z4WJ0-45323218.eu-west-1.elb.amazonaws.com

 Webapp is available at. 
   - http://a4e4af28b8a2011e9a5770a8942135dc-312107872.eu-west-1.elb.amazonaws.com/metrics
   - http://a4e4af28b8a2011e9a5770a8942135dc-312107872.eu-west-1.elb.amazonaws.com/homersimpson
   - http://a4e4af28b8a2011e9a5770a8942135dc-312107872.eu-west-1.elb.amazonaws.com/covilha
   
### Decisions Involved in the infrastructure.
  - Used kubectl and eksctl to do the heavy lifing for deploying the containers.
  - Used ansible to set the cloudformation stacks yaml for the promethues server.
  - Reused the vpc and subnets from the eks cluster deployment to just save some time.
  - I tried to get a static ip for the webapp but it seemed bit hard on AWS because it supports classic load balancer by default 
    which didnt support static ip. Tried using nlb with the beta support ``service.beta.kubernetes.io/aws-load-balancer-type: "nlb" `` 
    but it seemed to not get the health checks correct. I fixed that by setting  ``.spec.externalTrafficPolicy to Local ``.
    But even when the health check was ok the traffic didnt reach the container.
  - Used AWS because i have only used that.  
