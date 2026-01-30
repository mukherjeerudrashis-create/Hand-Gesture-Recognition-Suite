import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.7)
cap=cv2.VideoCapture(0)

# Finger tip landmark IDs:
tip_ids=[4,8,12,16,20] # Thumb, Index, Middle, Ring, Pinky

#This here specifies the drawing style for connections
connection_drawing_spec = mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
while True:
  success,frame=cap.read()
  if not success:
    break
  frame=cv2.flip(frame,1)
  rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) # we convert it to rgb because mediapipe sees RGB only
  result=hands.process(rgb)

  if(result.multi_hand_landmarks):
    for hand_landmarks in result.multi_hand_landmarks:
      mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,connection_drawing_spec=connection_drawing_spec)
      for id, lm in enumerate(hand_landmarks.landmark):
        h,w,c=frame.shape
        cx,cy=int(lm.x*w),int(lm.y*h)
        if id in tip_ids:
          cv2.circle(frame,(cx,cy),7,(255,0,255),cv2.FILLED)

  cv2.imshow("Finger Tip Highlighter",frame) 
  if cv2.waitKey(1) & 0xFF==ord('q'):
    break  
cap.release()
cv2.destroyAllWindows() 