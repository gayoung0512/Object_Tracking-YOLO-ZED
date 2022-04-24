# object_tracking & speed estimation using Zed cam

Zed
-------------
Zed : camera that reproduces the way human vision works

It captures high-definition 3D video with a wide field of view and outputs two synchronized left and right video streams in side-by-side format on USB 3.0
- Depth Sensing
- Positional tracking overview
- Spatial Mapping Overview
- 
ZED는 깊이 및 위치 추적 시 ROS(Robot Operating System) 등을 사용함.

### 1) Object Detection by Yolo

Yolo V3 & Coco.names 사용
-> loaded_loc: save list_ball_location
calculate v_inst

### 2) Object Detection Using color : 색 추출 기반 속도 측정

-> loaded_loc: save list_ball_location 
calculate v_inst

=> Zed cam: 화면 분할
