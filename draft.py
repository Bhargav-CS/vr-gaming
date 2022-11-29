
import cv2
import mediapipe as mp
import math
import pyautogui as pg

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


camera = cv2.VideoCapture(0)
hands = mp_hands.Hands()
pinch_position = []
direction = [0,0]



def getCurrentPosition(landmarks):
    (h , w, c ) = image.shape
    thumb_position = []
    index_position = []
    
    for index, lm in enumerate(landmarks.landmark) :
        if index == 8 :
            index_position = (lm.x * w, lm.y * h)
        if index == 4 :
            thumb_position = (lm.x * w, lm.y * h)
        
    if len(index_position) == 2 and len(thumb_position) == 2:
        return((thumb_position[0] + index_position[0])/2,(thumb_position[1] + index_position[1])/2)
        
    
    return []

def changeDirections(pinch_position, current_position) :
    global slope
    if current_position[0] > pinch_position [0] :
        direction[0] = 1
    elif current_position[0] == pinch_position[0] :
        direction[0] = 0 
    else:
        direction[0] = -1 
    if current_position[1] > pinch_position [1] :
        direction[1] = 1
    elif current_position[1] == pinch_position[1] :
        direction[1] = 0 
    else:
        direction[1] = -1 

def isPinch(landmarks) :
    global pinch_position
    (h , w ,c) = image.shape
    thumb_position = []
    index_position = []
  
    for index, lm in enumerate(landmarks.landmark) :
        if index == 8 :
            index_position = (lm.x * w, lm.y * h)
        if index == 4 :
            thumb_position = (lm.x * w, lm.y * h)

    if len(index_position) == 2 and len(thumb_position) == 2:
        distance = math.dist(index_position,thumb_position)
        if distance <= 25 :
            if len(pinch_position) == 0 :
                pinch_position = ((thumb_position[0] + index_position[0])/2,(thumb_position[1] + index_position[1])/2)
            return True
        else : 
            return False
    else:
        return False

def moveCurser() :
    try :
        x = pg.position().x
        y = pg.position().y

        new_x = x + direction[0] * 8
        new_y = y + direction[1] * 8
        # slope *(-x+new_x )
        pg.moveTo(new_x, new_y)
    except :
        pass

while True :
    _,image = camera.read()
    cimg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(cimg)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            if isPinch(hand_landmarks) :
                # pg.click()
                pg.mouseDown()
                current_position = getCurrentPosition(hand_landmarks)
                changeDirections(pinch_position, current_position)
                moveCurser()
            else:
                pg.mouseUp()
                pinch_position = []
                direction = [0,0]

    cv2.imshow('image', image)


    # cv2.imshow('converted image', cimg)
    if cv2.waitKey(1) == ord('q'):
        break
