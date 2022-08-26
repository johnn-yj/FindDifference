from cgitb import reset
import os ,time
import pyautogui
import cv2
from PIL import ImageChops

#왼쪽(원본) 이미지 시작좌표
# (0,19)
#오른쪽(비교대상) 이미지 시작 좌표
# (803 , 19 )
#이미지 크기 width 796
#height 636
while True:
    result = pyautogui.confirm('틀린그림찾기', buttons=['시작','종료'])
    if result == '종료':
        break # 프로그램 종료 
    
    width, height = 956 , 740
    y_pos = 45
    src = pyautogui.screenshot(region=(0 , y_pos, width , height))
    #src.save('src.jpg')
    dest = pyautogui.screenshot(region=(964 , y_pos, width , height))
    #dest.save('dest.jpg')
    diff = ImageChops.difference(src, dest)

    diff.save('diff.jpg')

    while not os.path.exists('diff.jpg'):
        time.sleep(1)



    #src_img = cv2.imread('src.jpg')
    #dest_img = cv2.imread('dest.jpg')
    diff_img = cv2.imread('diff.jpg')


    gray = cv2.cvtColor(diff_img , cv2.COLOR_BGR2GRAY) #차이점 이미지에서 틀린점 BGR컬러 -> 흑백 변환 
    gray = (gray > 25)*gray # 전체이미지 윤곽 잡히는 경우 해결 

    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # return값이 2개지만 뒤에 값은 받지 않을 예정 / EXTERNAL 로 외각선만 추출

    COLOR = (0, 200, 0) # BGR 기준 G 200 -> 녹색
    for cnt in contours:
        if cv2.contourArea(cnt)>100: # 약 1픽셀 크기 외곽선 제거
            x, y, widht, height = cv2.boundingRect(cnt)
            #cv2.rectangle(src_img, (x,y), (x + widht, y + height), COLOR, 2)
            #cv2.rectangle(dest_img, (x,y), (x + widht, y + height), COLOR, 2)
            #cv2.rectangle(diff_img, (x,y), (x + widht, y + height), COLOR, 2)

            to_x = x + (width // 2) - 490 # 기존 픽셀 문제로 x값 490 빼줌
            to_y = y + (height // 2) + y_pos
            pyautogui.moveTo(to_x , to_y , duration = 0.15)
            pyautogui.click(to_x,to_y)
    result = pyautogui.confirm('틀린그림찾기', buttons=['시작','종료'])
    if result == '종료':
        break # 프로그램 종료
    #cv2.imshow('src', src_img)
    #cv2.imshow('dest', dest_img)
    #cv2.imshow('diff', diff_img)

    #cv2.waitKey(0) 
    #cv2.destroyAllWindows()
