# convenient-converter
convert video files to mp3s that are delivered to your email inbox

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