import cv2
import numpy as np
import time
import math
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

width= cap.get(cv2.CAP_PROP_FRAME_WIDTH) #width 값 받아오기
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#height 값 받아오기
#print(width, height)

#--------------zed 카메라 정보 받기

width=int(width)
height=int(height)
width2=int(width/2)
#cap size 받기

list_ball_location = []
flag=0
t_part=[]
#------------------이미지 분할
while (True):#카메라 이미지를 제대로 불러왔다면 반복문 실행
    ret,img=cap.read()
    img_left = img[1:height,1:width2]
    img_right = img[1:height,width2:width]
    #cv2.imshow('img_left', img_left)
    #cv2.imshow('img_right', img_right)

    # 색을 HSV로 변환
    img_hsv = cv2.cvtColor(img_left, cv2.COLOR_BGR2HSV)
    #cv2.imshow('img_hsv',img_hsv)
#-------------------색 범위 설정
    hue_blue = 120
    # 파란색 범위 설정
    lower_blue = (hue_blue - 20, 100, 120)
    upper_blue = (hue_blue + 20, 255, 255)
    img_mask_blue = cv2.inRange(img_hsv, lower_blue, upper_blue)
#---------------------
    hue_red = 170
    # 빨간 색 범위 설정
    lower_red = (hue_red-20, 50, 50)
    upper_red = (hue_red+20, 255, 255)
    img_mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
#----------------------
    # 노란 색 범위 설정
    lower_yellow = (3, 150, 130)
    upper_yellow = (80, 200, 255)
    img_mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)


    # 구조 요소 생성 (커널의 형태[직사각형],커널의 크기)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

    # 팽창 연산 수행 (원본 배열, 연산 방법, 구조 요소, 고정점, 반복 횟수)

    img_mask_blue = cv2.morphologyEx(img_mask_blue, cv2.MORPH_DILATE, kernel, iterations=3)
    img_mask_red=cv2.morphologyEx(img_mask_red, cv2.MORPH_DILATE, kernel, iterations=3)
    img_mask_yellow = cv2.morphologyEx(img_mask_yellow, cv2.MORPH_DILATE, kernel, iterations=3)

    # 객체 정보 반환
    # nlabels= 객체 수 + 1, labels = 객체 번호가 지정된 레이블 맵
    # stats: N행 5열 - x,y, width, height, area(면적, 픽셀 수), centroid = 무게 중심 좌표
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_mask_yellow)

    max = -1
    max_index = -1
    for i in range(nlabels):  # 객체 수 + 1 만큼 반복
        if i < 1:  # 객체 수가 1보다 작은 경우
            continue
        # 영역의 크기 가져옴
        area = stats[i, cv2.CC_STAT_AREA]

        if area > max:  # 영역 크기 최댓값 저장
            max = area
            max_index = i

    #cv2.imshow('img_right', img_right)
    if max_index != -1:
        if flag==0:
            start = time.time()
        flag=1
        # 중심 좌표,a 외각 사각형에 대한 정보 저장
        center_x = int(centroids[max_index, 0])
        center_y = int(centroids[max_index, 1])
        left = stats[max_index, cv2.CC_STAT_LEFT]
        top = stats[max_index, cv2.CC_STAT_TOP]
        width_detect = stats[max_index, cv2.CC_STAT_WIDTH]
        height_detect = stats[max_index, cv2.CC_STAT_HEIGHT]
        # 영역 외곽에 사각형 그리기, 중심 좌표에 원 그리기
        #print(left, top, width_detect, height_detect)
        cv2.rectangle(img_left, (left, top), (left + width_detect, top + height_detect), (0, 0, 255), 5)
        cv2.circle(img_left, (center_x, center_y), 10, (0, 255, 0), -1)
        loc=np.array([center_x,center_y])
        list_ball_location.append(loc)
        #cv2.rectangle(img_right, (left, top), (left + width, top + height), (0, 0, 255), 5)
        #cv2.circle(img_right, (center_x, center_y), 10, (0, 255, 0), -1)
        #cv2.imshow('Blue', img_mask_blue)
    cv2.imshow('img_left', img_left)
    key = cv2.waitKey(1)
    if key == 27:  # esc
        end = time.time()
        break
cap.release()
cv2.destroyAllWindows()

np.save('./saved_location_center_zed', list_ball_location)

loaded_loc = np.load('./saved_location_center_zed.npy')


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
plt.title("Plotting 1-D array")
plt.xlabel("X axis - instant speed")
plt.ylabel("Y axis - time")
plt.xlim([0,(length-1)*t_part])
plt.plot(x*t_part, v_inst, color = "blue", marker = "o", label = "Array elements")
plt.legend()
plt.show()
