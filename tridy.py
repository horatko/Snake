from lib2to3.pgen2.token import NEWLINE
from msilib.schema import Class
from operator import truediv
from unicodedata import decimal
import pygame
import sys
import random
from tkinter import *
import csv



class Snake:

    def __init__(self):
            
        self.smer_snake="RIGHT"
        self.snake_size=20
        self.okno=[400,400]
        self.pozice=[{"x": self.okno[0]/2 , "y" : self.okno[1]/2}]
        self.game_speed=8
        self.barva_hada=pygame.Color(98,32,98)
        self.snake_size=20

    def novy_smer(self,keys):  # get keys
        if keys[pygame.K_UP] :
            return "UP" if self.smer_snake != "DOWN" else self.smer_snake
        if keys[pygame.K_DOWN] :
            return "DOWN" if self.smer_snake != "UP" else self.smer_snake
            
        if keys[pygame.K_LEFT] :
            return "LEFT" if self.smer_snake != "RIGHT" else self.smer_snake
        if keys[pygame.K_RIGHT] :
            return "RIGHT" if self.smer_snake != "LEFT" else self.smer_snake
        return self.smer_snake

    def zmen_pozici(self): #change position of snake
        snak={}
        if self.smer_snake=="LEFT":
            snak={"x":self.pozice[0]["x"]-self.snake_size, "y":self.pozice[0]["y"]}
        if self.smer_snake=="RIGHT":
            snak={"x":self.pozice[0]["x"]+self.snake_size, "y":self.pozice[0]["y"]}
            
        if self.smer_snake=="UP":
            snak={"x":self.pozice[0]["x"], "y":self.pozice[0]["y"]-self.snake_size}
        if self.smer_snake=="DOWN":
            snak={"x":self.pozice[0]["x"], "y":self.pozice[0]["y"]+self.snake_size}
        return snak

    def control_position(self):
        if self.pozice[0]["x"]>=self.okno[0] :
            return False
        elif self.pozice[0]["x"]<0:
            return False
        elif self.pozice[0]["y"]>=self.okno[0] :
            return False
        elif self.pozice[0]["y"]<0 :
            return False
        return True

    def generate_eat(self):

        x= random.choice(range(0,self.okno[0],self.snake_size))
        y= random.choice(range(0,self.okno[1],self.snake_size))
        for part in self.pozice:
            if x==part["x"] and y==part["y"]:
                x= random.choice(range(0,self.okno[0],self.snake_size))
                y= random.choice(range(0,self.okno[1],self.snake_size))
        return {"x":x, "y":y}


    def is_collision(self, eat):
        if self.pozice[0]["x"] == eat["x"] and self.pozice[0]["y"] == eat["y"] :
            return True
        return False
        
    def self_colision(self):
        for part in self.pozice[1:]:
            if self.pozice[0]==part:
                return True
        return False

class Game:
    
    def __init__(self):
        #set deafault condicions
        pygame.init()
        self.snake=Snake()
        
        pygame.display.set_caption("Snake by Jarmen")
        self.BIGFONT = pygame.font.SysFont("comicsans", 20)
        self.clock = pygame.time.Clock()
        self.eat_color =pygame.Color(10,150,150)
        self.okno_hry=pygame.display.set_mode((self.snake.okno))
        pygame.draw.rect(self.okno_hry, self.snake.barva_hada, pygame.Rect(self.snake.okno[0]/2, self.snake.okno[1]/2, self.snake.snake_size, self.snake.snake_size))
        self.eat = self.snake.generate_eat()
        self.running=True
        self.pauza=1
        self.score_uloz=0
        

    def run(self):    
        while self.running:
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_p:
                        print("pic")
                        self.pauza=self.pauza*-1
                        if self.pauza==-1:
                            if self.pauza==-1:
                                self.game_pause()
                        else:
                            self.running=True
                        
                        
        
            keys= pygame.key.get_pressed()
            self.snake.smer_snake=self.snake.novy_smer(keys)
            self.new_smer=self.snake.zmen_pozici()
            self.snake.pozice.insert(0,self.new_smer)

            if self.snake.is_collision(self.eat):
                
                self.eat = self.snake.generate_eat()
            else:
                self.snake.pozice.pop()

            if not self.snake.control_position():
                
                self.running=False

                if not self.running:
                    self.show_gameover(True)
                        
            if self.snake.self_colision():
                self.running=False
                
                if not self.running:
                    self.show_gameover(True)
            
            
                                                    
                       
            #draw snake and window update tick tack
            self.show_snake((10,10),False)

            
    def game_pause(self):
        while self.pauza==-1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
    
                    if event.key == pygame.K_p:
                        self.pauza*=-1
                
            self.show_snake((100,200),True)


    def show_snake(self, poz, showpause):
        for part in self.snake.pozice:
                pygame.draw.rect(self.okno_hry, self.snake.barva_hada, pygame.Rect(part["x"], part["y"], self.snake.snake_size, self.snake.snake_size))
        pygame.draw.rect(self.okno_hry, self.eat_color, pygame.Rect(self.eat["x"], self.eat["y"], self.snake.snake_size, self.snake.snake_size))
        if showpause :
            self.score2 = self.BIGFONT.render(f" !!!PAUSE!!!   SCORE  {len(self.snake.pozice)}", False, (255, 255, 255))
        else:
            self.score2 = self.BIGFONT.render(f" SCORE {len(self.snake.pozice)}", False, (255, 255, 255))
        self.okno_hry.blit(self.score2,(poz))
            
        pygame.display.update()
        self.okno_hry.fill(pygame.Color(0,0,0))
        self.clock.tick(self.snake.game_speed)

    def show_gameover(self, ingameover):
        self.pole=[]
        self.nalez=False

        #with open('score.csv', 'a', newline="\n" ) as self.soubor:
            #self.writer=csv.writer(self.soubor)
            #self.writer.writerow((user,str(len(self.snake.pozice))))
            #self.soubor.close
            
            #self.soubor.close
        with open('score.csv', 'r' ) as self.soubor:
            self.reader=csv.reader(self.soubor)
            for row in self.reader:
                self.pole.append(row)
            for row in self.pole:
                if row[1]==user:
                    self.nalez=True
                    if int(row[0])<=len(self.snake.pozice):
                        row[0]=str(len(self.snake.pozice))
                        
            
            if not self.nalez:
                self.pole.append([str(len(self.snake.pozice)),user])   
               
            print(self.pole)
            self.soubor.close

        with open('score.csv', 'w', newline="" ) as self.soubor:
            self.writer=csv.writer(self.soubor)           
            self.writer.writerows(self.pole)
            self.soubor.close 
        
        
        while ingameover==True:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE:
                        self.snake.pozice=[]
                        
                        
                        self.snake.pozice = [{"x": self.snake.okno[0]/2 , "y" : self.snake.okno[1]/2}]
                        self.eat = self.snake.generate_eat()
                        self.running=True
                        ingameover=False
                                
           
            pygame.display.update()
            self.okno_hry.fill(pygame.Color(0,0,0))
            score = self.BIGFONT.render(f" SCORE {len(self.snake.pozice)} pro novou hru stiskni ESC", False, (255, 255, 255))

            self.okno_hry.blit(score,(10,self.snake.okno[0]/2))

class User():
        
    def __init__(self):
          
        self.window=Tk()
        self.label=Label(self.window,text="Zadej jméno hráče", background="black", fg="white")
        self.label.pack()
        self.username=StringVar
        self.vstup=Entry(self.window,textvariable=self.username)
        self.vstup.pack()
        self.button=Button(self.window, text="ulož", command=self.buttonclick)
        self.button.pack()
        
        
        self.window.mainloop()

    def buttonclick(self):
        
        self.username=self.vstup.get()
        global user
        user=self.username

        self.window.destroy()


        

        
        
        

        