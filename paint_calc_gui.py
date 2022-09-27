from abc import abstractmethod
from enum import Enum
import math
from tkinter import Button 

##### Enums #####
# Shapes
class Shape(Enum):
    SQUARE = lambda b: pow(b, 2)
    RECTANGLE = lambda b, h: b * h
    PARALLELOGRAM = lambda b, h: b * h
    TRAPEZOID = lambda b, h, a: ((a + b) // 2) * h
    TRIANGLE = lambda b, h: 0.5 * (b * h)
    ELLIPSE = lambda b, a: math.pi * (a*b)
    CIRCLE = lambda r: math.pi * pow(r, 2)
    SEMICIRCLE = lambda r: (math.pi * pow(r, 2)) // 2
    
    def __call__(self, args):
        return self.value[0](args)
    
    @classmethod
    def to_shape(self, shape_name):
        match shape_name:
            case "square":
                return Shape.SQUARE
            case "rectangle":
                return Shape.RECTANGLE
            case "parallelogram":
                return Shape.PARALLELOGRAM
            case "trapezoid":
                return Shape.TRAPEZOID
            case "triangle":
                return Shape.TRIANGLE
            case "ellipse":
                return Shape.ELLIPSE
            case "circle":
                return Shape.CIRCLE
            case "semicircle":
                return Shape.SEMICIRCLE
            case _:
                return None

# Paints
class Paint(Enum):
    # name = [price per bucket, litres per bucket, coverage per litre]
    RED = (1.00, 1.25, 0.75)
    BLUE = (1.25, 1.25, 0.5)
    GREEN = (2.75, 0.75, 1.34)
    
    def __call__(self, args):
        return self.value[args]
    
    @classmethod
    def to_paint(self, paint_name):
        match paint_name:
            case "red":
                return Paint.RED
            case "blue":
                return Paint.BLUE
            case "green":
                return Paint.GREEN
            case _:
                return None


##### Classes ##### 
# Architecture (Walls, doors, windows, etc)
class Architecture():
    def __init__(self):
        self.__surface_area = 0  
        self.__index = 0

    def area(self):
        return self.__surface_area
    
    @abstractmethod
    def define(self):
        pass

    def __get_shape(self):
        while True:
            print("Square | Rectangle | Parallelogram | Trapezoid | Triangle | Ellipse | Circle | Semicircle")
            wall_shape = input("Of the shapes listed above, which best describes the shape of this %s?: "% type(self).__name__.lower()).lower()

            shape_type = Shape.to_shape(wall_shape)
            if shape_type is not None:
                wall_shape = shape_type
                break
            else:
                print("Invalid Shape!")
        
        return wall_shape
    
    def _calc_area(self):
        surface_area = None
        shape = self.__get_shape()
        
        if shape is Shape.SQUARE:
            base_metres = get_float_input("Please enter the length of one side in metres: ")
            wall_surface_area = shape(base_metres)
            
        elif shape is Shape.RECTANGLE or shape is Shape.PARALLELOGRAM or shape is Shape.TRIANGLE:
            prompts = [
                "Please enter the length of the base in metres: ",
                "Please enter the the height in metres: "
            ]
            
            answers = get_multi_float(prompts)
            wall_surface_area = shape(answers[0], answers[1])
            
        elif shape is Shape.TRAPEZOID:
            prompts = [
                "Please enter the length of the base in metres: ",
                "Please enter the length of the top in metres: ",
                "Please enter the the height in metres: "
            ]
             
            answers = get_multi_float(prompts)
            wall_surface_area = shape(answers[0], answers[2], answers[1])
            
        elif shape is Shape.ELLIPSE:
            vertical_metres = get_float_input("Please enter the vertical radius of in metres: ")
            horizontal_metres = get_float_input("Please enter the horizontal radius in metres: ")
            wall_surface_area = shape(horizontal_metres, vertical_metres)
        elif shape is Shape.CIRCLE or shape is Shape.SEMICIRCLE:
            radius_metres = get_float_input("Please enter the radius in metres: ")
            wall_surface_area = shape(radius_metres)
            
        return wall_surface_area

# A wall
class Wall(Architecture):
    def __init__(self):
        self.__paint = Paint.RED
        self.__surface_area = 0.0
        self.__coats = 1
        self.__obstacles = []
        self.__index = 0
        
    def define(self, index):
        self.__index = index
        self.__paint = self.__get_paint()
        self.__coats = self.__get_coats()
        clear_console()
        
        self.__get_obstacles = self.__get_obstacles()
        clear_console()

        print("Wall No.%d" % self.__index)
        self.__surface_area = self._calc_area()
        clear_console()
        
        if len(self.__obstacles) != 0:
            self.__area_without_obstacles()
    
    def __get_coats(self):
        return get_int_input("How many coats of this paint do you plan to apply? ")
    
    def required_buckets(self):
        litres_required = (self.__surface_area * self.__coats) // self.__paint(2)
        return  round(litres_required // self.__paint(1))
    
    def cost(self):
        return self.required_buckets() * self.__paint(0)
    
    def __get_obstacles(self):
        num_of_obstacles = get_int_input("Please enter the number of obstacles (doors/windows) on this wall: ")
        while True:
            try:
                obstacles = [Obstacle()] * num_of_obstacles
                break
            except: 
                num_of_obstacles = get_int_input("Error! Please enter the number of obstacles (doors/windows) on this wall as a whole number: ")
        
        index = 0
        for obstacle in obstacles:
            print("Obstacle No.%d" % self.__index)
            obstacle.define(index)
            index += 1
            clear_console()
        
        return obstacles
    
    def __area_without_obstacles(self):
        for obstacle in self.__obstacles:
            self.__surface_area -= obstacle.area()
        
    def __get_paint(self): 
        print("Wall No.%d" % self.__index)
        
        while True:
            print("Red | Green | Blue")
            colour = input("Of the colours listed above, which do you want to use on your wall? ").lower()

            paint_colour = Paint.to_paint(colour)
            if paint_colour is not None:
                colour = paint_colour
                break
            else:
                print("Invalid colour!")
        
        return colour

# Windows, Doors, etc. 
class Obstacle(Architecture): 
    def define(self, index):
        self.__index = index
        self.__surface_area = self._calc_area()

# Rooms
class Room():
    def __init__(self):
        self.__walls = []
        self.__name = "default room"
        self.__index = 0
    
    def set_name(self, room_index): 
        import PySimpleGUI as sg
        import sys
        
        self.__index = room_index
        
        layout = [
                [sg.Text("Room No.%d" % self.__index)], 
                [sg.Text("Please enter a name for this room: ")], 
                [sg.Multiline(size=(30,5), key='textbox')], 
                [sg.Button("CONFIRM")],
                [sg.Button("CLOSE")]
            ] 
                
        window = sg.Window("Paint Calculator", layout)
        
        while True:
            event, values = window.read()
            match event:
                case "CONFIRM":
                    self.__name = values['textbox']
                    break 
                case None:
                    sys.exit()
                case "CLOSE":
                    sys.exit()
                case _: 
                    pass
        window.close()
         
    def define(self, room_index):
        self.__index = room_index
        
        clear_console()
        
        print("Current Room: %s" % self.__name)  
        num_of_walls = get_int_input("Please enter the number of walls for this room: ")
        
        while True:
            try:
                self.__walls = [Wall()] * num_of_walls
                break
            except: 
                num_of_walls = get_int_input("Error! Please enter the number of walls for this room as a whole number: ")
        
        index = 1
        for wall in self.__walls:
            print("Current Room: %s" % self.__name) 
            wall.define(index)
            index += 1
            clear_console()
            
    def walls(self):
        return self.__walls

# The Calculator
class Calculator():
    def __init__(self):       
        self.__rooms = []
    
  
        
    def main(self):
        import PySimpleGUI as ui

        self.__rooms = self.__get_rooms()
        
        room_index = 1
        for room in self.__rooms: 
            room.set_name(room_index)
            room_index += 1
        
        
        shape_types = [['Shape', ["Square", "Rectangle", "Parallelogram", "Trapezoid", "Triangle", "Ellipse", "Cirlce", "Semicircle"]]]

        # Define UI elements
        layout = [[ui.Menu(shape_types, text_color="black", font="SYSTEM_DEFAULT", pad=(10,10))]]
        window = ui.Window("Paint Calculator", layout)

        while True:
            event, value = window.read()

            match event:
                case ui.WIN_ClOSED:
                    break
                case 'Rectangle' | 'Parallelogram' | 'Triangle':
                    print('Temp')
                case 'Trapezoid':
                    print('Temp')
                case 'Ellipse':
                    print('Temp')
                case 'Cirlce' | 'Semicircle':
                    print('Temp')
                case _: # Square as default
                    layout = [
                        [ui.Menu(shape_types, text_color="black", font="SYSTEM_DEFAULT", pad=(10,10))] ,
                        [sg.Text('Please enter the length of one side of your wall in metres:')], 
                        [sg.Multiline(size=(30,5), key='length')], 
                        [sg.Button("CONFIRM")], 
                        [sg.Button("CLOSE")]
                    ]





        window.close()

    def calc_cost(self):
        cost = 0
        for room in self.__rooms:
            for wall in room.walls():
                cost += wall.cost()
        
        return cost

    def __get_rooms(self): 
        import PySimpleGUI as sg
        import sys
        
        layout = [[sg.Text('Please enter the number of rooms you wish to paint in the box below:')], [sg.Multiline(size=(30,5), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]] 
        window = sg.Window("Paint Calculator", layout)
        
        while True:
            event, values = window.read()
            match event:
                case "CONFIRM":
                    num_of_rooms = get_int_input(values['textbox'], window)
                    rooms = [Room()] * num_of_rooms
                    return rooms
                case None:
                    sys.exit()
                case "CLOSE":
                    sys.exit()
                case _: 
                    pass
        


##### Public Functions ##### 
def get_float_input(usr_input):
    import PySimpleGUI as sg
    import sys
    
    user_input = ""
    valid_input = False
    
    while True:
        try:
            user_input = float(usr_input)
            valid_input = True
        except ValueError:
            valid_input = False

        if not valid_input or user_input <= 0:
            layout = [[sg.Text('Error: Please enter a positive, non-zero, whole number:')], [sg.Multiline(size=(30,5), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
            window.close()
            window = sg.Window("Paint Calculator", layout) 
        elif valid_input:
            window.close()
            return user_input

        window.refresh()
        while True:
          event, values = window.read()
          if event == "CONFIRM":
              usr_input = values['textbox']
              break
          elif event == "CLOSE":
              sys.exit()
    
def get_int_input(usr_input, window):
    import PySimpleGUI as sg
    import sys
    
    user_input = ""
    valid_input = False
    
    while True:
        try:
            user_input = int(usr_input)
            valid_input = True
        except ValueError:
            valid_input = False

        if not valid_input or user_input <= 0:
            layout = [[sg.Text('Error: Please enter a positive, non-zero, whole number:')], [sg.Multiline(size=(30,5), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
            window.close()
            window = sg.Window("Paint Calculator", layout) 
        elif valid_input:
            window.close()
            return user_input

        window.refresh()
        while True:
          event, values = window.read()
          if event == "CONFIRM":
              usr_input = values['textbox']
              break
          elif event == "CLOSE":
              sys.exit()


def clear_console():
    import os
    clear = lambda: os.system('clear')

if __name__ == '__main__':
    calculator = Calculator()
    calculator.main()

