import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7)
cap=cv2.VideoCapture(0)
tip_ids=[4,8,12,16,20]
while True:
  ret,frame=cap.read()
  if not ret:
    break
  frame=cv2.flip(frame,1)
  rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
  result=hands.process(rgb)

  if(result.multi_hand_landmarks):
    for hand_landmarks in result.multi_hand_landmarks:
      mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
      lm_list=[]
      for id,lm in enumerate(hand_landmarks.landmark):
        h,w,c=frame.shape
        lm_list.append((int(lm.x*w),int(lm.y*h)))
      fingers=[]
      # Thumb Configuration :

      if lm_list[tip_ids[0]][0]>lm_list[tip_ids[0]-1][0]:
        fingers.append(1)
      else:
        fingers.append(0)
      # Other 4 fingers:

      for id in range(1,5):
        if lm_list[tip_ids[id]][1]<lm_list[tip_ids[id]-2][1]:
          fingers.append(1)
        else:
          fingers.append(0)
      total_fingers=fingers.count(1)
      
      #Displaying the finger count:

      cv2.putText(frame,f'Fingers :{total_fingers}',(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),5)
  cv2.imshow("Finger Counter",frame)
  if cv2.waitKey(1) & 0xFF==ord('q'):
    break
cap.release()
cv2.destroyAllWindows()