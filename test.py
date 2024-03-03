import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize MediaPipe Hands with a more powerful model
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Initialize OpenCV VideoCapture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)
    
    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Iterate through each hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Detect left or right hand
            if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:
                hand_label = "Left Hand"
            else:
                hand_label = "Right Hand"
            
            # Display hand label
            cv2.putText(frame, hand_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Hand Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
