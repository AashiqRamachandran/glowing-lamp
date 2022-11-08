aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 259881173586.dkr.ecr.us-east-1.amazonaws.com

docker build -t glowing-lamp . --platform=linux/amd64

docker tag glowing-lamp:latest 259881173586.dkr.ecr.us-east-1.amazonaws.com/glowing-lamp:latest

docker push 259881173586.dkr.ecr.us-east-1.amazonaws.com/glowing-lamp:latest

```shell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 259881173586.dkr.ecr.us-east-1.amazonaws.com;docker build -t glowing-lamp .;docker tag glowing-lamp:latest 259881173586.dkr.ecr.us-east-1.amazonaws.com/glowing-lamp:latest

```