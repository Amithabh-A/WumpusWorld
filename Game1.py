import pygame
import os
import boards
import math
import Config
import time
pygame.init()
PI=math.radians(180)
print("SSS")
ob=Config.config1()
WIDTH,HEIGHT=(900,600)
screen=pygame.display.set_mode([WIDTH,HEIGHT])
WIN = pygame.Surface(screen.get_size())
pygame.display.set_caption("WUMPUS GAME")
RED=(255,0,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
COL=(0,0,128)
VEL=1
FPS=120 ##To have a definite speed for game
num1=(HEIGHT)//30
num2=(WIDTH-300)//30
WUMPUS_IMG=pygame.image.load(os.path.join('Agents','Wumpus.jpg'))
WUMPUS_IMG=pygame.transform.scale(WUMPUS_IMG,(num2*2,num1*2))

PIT_IMG=pygame.image.load(os.path.join('Agents','pit.png'))
PIT_IMG=pygame.transform.scale(PIT_IMG,(num2*2,num1*2))

PLAYER_IMG=pygame.transform.scale(pygame.image.load(os.path.join('Agents','Player.jpg')),(num2*2,num1*2))
GOLD_IMG=pygame.transform.scale(pygame.image.load(os.path.join('Agents','Gold.png')),(num2*2,num1*2))
buffer_surface = pygame.Surface(WIN.get_size())
actions_allowed=[False,False,False,False] ##left,right,up,down

textfont=pygame.font.SysFont("monospace",15)
textfont2=pygame.font.SysFont("monospace",30)
VISIBLITY=0
GameOver=False
GOLDS=len(ob.reward_pos)
FLAG=False
CURRENT_POS=13
VISITED={1:False,2:False,3:False,4:False,5:False,6:False,7:False,8:False,9:False,10:False,11:False,12:False,13:False,14:False,15:False,16:False}
AWARE={1:False,2:False,3:False,4:False,5:False,6:False,7:False,8:False,9:False,10:False,11:False,12:False,13:False,14:False,15:False,16:False}
VISITED[13]=True
AWARE[13]=True
if VISIBLITY==1:#1 mean all states are known to the agent. 0 mean agent knows nothing. 
    for i in AWARE:
        AWARE[i]=True
Labels_l={1:(40,40),2:(160,40),3:(280,40),4:(400,40),5:(40,160),6:(160,160),7:(280,160),8:(400,160),9:(40,280),10:(160,280),11:(280,280),12:(400,280),13:(40,400),14:(160,400),15:(280,400),16:(400,400)}
Labels_l1={}
for integ in Labels_l:
    Labels_l1[integ]=(Labels_l[integ][0],Labels_l[integ][1]+20)

posi={1:(80,80),2:(200,80),3:(320,80),4:(440,80),5:(80,200),6:(200,200),7:(320,200),8:(440,200),9:(80,320),10:(200,320),11:(320,320),12:(440,320),13:(80,440),14:(200,440),15:(320,440),16:(440,440)}


def player_movement(keys_pressed,player,turns):
        global SCORE
        if keys_pressed[pygame.K_a] and turns[1]==True: #left
            player.x-=VEL
            SCORE-=1
        if keys_pressed[pygame.K_d] and turns[0]==True: #right
            player.x+=VEL
            SCORE-=1
        if keys_pressed[pygame.K_w] and turns[2]==True: #up
            player.y-=VEL
            SCORE-=1
        if keys_pressed[pygame.K_s] and turns[3]==True: #down
            player.y+=VEL
            SCORE-=1
def wumpus_movement(keys_pressed,player):
        if keys_pressed[pygame.K_LEFT]: #left
            player.x-=VEL
        if keys_pressed[pygame.K_RIGHT]: #right
            player.x+=VEL
        if keys_pressed[pygame.K_UP]: #up
            player.y-=VEL
        if keys_pressed[pygame.K_DOWN]: #down
            player.y+=VEL

SCORE=0


def draw_board(lvl):
    global num1,num2,num3,WIN,COL,PI
    for i in range (len(lvl)):
        for j in range (len(lvl[i])):
            if lvl[i][j]==1:
                pygame.draw.line(WIN,COL,(j*num2+(0.5*num2),i*num1),(j*num2+(0.5*num2),i*num1+num1),3)


            if lvl[i][j]==2:
                pygame.draw.line(WIN,COL,(j*num2,i*num1+(0.5*num1)),(j*num2+num2,i*num1+(0.5*num1)),3)

            if lvl[i][j]==3:
                pygame.draw.arc(WIN,COL,[(j*num2-(0.5*num2)),(i*num1+(0.5*num1)),num2,num1],0,PI/2,3)
            if lvl[i][j]==4:
                pygame.draw.arc(WIN,COL,[(j*num2+(0.5*num2)),(i*num1+(0.5*num1)),num2,num1],PI/2,PI,3)
            if lvl[i][j]==5:
                pygame.draw.arc(WIN,COL,[(j*num2+(0.5*num2)),(i*num1-(0.5*num1)),num2,num1],PI,3*PI/2,3)
            if lvl[i][j]==6:
                pygame.draw.arc(WIN,COL,[(j*num2-(0.5*num2)),(i*num1-(0.5*num1)),num2,num1],3*PI/2,0,3)
   
def draw_player(player):
    global ob,posi,WUMPUS_IMG,PIT_IMG,DIRECTION,WIN
    if DIRECTION==0:##RIGHT
        
        WIN.blit(pygame.transform.flip(PLAYER_IMG,True,False),(player.x,player.y))
    elif DIRECTION==1:##LEFT

        WIN.blit(PLAYER_IMG,(player.x,player.y))
    elif DIRECTION==2:##UP
        WIN.blit(pygame.transform.rotate(PLAYER_IMG,270),(player.x,player.y))
    elif DIRECTION==3:##DOWN
        WIN.blit(pygame.transform.rotate(PLAYER_IMG,90),(player.x,player.y))
DIRECTION=0
num3=20
def check_pos(player,centrex,centrey):
    turns=[False,False,False,False]
    global num2,num1,num3
    ##print(centrex,centrey)
    
    collide=0
    
    if (centrex+2*num3<23*num2)and (((centrey>1.5*num2) and (centrey+2*num3<5.5*num2)) or ((centrey>8.5*num2) and (centrey+2*num3<11.5*num2)) or ((centrey>14.5*num2) and (centrey+2*num3<17.5*num2)) or((centrey>20.5*num2) and (centrey+2*num3<23.5*num2))):
        
        turns[0]=True

    if (centrex-num3>2*num2) and (((centrey>1.5*num2) and (centrey+2*num3<5.5*num2)) or ((centrey>8.5*num2) and (centrey+2*num3<11.5*num2)) or ((centrey>14.5*num2) and (centrey+2*num3<17.5*num2)) or((centrey>20.5*num2) and (centrey+2*num3<23.5*num2))):
        
        turns[1]=True
    if (centrey+2*num3<23*num2) and (((centrex>1.5*num2) and (centrex+2*num3<5.5*num2)) or ((centrex>8.5*num2) and (centrex+2*num3<11.5*num2)) or ((centrex>14.5*num2) and (centrex+2*num3<17.5*num2)) or((centrex>20.5*num2) and (centrex+2*num3<23.5*num2))):
        
        turns[3]=True

    if (centrey-num3>2*num2) and (((centrex>1.5*num2) and (centrex+2*num3<5.5*num2)) or ((centrex>8.5*num2) and (centrex+2*num3<11.5*num2)) or ((centrex>14.5*num2) and (centrex+2*num3<17.5*num2)) or((centrex>20.5*num2) and (centrex+2*num3<23.5*num2))):
        turns[2]=True
        '''for i in range(9):
        if pygame.Rect.colliderect(player,rects[i]):
            turns[DIRECTION]=False'''
 
        
        
    return turns
BOUNDARY={1:(1.5*num2,5.5*num2,1.5*num2,5.5*num2),2:(8.5*num2,11.5*num2,1.5*num2,5.5*num2),3:(14.5*num2,17.5*num2,1.5*num2,5.5*num2),4:(20.5*num2,23.5*num2,1.5*num2,5.5*num2),
          5:(1.5*num2,5.5*num2,8.5*num2,11.5*num2),6:(8.5*num2,11.5*num2,8.5*num2,11.5*num2),7:(14.5*num2,17.5*num2,8.5*num2,11.5*num2),8:(20.5*num2,23.5*num2,8.5*num2,11.5*num2),
          9:(1.5*num2,5.5*num2,14.5*num2,17.5*num2),10:(8.5*num2,11.5*num2,14.5*num2,17.5*num2),11:(14.5*num2,17.5*num2,14.5*num2,17.5*num2),12:(20.5*num2,23.5*num2,14.5*num2,17.5*num2),
          13:(1.5*num2,5.5*num2,20.5*num2,23.5*num2),14:(8.5*num2,11.5*num2,20.5*num2,23.5*num2),15:(14.5*num2,17.5*num2,20.5*num2,23.5*num2),16:(20.5*num2,23.5*num2,20.5*num2,23.5*num2)}
rects=[0,0,0,0,0,0,0,0,0]        


def write_labels():
    global DIRECTION , num2,num1,num3,DIRECTION,posi,Labels_l,VISITED,ob, Labels_l1,AWARE,textfont,textfont2,WIN
    
    for i in AWARE:
        if AWARE[i]==True and ob.Safe_points[i-1]==1:
            textTBD=textfont.render("Safe " ,1,WHITE)
            WIN.blit(textTBD,Labels_l[i])
            if ob.stink_points[i-1]==1:
                textTBD=textfont.render("Stinky " ,1,WHITE)
                WIN.blit(textTBD,Labels_l1[i])
            if ob.breeze_points[i-1]==1:
                textTBD=textfont.render("Breezy " ,1,WHITE)
                WIN.blit(textTBD,(Labels_l1[i][0],Labels_l1[i][1]+20))
            

def update_visited(centrex,centrey):
    global DIRECTION , num2,num1,num3,DIRECTION,posi,Labels_l,VISITED,BOUNDARY,AWARE,FLAG,ob,SCORE,CURRENT_POS
    for i in range(16):
        if ((centrey>BOUNDARY[i+1][2]) and (centrey+2*num3<BOUNDARY[i+1][3])) and((centrex>BOUNDARY[i+1][0]) and (centrex+2*num3<BOUNDARY[i+1][1])):
            CURRENT_POS=i+1
            if (VISITED[i+1]==False):
                VISITED[i+1]=True
                ##SCORE-=10
                if i+1 in ob.reward_pos:
                    SCORE+=1000
                    FLAG=True
                
                AWARE[i+1]=True

def draw_entity():
    global ob,posi,WUMPUS_IMG,PIT_IMG,num1,num2,GameOver,AWARE,VISITED,GOLD_IMG,GOLDS,FLAG,SCORE,WIN
    for i in ob.wumpus_pos:
        if AWARE[i]==True:

            WIN.blit(WUMPUS_IMG,(posi[i][0]-num1,posi[i][1]-num2))
            if VISITED[i]==True:
                SCORE-=2000
                GameOver=True
    for i in ob.pit_pos:
        if AWARE[i]==True:
            WIN.blit(PIT_IMG,(posi[i][0]-num1,posi[i][1]-num2))
            if VISITED[i]==True:
                SCORE-=2000
                GameOver=True
    for i in ob.reward_pos:
        if AWARE[i]==True:
            WIN.blit(GOLD_IMG,(posi[i][0]-num1,posi[i][1]-num2))
            if VISITED[i]==True and FLAG==True:

                GOLDS-=1
                FLAG=False
                if GOLDS==0:
                    GameOver=True

    pygame.display.update()
    
def main():
    
    global DIRECTION , num2,num1,num3,DIRECTION,posi,Labels_l,VISITED,AWARE,FLAG,GameOver,textfont,textfont2,SCORE,ob,CURRENT_POS
    player=pygame.Rect(posi[13][0]-num1,posi[13][1]-num2,num1,num2)
    clock=pygame.time.Clock()
  
    
    
    Run=True
    
    while(Run):
        
        WIN.fill(BLACK)
        draw_board(boards.board3)
        draw_player(player)
        mouse=pygame.mouse.get_pos()
        #print(mouse)
        update_visited(player.x,player.y)
        draw_entity()
        write_labels()
        for event in  pygame.event.get():
            if event.type==pygame.QUIT:
                Run=False
            if event.type==pygame.KEYDOWN:
                
                if event.key==pygame.K_a: #left
                    DIRECTION=1
                if event.key==pygame.K_d: #right

                    DIRECTION=0
                if event.key==pygame.K_w: #up
                    DIRECTION=2
                if event.key==pygame.K_s: #down
                    DIRECTION=3
        

        turns=check_pos(player,player.x,player.y)
        keys_pressed=pygame.key.get_pressed()
        player_movement(keys_pressed,player,turns)
        ##wumpus_movement(keys_pressed,wumpus)
        textTBD=textfont2.render("Score  : " + str(SCORE),1,WHITE)
        WIN.blit(textTBD,(600,200))
        
        
        if GameOver==True:
                    if CURRENT_POS in ob.wumpus_pos or CURRENT_POS in ob.pit_pos :

                            textTBD=textfont2.render("You Lose!!! " ,1,WHITE)
                            WIN.blit(textTBD,(600,400))
                    if CURRENT_POS in ob.reward_pos:
                            textTBD=textfont2.render("You Win!!! " ,1,WHITE)
                            WIN.blit(textTBD,(600,400))
                    screen.blit(WIN, (0, 0))
                    pygame.display.flip()
                    
                    time.sleep(2)
                    break
        screen.blit(WIN, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
if __name__=="__main__":
    main()
