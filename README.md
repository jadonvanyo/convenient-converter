# convenient-converter
convert video files to mp3s that are delivered to your email inbox

## Initialization
Starting this project will require you to create secret.yaml files for each of the following directories:
    -

## Initialize Database

    mysql -u root -p < init.sql

## Drop Database

    mysql -u root -p -e "DROP DATABASE auth"

## Drop User

    mysql -u root -p -e "DROP USER auth_user@localhost"

## Access database

    mysql -u root -p
    use auth;
    SELECT * FROM user;

## Create Docker Image Tag
This can only be done after a Dockerfile has been created and `docker build .` has been run in that directory.

    docker tag [image_id] jadonvanyo/[repo_name]:latest

    > Note: Image ID comes from the end of a build in the following line: writing image sha256:[image_id]

## Push Docker Image

    docker push jadonvanyo/[repo_name]:latest

## Apply all files to k8s
Note: must be in the manifests directory

    kubectl apply -f ./

## Update a Docker Image

    cd [image directory]
    docker build .
    docker tag [image_id] jadonvanyo/[repo_name]:latest
    docker push jadonvanyo/[repo_name]:latest
    kubectl delete -f ./manifests
    kubectl apply -f ./manifests

## Get kubectl pods

    kubectl get pods

## See kubectl logs

    kubectl logs [pod name]

## Test Converter

    curl -X POST http://mp3converter.com/login -u jadon.vanyo@gmail.com:Admin123
    curl -X POST -F 'file=@./test.mkv' -H 'Authorization: Bearer [JWS Token]' http://mp3converter.com/upload

## Scale Down Deployment for Testing

    kubectl scale deployment --replicas=1 [pod name(s)]

>Note: Pod name is like gateway, converter, auth, etc.

## Setup MongoDB

    brew install mongodb-atlas
    atlas setup

Follow steps in the browser to sign up for a mongodb account.

    atlas deployments setup
    use videos

## Connect to the MongoDB Shell

    kubectl exec service/mongo -it -- /bin/bash
    mongosh

## Download the File

    curl --output [filename].mp3 -X GET -H 'Authorization: Bearer [token]' "http://mp3converter.com/download?fid=[fid from email]"

## End Usage
All manifests must be up and running. Must be in the file directory as video

    curl -X POST http://mp3converter.com/login -u jadon.vanyo@gmail.com:Admin123
    curl -X POST -F 'file=@[filename]' -H 'Authorization: Bearer [Token]' http://mp3converter.com/upload
    curl --output [filename].mp3 -X GET -H 'Authorization: Bearer [Token]' "http://mp3converter.com/download?fid=[fid from email]"
