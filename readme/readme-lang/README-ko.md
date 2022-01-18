AWS 계정

사용되는 것

ECS, elastic container service 

ECR, elastic container registry

EC2, elastic cloud computing

docker, docker desktop

----------------

우선 디스코드 봇과 관련된 파이썬 파일은 나중에

이 개념은 레포지토리에 있는 파일을 모아 도커 이미지로 만들어서 빌드를 한다

그리고 도커 데스크탑을 켜서 빌드를 하고 작동하는지 테스트를 한다.

정상적으로 디스코드 봇이 동작을 하면

AWS에서 계정을 만들고

프로그램적으로 AWS에 로그인을 할 수 있는 IAM - 사용자를 만든다.

ECS, ECR, EC2 권한을 가진 사용자를 만들고

마지막 페이지에서 보여주는 키, 시크릿 키를 저장한다.

저장한 시크릿 키는 깃헙 secrets에 저장한다.

ecs에서 클러스터를 만드는데 로드 벨랜서 없이 만든다.

# ccppoo/discord-bot

Deploy your bot on AWS ECS

This Demo requires exprience of running bot user(a.k.a bot server) with python

This repositoty is a basic template for AWS CI/CD

![diagram](./readme/img/discord-bot-server-cicd-flow.png)

by following this, you could develop bot running 24/7 via CI/CD

## File explainations

### .github/workflows/aws.yml

This file is the key part of CI/CD

After you clone or copy paste this repo, change your component name.

I made every values(name) used in yml as agrs so it could prevent typo

**Before running** `Github Action` you must fill in **Github repo Secrets**

![github secrets](./readme/img/github-secret-page.png)

Once you paste this value, you will not be able to read secret again

Save it some where safe just in case.

required secrets:

1. **AWS_ACCESS_KEY_ID**
   1. access key id, you will get this when making `AWS - IAM - USER`

2. **AWS_SECRET_ACCESS_KEY**
   1. access key id, you will get this when making `AWS - IAM - USER`

3. **AWS_DEFAULT_REGION**
   1. Your AWS region, could check this when you access `AWS - Management Console` (when you are logged in)

![check aws region](./readme/img/check-aws-region.png)

in my case, it's `ap-northeast-2`

4. **DISCORD_BOT_TOKEN**
   1. your bot app token check this at [discord/developers/applications](https://discord.com/developers/applications)

![where you could find bot token](./readme/img/bot-token-at-discord-dev-app.png)

------

you will see 

### Dockerfile

This file is a recipe how to set up environment and run your code

at the bottom, the enrty point, if your main script name is `main.py` then change to `CMD ["python", "main.py"]`

### docker-compose.yml

**This file is used for local test** running on docker desktop

As we are not going to host database in other docker container,

we don't configure other docker images.

Before testing in local enviornment, you should add `env` args in powershell

Make a file named `env-secrets.txt`, you could name whatever you want but don't forget to update `.gitignore`


```txt
# env-secrets.txt

$env:AWS_ACCESS_KEY_ID="<Your IAM USER KEY ID>"
$env:AWS_SECRET_ACCESS_KEY="<Your IAM User Secret Acces Key>"
$env:AWS_DEFAULT_REGION="<Your AWS region>"
$env:AWS_CONTAINER_NAME="<Your ECR Container name>"
$env:DISCORD_BOT_TOKEN="<Your discord bot app token"
```

fill in the requirements, and paste it at powershell(or shell in case of Linux/MacOS)

it will look like this if you are using PowerShell in Windows

![paste env](./readme/img/paste-env-at-ps.png)

then run `docker-compose up --build`

it could take some mintues for installing requirements

If you see `Attaching to my-ecr-demo...`

go check your bot to see it is online

![check bot is online](./readme/img/bot-alive.png)

Then you are ready to deploy at AWS

Once you deployed a bot to AWS, make sure to run test with **test-bot token**

because after releasing your bot will run 24/7 and you'll not want to run same bot user at the same time.

### requirements.txt

Since `pycord` didn't released 2.x.x to pypi we have to pull from repository.

other dependencies will be installed, defined at [pycord/requirements.txt](https://github.com/Pycord-Development/pycord/blob/master/requirements.txt)

### app.py

Main entry point of your bot user.

import your other scripts from `./src`

### aws-task-definition.json

paste from `AWS-ECS-Task Definition`

---

don't need port forwarding, discord bot user is client to discord

and we don't need load balancer (AWS ELB, Elastic Load Balancer)

because pycord(discord.py) is event based

If your bot serves hundreds of server, take account of Auto scaling of **AWS EC2** instance

Change **region** and **ECR name** before running

## License

MIT

Released under [MIT](/LICENSE) by [@ccppoo](https://github.com/ccppoo).

-------

badges used - [michaelcurrin/badge-generator](https://michaelcurrin.github.io/badge-generator/#/)