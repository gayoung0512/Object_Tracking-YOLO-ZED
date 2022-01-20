import cv2
import numpy as np
import time
import math
import matplotlib.pyplot as plt
from cvlib.object_detection import draw_bbox

#안 되는 경우 물체 하나만 정해서 직접 학습
#YOLO 네트워크 불러오기

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
#weights, cfg 파일 불러와서 yolo 네트워크와 연결
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# YOLO NETWORK 재구성
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
flag=0
list_ball_location=[]
while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape

    # YOLO 입력
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # 검출 신뢰도
            if confidence > 0.5:
                # Object detected
                # 검출기의 경계상자 좌표는 0 ~ 1로 정규화되어있으므로 다시 전처리
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if(label=='donut'):
                if flag == 0:
                    start = time.time()
                flag = 1
                print('donut')
                loc = np.array([center_x, center_y])
                list_ball_location.append(loc)
            score = confidences[i]

            # 경계상자와 클래스 정보 투영
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)

    cv2.imshow("YOLOv3", frame)
    # 1ms 마다 영상 갱신
    if cv2.waitKey(1) > 0:
        end = time.time()
        break


np.save('./saved_location_center_labeling', list_ball_location)

loaded_loc = np.load('./saved_location_center_labeling.npy')

t=end-start
print(f"{t:.5f} sec")
length=len(loaded_loc)
t_part=t/length #초 간격
v_sum=0
dist=[] #거리 저장
v_inst=[] #순간 속도 저장
maxx=0
for i in range(0,length-1):
    dist.append(math.sqrt(pow(loaded_loc[i+1, 0] - loaded_loc[i, 0], 2) + pow(loaded_loc[i+1, 1] - loaded_loc[i, 1], 2)))
    v_sum += dist[i]
    v_inst.append(dist[i]/(t_part*100))
    if(v_inst[i]>maxx):
        maxx=v_inst[i]

v_av=v_sum/(t*100)
print(round(v_av,3))

x = np.array(range(0, length-1))
#plt.figure(figsize=(15,8))
plt.plot(x*t_part, v_inst)
plt.title("using yolo")
plt.xlabel("X axis - instant speed")
plt.ylabel("Y axis - time")
plt.xlim([0,(length-1)*t_part])
plt.plot(x*t_part, v_inst, color = "blue", marker = "o", label = "Array elements")
plt.legend()
plt.show()