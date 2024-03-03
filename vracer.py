import pygame
import random
import time
import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands

# Initialize MediaPipe Hands with a more powerful model
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                       min_tracking_confidence=0.08,model_complexity=1)

distance = (660,360,200,500,400,620)
distance2 = (660,360,200,500,400,620)
distance3 = (660,360,200,500,400,620)
unknown_1= random.choice(distance)
unknown_2 = random.choice(distance2)
unknown_3 = random.choice(distance3)

def boader():
	if bike.left <= 50:
		bike.right += 30
	elif bike.right >= 680:
		bike.left -= 30
pygame.init()

sw = 720
sh = 1280
screen = pygame.display.set_mode((sw ,sh))
road = pygame.image.load("rd.png")
black_car = pygame.image.load("wc.png")
black_car = pygame.transform.scale(black_car,(110,160))
player_bike = pygame.image.load("pl.png")
player_bike = pygame.transform.scale(player_bike,(100,150))
white_car = pygame.image.load("wc.png")
white_car = pygame.transform.scale(white_car,(100,150))
green_car = pygame.image.load("bk.png")
green_car = pygame.transform.scale(green_car,(100,150))
red_car = pygame.image.load("fe.png")
red_car = pygame.transform.scale(red_car,(140,190))
scroll = pygame.transform.scale(road,(730 ,1480))
bike = player_bike.get_rect(topright = [360,850])
car1 = black_car.get_rect(topright = [unknown_1 ,-1500])
car2 = green_car.get_rect(topright = [unknown_2 ,-500])
car3 = red_car.get_rect(topright = [unknown_3,-1000])
i = -1000
touch1 = False
touch2 = False
score = 0
vehicle_speed = 20

clock = pygame.time.Clock()
cap = cv2.VideoCapture(0)


while cap.isOpened():
    
	s,imo = cap.read()
	flipped_image = cv2.flip(imo, 2)
	frame_rgb = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)
    
    # Process the frame with MediaPipe Hands
	results = hands.process(frame_rgb)
 
	hand_label = None
 
	if results.multi_hand_landmarks:
		for hand_landmarks in results.multi_hand_landmarks:
			# Iterate through each hand
			# Detect left or right hand
			if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:
				hand_label = "Left Hand"
			else:
				hand_label = "Right Hand"
    
			cv2.putText(flipped_image, hand_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    
	unknown = random.choice(distance)
	unknown1 = random.choice(distance2)
	notknown2 = random.choice(distance3)
	screen.fill((0,0,0))
	screen.blit(scroll,(0,i))
	screen.blit(scroll,(0,1380+i))
	if i == -100:
		screen.blit(scroll,(0,1380+i))
		i = -1000
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	score += 1
	score_board = pygame.font.Font(None,60)
	load = score_board.render(f"SCORE : {score}",True,"white")

	car1.y += vehicle_speed
	car2.y += vehicle_speed
	car3.y += vehicle_speed
	
	if bike.colliderect(car1) or bike.colliderect(car2) or bike.colliderect(car3):
		
		fr = open("score.txt","r")
		compare = str(fr.read())
		fr.close()
		
		if int(score) >= int(compare):
			
			fn = open("score.txt","w")
			fn.write(str(score))
			
			update = pygame.font.Font(None,60)
			update_score = update.render("Congratulation High Score",True,"green")
			screen.blit(update_score,(120,850))
		
		game = pygame.font.Font(None,80)
		over = game.render("Game over",True,"green")
		screen.blit(over,(200,500))
		final = pygame.font.Font(None,80)
		
		
		pygame.display.update()
		time.sleep(3)
		pygame.quit()
		exit()

	if car1.top >= 1380:
		car1 = black_car.get_rect(topright = [unknown,-100])

	if car2.top >= 1380:
		car2 = green_car.get_rect(topright = [unknown1,-100])
	if car3.top >= 1380:
		car3 = red_car.get_rect(topright = [notknown2,-100])
	if hand_label == 'Right Hand':
		
		bike.x += 15
	elif hand_label == 'Left Hand':
		bike.x -= 15
			
	i += 50
		
	if score >= 1000:
		
		vehicle_speed = 30
		
	fr = open("score.txt","r")
	compare = str(fr.read())
	
	if score >= int(compare):
		
		vehicle_speed = 40
		
	high = pygame.font.Font(None,60)
	high_score = high.render(f"High Score : {compare}",True,"white")
	scoreb = high.render(f"Your Score : {score}",True,"red")
	screen.blit(player_bike,bike)
	screen.blit(black_car,car1)
	screen.blit(green_car,car2)
	screen.blit(red_car,car3)
	screen.blit(high_score,(30,100))
	screen.blit(load,(30,30))
	screen.blit(scoreb,(30,140))
	
	boader()
	cv2.imshow('Hand Detection', flipped_image)
	cv2.resizeWindow('Hand Detection',400,400)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	pygame.display.update()
	clock.tick(15)