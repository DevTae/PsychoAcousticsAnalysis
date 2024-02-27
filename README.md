### PsychoAcousticsAnalysis

- 프로젝트 설명
  - `Sound Event Detection` + `Visual Feature Extraction` 를 활용한 4D 의자 설계를 진행하는 연구에서, `Sound Event Detection` 에 대한 알고리즘 및 로직을 개발한 Repo 입니다.
  - 소리의 특성 중에서, 소리의 진폭이 크고 작고를 구분하는 `Intensity`, 저음역대 소리의 크기를 계산하는 `Loudness`, 고음역대 소리의 크기를 계산하는 `Sharpness` 속성, 폭발 소리의 크기를 계산하는 `Booming` 으로 나누어집니다.
    - 위 소리의 특성들을 계산하고 그래프로 그려놓은 파일은 `PsychoAcousticsAnalysis 주피터 노트북 파일` 에서 확인할 수 있습니다.
  - 음향 데이터를 각 Feature 별로 나누고, 각 Feature 들에 대하여 `Adaptive Threshold` 를 적용하여 평균 대비 크거나 효과적인 음향을 검출합니다.
    - 추가적으로, `Max Window Function` 을 활용하여 신호에 대한 `Interval` 설정이 가능하도록 구현하여 `Timestamp 별 Event Type` 을 출력하도록 구현하였습니다.
  - `fusion_with_other_effect` 에서는 `Sound` 뿐만 아니라 `Vision` 에서 검출한 이벤트까지 합쳐서 4D 의자에서 실행할 수 있도록 `시간 별 장치 활성화/비활성화 여부`에 대한 데이터를 작성할 수 있게 구성하였습니다.

- 예시 화면
  - Intensity
    ![image](https://github.com/DevTae/PsychoAcousticsAnalysis/assets/55177359/0c9ed9f0-bdc1-4e35-a177-5aa9dc216d74)
 
  - Loudness
    ![image](https://github.com/DevTae/PsychoAcousticsAnalysis/assets/55177359/4376fd8c-cc4b-4f2e-a49b-98e275c3223f)
 
  - Sharpness
    ![image](https://github.com/DevTae/PsychoAcousticsAnalysis/assets/55177359/563791ea-9031-44b0-878a-c92f3f59756d)

  - Booming
    ![image](https://github.com/DevTae/PsychoAcousticsAnalysis/assets/55177359/daec9e3b-450d-474b-99a1-f281638c1a09)

- 참고문헌
  - Yaxuan Li, Yongjae Yoo, Antoine Weill-Duflos, Jeremy Cooperstock, towards Context-aware Automatic Haptic  Effect Generation for Home Theatre Environments, VRST '21, December 2021.
