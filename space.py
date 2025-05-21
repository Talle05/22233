#Module for drawing planets for DVA248 Datorsystem
#
#   author: Dag Nyström, 2023
#
import tkinter

class space:
    '''
    Class for managing a canvas to draw planets on
    '''
    tk=tkinter.Tk
    c=tkinter.Canvas
    spacex=0
    spacey=0

    def __init__(self,x:int,y:int):
        '''
        Constructor that creates an instance of the canvas.
            x,y:    Integers that define the size (in pixels/coordinates) of the canvas.
        '''
        self.spacex=x
        self.spacey=y
        self.tk=tkinter.Tk()
        self.tk.geometry(str(self.spacex)+"x"+str(self.spacey))
        self.c=tkinter.Canvas(self.tk,width=self.spacex, height=self.spacey)
        self.c.create_rectangle(0,0,self.spacex,self.spacey,fill="black",outline="black")
        self.c.place(x=0,y=0)

    def putPlanet(self,x,y,rad=5,color="white"):
        '''
        Method that draws a planet on the canvas
            x,y:    Integer-coordinates to draw the planet
            rad:    size of the planet (default is 5pixels)
            color:  color of the planet, (default is white)
        '''
        self.c.create_oval(x,y,x+rad,y+rad,fill=color,outline=color)

    def mainLoop(self):
        '''
        Method to manage the main loop of the canvas management. Is usually placed last in the main function.
        '''
        self.tk.mainloop()
