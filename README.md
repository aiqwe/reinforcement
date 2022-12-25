> <h3> 강화학습 과제 </h3>
- 팀원
  - 김현아(A64027)
  - 서종환(A64041)
  - 이재상(A64058)
- 다음 패키지를 설치해야 합니다.
```
pytorch=1.12.1
kaggle-environments=1.10.3
tqdm=4.64.1
gym=0.21.0
numpy=1.23.4
matplotlib=3.6.2
```
<hr>

다음 명령어를 실행하면됩니다.
```
pip install pytorch kaggle-environments tqdm gym numpy matplotlib
```

> <h3> ./src 디렉토리에는 다음 클래스들이 내장되어있습니다.
- **environment** : ConnectX Environment를 커스터마이징합니다. gym Environment를 상속하여 다루기 쉽도록 하였습니다.
- **dqn** :
  - **Network** : 신경망 Network 클래스입니다.
    - Activation Function은 Descrete한 Action(7개 중 1 컬럼 선택)이므로 tanh 함수를 사용했습니다.
  - **DQN** : Network 클래스를 속성값으로 사용하여 DQN 학습을 모델링합니다.
    - 클래스 내에 Replay Buffer가 함께 정의되어있습니다.
    - Optimization은 Adam을 사용하였습니다.
    - s, a, r, s', done 값을 정의하여 DQN 네트워크에서 학습할 수 있도록 합니다.
- **play** : Episode의 reward, Target / Train Network의 관계등을 정의하는 helper 클래스입니다.
- **agent** : 학습된 DQN 모델의 weight를 Feed Forward하여 Agent를 만듭니다.

<hr></hr>

> <h3> run.ipnyb를 실행하면 Parameter를 조절할 수 있으며, 실제 Agent로 시뮬레이션을 해 볼 수도 있습니다.

<img width="400" alt="parameter" src="https://user-images.githubusercontent.com/95918475/209474146-70e9ca00-6e87-49e5-ab74-81aa2f72047c.png">

model paramter와 parameter dictionary의 hyper parameter를 조절할 수 있습니다.
<br></br>
<img width="400" alt="rewards" src="https://user-images.githubusercontent.com/95918475/209474209-84bca428-a4a6-4187-8a4a-aaea0c82e017.png">

reward 그래프는 총 승리 횟수 / episode 수 입니다. 따라서 승률로 생각해볼 수 있습니다.
<br></br>
![agent](https://user-images.githubusercontent.com/95918475/209474289-4ac4ef67-eee0-4fb8-9da8-18c695a44741.gif)
<br></br>
학습된 모델로 agent를 만들고 kaggle-environments에 내장된 메서드를 사용하여 Random과 대결해볼 수 있습니다.




