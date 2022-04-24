# object_tracking & speed estimation using Zed cam

Zed
-------------
Zed : camera that reproduces the way human vision works

It captures high-definition 3D video with a wide field of view and outputs two synchronized left and right video streams in side-by-side format on USB 3.0

<img src="https://cdn.stereolabs.com/assets/video/basket-boxes.mp4" width="450px" height="300px" title="px(픽셀) 크기 설정" alt="Spatial_Map"></img><br/>
- Depth Sensing
Depth Map captured by the ZED store a distance value(Z) for each pixel(X,Y) in the image. → expressed in metric units( ex: meters ) and calculated from the back of the left eye of the camera to the scene object

- Positional tracking overview
- Spatial Mapping Overview

비전을 위한 이미지 센서로 듀얼렌즈가 장착된 카메라→ 고화질 3D 비디오를 캡쳐할 수 있고, 깊이 인식이 가능하다.

스테레오 비전 기술을 사용한다. 그렇기에 적외선 RGBD 방식에 비해 강한 햇빛에 영향을 받지 않는다.

ZED2는 최대 40m까지 스캔이 가능하며, ZED는 20m 범위에서 깊이 캡처가 가능하다

depth map 캡쳐 속도는 100FPS (Frame per second)

화각은 최대 90도(H) x 60도(V)

6DOF를 지원한다

ZED는 깊이 및 위치 추적 시 ROS(Robot Operating System) 등을 사용함.

Zed의 이미지 처리와 소프트웨어 실행에는 많은 연산이 필요하므로, 보통 GPU가 장착된 임베디드 컴퓨터 (NVIDIA의 NANO,TX2) 사용
ZED는 깊이 및 위치 추적 시 ROS(Robot Operating System) 등을 사용함.

### 1) Object Detection by Yolo

Yolo V3 & Coco.names 사용
-> loaded_loc: save list_ball_location
calculate v_inst

### 2) Object Detection Using color : 색 추출 기반 속도 측정

-> loaded_loc: save list_ball_location 
calculate v_inst

=> Zed cam: 화면 분할
