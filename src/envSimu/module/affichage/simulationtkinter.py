import tkinter as tk
import math
import random
import threading
import time

class Simulationtkinter(tk.Tk):
    def __init__(self,environnement):
        tk.Tk.__init__(self)
#OBJETS
        self.environnement = environnement
        self.bool = False
        self.robot = self.environnement.robot
#CANVAS TKINTER
        self.canvas = tk.Canvas(self, bg='white', width=self.environnement.max_x, height=self.environnement.max_y)
        self.robot_canv = self.canvas.create_oval(self.robot.posx-self.robot.rayon,self.robot.posy-self.robot.rayon, self.robot.posx+self.robot.rayon, self.robot.posy+self.robot.rayon, fill='red')
        self.line = self.canvas.create_line(self.robot.posx,self.robot.posy,self.robot.posx+math.cos(math.radians(self.robot.dirr))*self.robot.rayon,self.robot.posx+math.sin(math.radians(self.robot.dirr))*self.robot.rayon, arrow="last")
        self.label = tk.Label( text="Vitesse gauche:         Vitesse droite:0\nAngle: 0\nPosition: (0, 0)")
        self.label.pack()
        for i in self.environnement.ensObstacle:
            obstacle_canv=self.canvas.create_oval(i.posx-i.rayon,i.posy-i.rayon,i.posx+i.rayon,i.posy+i.rayon, fill=i.color)
        self.canvas.pack()

#BOUTTONS TKINTER
        self.PlusVg = tk.Button(self, text='+ Vd', command=self.robot.augDPSd)
        self.PlusVg.pack(side='right')
        self.DimVg = tk.Button(self, text='- Vd', command=self.robot.dimDPSd)
        self.DimVg.pack(side='right')
        self.PlusVd = tk.Button(self, text='+ Vg', command=self.robot.augDPSg)
        self.PlusVd.pack(side='left')
        self.DimVd = tk.Button(self, text='- Vg', command=self.robot.dimDPSg)
        self.DimVd.pack(side='left')
        self.quit_button = tk.Button(self, text="Quitter Simulation", command=self.destroy)
        self.quit_button.pack()
      

#FONCTION LANCER SIMULATION 

    def update_robot(self):
        time.sleep(0.001)
        self.canvas.coords(self.robot_canv,self.robot.posx-self.robot.rayon,self.robot.posy-self.robot.rayon,self.robot.posx+self.robot.rayon, self.robot.posy+self.robot.rayon)

        self.canvas.create_rectangle(self.robot.lastposx,self.robot.lastposy,self.robot.posx,self.robot.posy)

        self.canvas.coords(self.line,self.robot.posx,self.robot.posy,self.robot.posx+math.cos(math.radians(self.robot.dirr))*self.robot.rayon,self.robot.posy+math.sin(math.radians(self.robot.dirr))*self.robot.rayon)
        self.label.config(text=f"Vitesse gauche: {self.robot.dpsG}          Vitesse droite: {self.robot.dpsD} \nAngle: {self.robot.dirr}\nPosition: {self.robot.getPos()}")
        self.canvas.after(20, self.update_robot)

    def loop(self):
        self.update_robot()   
        self.mainloop()
