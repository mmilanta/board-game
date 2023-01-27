from tkinter import *
import subprocess
import random
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

"""noise = PerlinNoise()

xpix, ypix = 100, 100
pic = []
freq = 4
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val = noise([freq*i/xpix,freq* j/ypix])
        row.append(noise_val)
    pic.append(row)

plt.imshow(pic, cmap='gray')
plt.colorbar()
plt.show()"""

def main():
    grid_width = 10
    grid_height = 10
    board = Board(grid_width,grid_height)
    board.generate_world(freq = 4, thrs=[-.2,.0,.3])
    board.render_world(scale=20)

def discretize(val, th):
    out = 0
    for i in th:
        if val > i:
            out += 1
    return out

class Board():
    """ A board """
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width
        self.mat = [[0 for _ in range(height)] for _ in range(width)]
        pass

    def generate_world(self, freq = 6, thrs = [-.1,.05,.3]) -> None:
        noise = PerlinNoise()
        for row in range(self.height):
            for col in range(self.width):
                #self.mat[row][col] = random.choices([0,1,2,3], weights = [0,3,4,1],  k = 1)[0]
                tmp = noise([freq*row/self.height,freq* col/self.width])
                self.mat[row][col] = discretize(tmp,thrs)

    def render_world(self, scale = 10) -> None:
        tk = Tk()
        grid = HexagonalGrid(tk, scale = scale, grid_width=self.width, grid_height=self.height)
        grid.grid(row=0, column=0, padx=5, pady=5)

        def correct_quit(tk):
            tk.destroy()
            tk.quit()
        def save_to_pdf(canvas):
            canvas.postscript(file="tmp.ps", colormode='color')
            somecommand = "gs -o output.pdf -sDEVICE=pdfwrite -dEPSCrop tmp.ps"
            process = subprocess.Popen(somecommand, shell=True)
            process.wait()


        quit = Button(tk, text = "Quit", command = lambda :correct_quit(tk))
        save = Button(tk, text = "Save", command = lambda :save_to_pdf(grid))
        quit.grid(row=1, column=0)
        save.grid(row=1, column=1)
        colors = [  "#43d3f0",
                    '#f9e79f',
                    '#52be80',
                    "#706f6b"]
        for row in range(self.height):
            for col in range(self.width):
                grid.setCell(row,col, fill=colors[self.mat[row][col]])
        tk.mainloop()


class HexaCanvas(Canvas):
    """ A canvas that provides a create-hexagone method """
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.hexaSize = 20

    def setHexaSize(self, number):
        self.hexaSize = number


    def create_hexagone(self, x, y, color = "black", fill="blue", color1=None, color2=None, color3=None, color4=None, color5=None, color6=None):
        """ 
        Compute coordinates of 6 points relative to a center position.
        Point are numbered following this schema :

        Points in euclidiean grid:  
                    6

                5       1
                    .
                4       2

                    3

        Each color is applied to the side that link the vertex with same number to its following.
        Ex : color 1 is applied on side (vertex1, vertex2)

        Take care that tkinter ordinate axes is inverted to the standard euclidian ones.
        Point on the screen will be horizontally mirrored.
        Displayed points:

                    3
              color3/      \color2      
                4       2
            color4|     |color1
                5       1
              color6\      /color6
                    6

        """
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5

        point1 = (x+Δx, y+size/2)
        point2 = (x+Δx, y-size/2)
        point3 = (x   , y-size  )
        point4 = (x-Δx, y-size/2)
        point5 = (x-Δx, y+size/2)
        point6 = (x   , y+size  )

        #this setting allow to specify a different color for each side.
        if color1 == None:
            color1 = color
        if color2 == None:
            color2 = color
        if color3 == None:
            color3 = color
        if color4 == None:
            color4 = color
        if color5 == None:
            color5 = color
        if color6 == None:
            color6 = color

        self.create_line(point1, point2, fill=color1, width=2)
        self.create_line(point2, point3, fill=color2, width=2)
        self.create_line(point3, point4, fill=color3, width=2)
        self.create_line(point4, point5, fill=color4, width=2)
        self.create_line(point5, point6, fill=color5, width=2)
        self.create_line(point6, point1, fill=color6, width=2)

        if fill != None:
            self.create_polygon(point1, point2, point3, point4, point5, point6, fill=fill)

class HexagonalGrid(HexaCanvas):
    """ A grid whose each cell is hexagonal """
    def __init__(self, master, scale, grid_width, grid_height, *args, **kwargs):

        Δx     = (scale**2 - (scale/2.0)**2)**0.5
        width  = 2 * Δx * grid_width + Δx
        height = 1.5 * scale * grid_height + 0.5 * scale

        HexaCanvas.__init__(self, master, background='white', width=width, height=height, *args, **kwargs)
        self.setHexaSize(scale)

    def setCell(self, xCell, yCell, *args, **kwargs ):
        """ Create a content in the cell of coordinates x and y. Could specify options throught keywords : color, fill, color1, color2, color3, color4; color5, color6"""

        #compute pixel coordinate of the center of the cell:
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5

        pix_x = Δx + 2*Δx*xCell
        if yCell%2 ==1 :
            pix_x += Δx

        pix_y = size + yCell*1.5*size

        self.create_hexagone(pix_x, pix_y, *args, **kwargs)



if __name__ == "__main__":
    main()
