from msilib.schema import Class
from operator import truediv
import pygame
import sys
import random




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

class Game():

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

    def run(self):    
        while self.running:
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            keys= pygame.key.get_pressed()
            self.snake.smer_snake=self.snake.novy_smer(keys)
            self.new_smer=self.snake.zmen_pozici()
            self.snake.pozice.insert(0,self.new_smer)

            if self.snake.is_collision(self.eat):
                
                self.eat = self.snake.generate_eat()
            else:
                self.snake.pozice.pop()

            if not self.snake.control_position():
                
                running=False

                while not running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_ESCAPE:
                                self.snake.pozice=[]
                                self.snake.pozice = [{"x": self.snake.okno[0]/2 , "y" : self.snake.okno[1]/2}]
                                eat = self.snake.generate_eat()
                                running=True
                                
                    else:
                        pygame.display.update()
                        self.okno_hry.fill(pygame.Color(0,0,0))
                        score = self.BIGFONT.render(f" SCORE {len(self.snake.pozice)} pro novou hru stiskni ESC", False, (255, 255, 255))
                        self.okno_hry.blit(score,(10,self.snake.okno[0]/2))
                        
            if self.snake.self_colision():
                running=False
                
                while not running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.snake.pozice=[]
                                self.snake.pozice = [{"x": self.snake.okno[0]/2 , "y" : self.snake.okno[1]/2}]
                                eat = self.snake.generate_eat(self.snake.snake_size,self.snake,self.snake.okno)
                                                    
                            running=True
                    else:
                        pygame.display.update()
                        self.okno_hry.fill(pygame.Color(0,0,0))
                        score = self.BIGFONT.render(f" SCORE {len(self.snake)} pro novou hru stiskni ESC", False, (255, 255, 255))
                        self.okno_hry.blit(score,(10,self.snake.okno[0]/2))
                                                    
                       
            #draw snake and window update tick tack
            for part in self.snake.pozice:
                pygame.draw.rect(self.okno_hry, self.snake.barva_hada, pygame.Rect(part["x"], part["y"], self.snake.snake_size, self.snake.snake_size))
            pygame.draw.rect(self.okno_hry, self.eat_color, pygame.Rect(self.eat["x"], self.eat["y"], self.snake.snake_size, self.snake.snake_size))
            score2 = self.BIGFONT.render(f" SCORE {len(self.snake.pozice)}", False, (255, 255, 255))
            self.okno_hry.blit(score2,(10,10))
            
            pygame.display.update()
            self.okno_hry.fill(pygame.Color(0,0,0))
            self.clock.tick(self.snake.game_speed)


if __name__ == "__main__":

     game=Game()
     game.run()


    


    
        
