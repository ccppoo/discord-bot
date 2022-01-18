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

### branches

[![README - about branches](https://img.shields.io/badge/README-about_branches-2ea44f)](./readme/branches/readme-lang/branches-ko.md) - 한글

# ccppoo/discord-bot

요구사항 : Docker desktop(필수 x), git

AWS ECS에 디스코드 봇을 배포해보세요!

이 데모는 봇 서버를 파이썬으로 구동시킬 수 있는 기본적인 지식을 요구합니다.

이 레포지토리는 AWS CI/CD를 구축하기 위한 기본적인 템플릿입니다.

![diagram](./readme/img/discord-bot-server-cicd-flow.png)

이 레포지토리를 포크(Fork)를 통해서 만들면 CI/CD를 통해 24시간 365일 내내 구동시킬 수 있습니다.

ec2 인스턴스를 사용하기 때문에 프리티어 계정이 아닐 경우 사용량에 따라 한 달에 3$ ~ 5$의 비용이 청구될 수 있습니다.

## 파일 설명

* [.github/workflows/aws.yml](#githubworkflowsawsyml)

* [Dockerfile](#dockerfile)

* [Dockerfile.dev](#dockerfiledev)

* [docker-compose.yml](#docker-composeyml)

* [requirements.txt](#requirementstxt)

* [app.py](#apppy)

* [aws-task-definition.json](#aws-task-definitionjson)

* [License](#license)

### .github/workflows/aws.yml

CI/CD를 위한 필수적인 파일입니다.

AWS ECR, ECS(클러스터, 작업)의 이름이 이 레포지토리와 다른 경우 `aws.yml` 스크립트 내 이름을 수정하시면 됩니다.

오타를 방지하기 위해서 변수명으로 만들었습니다.

`Github Action`을 실행하기 전에 **Github repo Secrets**을 만들어야 합니다.

![github secrets](./readme/img/github-secret-page.png)

Github secrets에 값을 한 번 넣으면, 다시 그 값을 읽어 볼 수 없으므로

다른 파일에 저장하는 것을 추천합니다.

필요한 secrets:

1. **AWS_ACCESS_KEY_ID**
   1. Github Action CI/CD 작업을 하기 위해서 프로그램 접속을 위해서 사용되는 Key 입니다. `AWS - IAM - USER`에서 만들 수 있습니다.

2. **AWS_SECRET_ACCESS_KEY**
   1. Key의 비밀키로 마찬가지로 `AWS - IAM - USER`에서 만들 수 있습니다(사용자를 만들면 key, Secret Access key를 동시에 발급 받습니다)

3. **AWS_DEFAULT_REGION**
   1. 사용하는 AWS 리전입니다. `AWS - Management Console` (한국의 경우 자동으로 ap-northeast-2로 접속하게 될겁니다)

![check aws region](./readme/img/check-aws-region.png)

저의 경우 `ap-northeast-2` 입니다.

4. **DISCORD_BOT_TOKEN**
   1. [discord/developers/applications](https://discord.com/developers/applications)에서 확인할 수 있습니다.

![where you could find bot token](./readme/img/bot-token-at-discord-dev-app.png)

------

### Dockerfile

여러분이 작성한 코드가 작동할 환경을 정의하는 스크립트입니다.

봇이 작성된 도입부(entry) 파일 이름을 바꿀 경우(봇을 실행할 때 `python main.py`라고 할 경우) `CMD ["python", "main.py"]`와 같이 바꾸시면 됩니다.

### Dockerfile.dev

Dockerfile을 로컬에서 실행할 때 사용되는 스크립트입니다.

`Dockerfile.dev`을 사용하는 방법은 `Dockerfile.dev` 내 주석으로 작성했으니, 실행하기 전에 Docker desktop을 실행하고 사용하면 됩니다.

필수적인 것은 아니지만, AWS에 배포하기 전에 먼저 테스트 하는 것을 추천드립니다.

### docker-compose.yml

**AWS ECS**에서 사용되는 스크립트로, `Dockerfile`로 최종 테스트를 하기 위해서 사용되는 스크립트입니다.

일반적으로 **AWS ECS** 데모 영상의 예시에서는 Flask 예시 앱을 작동시키기 위해서 DB 서버 이미지와 같이 정의하는 것이 일반적인데

이번 레포지토리는 DB를 사용하지 않습니다.

docker-compose를 이용해 로컬에서 테스트를 하기전에 쉘(powershell)에서 환경변수를 `env` 정의해야합니다.

`env-secrets.txt` 이름으로 파일을 만드세요

```txt
# env-secrets.txt

$env:AWS_ACCESS_KEY_ID="<Your IAM USER KEY ID>"
$env:AWS_SECRET_ACCESS_KEY="<Your IAM User Secret Acces Key>"
$env:AWS_DEFAULT_REGION="<Your AWS region>"
$env:AWS_CONTAINER_NAME="<Your ECR Container name>"
$env:DISCORD_BOT_TOKEN="<Your discord bot app token"
```

위와 같이 내용을 복사하고, AWS 구성 요소와 디스코드 봇 토큰을 넣으세요.

그리고 `docker-compose up`을 실행하기 전에 복사 붙여넣기를 하면 아래와 같이 보일 겁니다.

![paste env](./readme/img/paste-env-at-ps.png)

그리고 `docker-compose up --build`을 실행하세요

구성 요소를 설치하기 위해 몇 분정도 걸릴 수 있습니다.

`Attaching to my-ecr-demo...`라는 메세지가 보이면 디스코드를 켜서 봇이 온라인이 되어있는지 확인하세요

![check bot is online](./readme/img/bot-alive.png)

정상적으로 작동하면 AWS에 배포할 준비가 된 것입니다.

AWS에 최초로 배포한 이후 반드시 **테스트 용 봇 토큰**을 이용하세요

배포 이후 봇은 24시간 내내 돌아갈 것이기 때문에,

만약 배포용 봇과 똑같은 토큰으로 두 개의 봇 서버가 작동하면 디스코드 서비스 사용에 문제가 일어날 수 있기 때문입니다.

### requirements.txt

Since `pycord` didn't released 2.x.x to pypi we have to pull from repository.

이 레포지토리 예시에서 사용하는 `pycord` 2.0.0 이상의 버전 패키지는 아직 pypi에 출시되지 않았으므로 git을 통해서 패키지를 설치합니다.

git이 설치되어 있지 않았다면 설치 후 진행해주세요.

### app.py

봇이 정의된 스크립트입니다.

`./src`에서 개발후 import를 해서 사용하시면 됩니다.

### aws-task-definition.json

`AWS-ECS-Task Definition`에서 task-definition JSON을 복사해서 붙여넣기를 하면 됩니다.

---

일반적인 ECS Flask를 이용한 데모와 달리 디스코드 봇은 포트 포워딩이나 로드 벨런서(AWS ELB)가 필요하지 않습니다.

봇은 이벤트 기반으로 동작하고, 디스코드 봇은 디스코드 서버의 입장에서 클라이언트이기 때문입니다.

만약 수 백개의 서버에서 운영되는 봇의 경우 EC2 인스턴스의 자동 스케일링 기능에 대해서 살펴보는 것을 추천드립니다.

## License

MIT

Released under [MIT](/LICENSE) by [@ccppoo](https://github.com/ccppoo).

---

badges used - [michaelcurrin/badge-generator](https://michaelcurrin.github.io/badge-generator/#/)