import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.7)
cap=cv2.VideoCapture(0)

green=mp_draw.DrawingSpec(color=(0,255,0),thickness=3,circle_radius=5)
# Finger tip landmarks :
tip_ids=[4,8,12,16,20]

while True:
  success,frame=cap.read()
  if not success:
    break
  frame=cv2.flip(frame,1)
  rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
  result=hands.process(rgb)
  finger=[]

  if(result.multi_hand_landmarks):
    
    for id , hand_landmarks in enumerate(result.multi_hand_landmarks):
            hand_info=result.multi_handedness[id]
            hand_label=hand_info.classification[0].label

            # Drawing the hand skeleton :
            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,connection_drawing_spec=green)
            if(hand_label=="Right"):
                lm_list=[]
                for i ,lm in enumerate(hand_landmarks.landmark):
                    h,w,c=frame.shape
                    cx=int(lm.x*w)
                    cy=int(lm.y*h)
                    lm_list.append((cx,cy))
                # For right hand thumb:
                if lm_list[tip_ids[0]][0]<lm_list[tip_ids[0]-1][0]:
                    finger.append(1)
                else:
                    finger.append(0)
                # For other 4 fingers:
                for j in range(1,5):
                    if lm_list[tip_ids[j]][1]<lm_list[tip_ids[j]-2][1]:
                        finger.append(1)
                    else:
                        finger.append(0)
            elif(hand_label=="Left"):
                lm_list=[]
                for i ,lm in enumerate(hand_landmarks.landmark):
                    h,w,c=frame.shape
                    cx=int(lm.x*w)
                    cy=int(lm.y*h)
                    lm_list.append((cx,cy))
                # For left hand thumb:
                if lm_list[tip_ids[0]][0]>lm_list[tip_ids[0]-1][0]:
                    finger.append(1)
                else:
                    finger.append(0)
                # For other 4 fingers:
                for j in range(1,5):
                    if lm_list[tip_ids[j]][1]<lm_list[tip_ids[j]-2][1]:
                        finger.append(1)
                    else:
                        finger.append(0)
    total_fingers=finger.count(1)
    cv2.putText(frame,f'Fingers :{total_fingers}',(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),5)
  cv2.imshow("Multi Hand Finger Counter",frame)
  if cv2.waitKey(1) & 0xFF==ord('q'):
    break
        
cap.release()
cv2.destroyAllWindows()
            
