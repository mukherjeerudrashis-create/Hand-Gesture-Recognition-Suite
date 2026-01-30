import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.7)

connection_color=mp_draw.DrawingSpec(color=(255,0,0),thickness=2,circle_radius=2)
cap=cv2.VideoCapture(0)

while True:
    success,frame=cap.read()
    if not success:
        break

    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    
    result=hands.process(rgb)
    
    
    # checking for hands:
    if(result.multi_hand_landmarks):
        for id,hand_landmarks in enumerate(result.multi_hand_landmarks):
            # We now get the hand information

            hand_info=result.multi_handedness[id]
            hand_label=hand_info.classification[0].label

            # Now  we draw the hand skeleton :

            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,
                                   connection_drawing_spec=connection_color)

            # now we take the height and width of the frame(for the selected hand):
            h,w,c=frame.shape
           
            # we know that landmark for wrist is 0
            x_wrist=hand_landmarks.landmark[0].x# this is the decimal coordinate
            y_wrist=hand_landmarks.landmark[0].y# the y coordinate is also in decimal
            # converting to pixel coordinates
            cx=int(x_wrist*w)
            cy=int(y_wrist*h)

            # Displaying the hand label on the frame:
            # moving the text a bit above 
            cv2.putText(frame,hand_label,(cx,cy-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)# cy-20 means 20 pixels above the wrist point
    cv2.imshow("Kaunsa haath?",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.realease()
cv2.destroyAllWindows()
    
