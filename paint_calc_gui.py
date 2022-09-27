from abc import abstractmethod
from asyncio import constants
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

    def _calc_area(self, shape, dimensions):
        surface_area = 0
        
        if shape is Shape.SQUARE:
           return shape(dimensions[0])
        elif shape is Shape.RECTANGLE or shape is Shape.PARALLELOGRAM or shape is Shape.TRIANGLE:
           return shape(dimensions[0], dimensions[1])
        elif shape is Shape.TRAPEZOID:
          return shape(dimensions[0], dimensions[1], dimensions[2])
        elif shape is Shape.ELLIPSE:
           return shape(dimensions[0], dimensions[1])
        elif shape is Shape.CIRCLE or shape is Shape.SEMICIRCLE:
           return shape(dimensions[0])
        else:
            return wall_surface_area

# A wall
class Wall(Architecture):
    def __init__(self):
        self.__paint = Paint.RED
        self.__surface_area = 0.0
        self.__coats = 1
        self.__obstacles = []
        
    def define(self, shape, colour, num_of_obstacles):
        import PySimpleGUI as sg
        import sys
        
        num_of_values = 0 
        
        self.__obstacles = [Obstacle()] * num_of_obstacles
        obstacle_index = 1
        
        for obstacle in self.__obstacles:
            obstacle.define(obstacle_index, len(self.__obstacles))
            obstacle_index += 1 
        
        match shape:
            case Shape.RECTANGLE | Shape.PARALLELOGRAM | Shape.TRIANGLE:
                num_of_values = 2 
                layout = [
                    [sg.Text("Please enter the details of this wall:")], 
                    [sg.Text("Enter the length of the base of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val1')], 
                    [sg.Text("Enter the height of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Text("Enter the number of coats side you plan to apply to the wall:")], 
                    [sg.Multiline(size=(30,1), key='paint')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case Shape.TRAPEZOID:
                num_of_values = 3 
                layout = [
                    [sg.Text("Please enter the details of this wall:")], 
                    [sg.Text("Enter the length of the base of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the height of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Text("Enter the length of the top of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val3')],  
                    [sg.Text("Enter the number of coats side you plan to apply to the wall:")], 
                    [sg.Multiline(size=(30,1), key='paint')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case Shape.ELLIPSE:
                num_of_values = 2
                layout = [
                    [sg.Text("Please enter the details of this wall:")], 
                    [sg.Text("Enter the vertical radius the wall:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the horizontal radius the wall:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Text("Enter the number of coats side you plan to apply to the wall:")], 
                    [sg.Multiline(size=(30,1), key='paint')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case Shape.CIRCLE | Shape.SEMICIRCLE:
                num_of_values = 1
                layout = [
                    [sg.Text("Please enter the details of this wall:")], 
                    [sg.Text("Enter the radius the wall:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the number of coats side you plan to apply to the wall:")], 
                    [sg.Multiline(size=(30,1), key='paint')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case _: # Default case is a square
                num_of_values = 1 
                layout = [
                    [sg.Text("Please enter the details of this wall:")], 
                    [sg.Text("Enter the length of one side of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val1')], 
                    [sg.Text("Enter the number of coats side you plan to apply to the wall:")], 
                    [sg.Multiline(size=(30,1), key='paint')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
                
            
                
        window = sg.Window("Paint Calculator", layout)
        
        dimensions = []
        coats = 0
                
        while True:
          event, values = window.read()
          match event:
              case "CONFIRM":
                coats = get_int_input(values['paint'], False)
                if num_of_values == 1:
                    dimensions.append(get_float_input(values['val1'],  False))
                elif num_of_values == 2:
                    dimensions.append(get_float_input(values['val1'], False))
                    dimensions.append(get_float_input(values['val2'], False))
                else:
                    dimensions.append(get_float_input(values['val1'], False))
                    dimensions.append(get_float_input(values['val2'], False))
                    dimensions.append(get_float_input(values['val3'], False))
                break 
              case None | "CLOSE":
                  sys.exit()
              case _: 
                 pass
                 
        self.__paint = colour
        self.__coats = coats
        
        window.Disable()
        self.__surface_area = self._calc_area(shape, dimensions)
        window.close()
    
    def required_buckets(self):
        litres_required = (self.__surface_area * self.__coats) // self.__paint(2)
        return  round(litres_required // self.__paint(1))
    
    def cost(self):
        return self.required_buckets() * self.__paint(0)
    
    def __area_without_obstacles(self):
        for obstacle in self.__obstacles:
            self.__surface_area -= obstacle.area()


# Windows, Doors, etc. 
class Obstacle(Architecture): 
    
    def define(self, index, total_num):
        import PySimpleGUI as sg
        import sys
        
        shape_types = ["Square", "Rectangle", "Parallelogram", "Trapezoid", "Triangle", "Ellipse", "Circle", "Semicircle"]
        
        layout = [
                [sg.Text("Obstacle No.%d of %d" % (index, total_num))], 
                [sg.Text("Please enter the details of this obstacle:")], 
                [sg.Text("Please select the shape of the obstacle from the drop down menu: ")], 
                [sg.OptionMenu(values=shape_types,size=(30,8), default_value='Square',key='shape')],
                [sg.Button("CONFIRM")],
                [sg.Button("CLOSE")]
            ] 
        
        window = sg.Window("Paint Calculator", layout)

        while True:
            event, values = window.read()
            match event:
                case "CONFIRM":
                    shape = Shape.to_shape(values['shape'].lower())
                    break 
                case None:
                    sys.exit()
                case "CLOSE":
                    sys.exit()
                case _: 
                    pass
        
        window.Disable()
        self.__area(shape)   
        window.close()
        
    def __area(self, shape):
        import PySimpleGUI as sg
        import sys
         
        match shape:
            case Shape.RECTANGLE | Shape.PARALLELOGRAM | Shape.TRIANGLE:
                num_of_values = 2 
                layout = [
                    [sg.Text("Please enter the details of this obstacle:")], 
                    [sg.Text("Enter the length of the base of the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val1')], 
                    [sg.Text("Enter the height of the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case Shape.TRAPEZOID:
                num_of_values = 3 
                layout = [
                    [sg.Text("Please enter the details of this obstacle:")], 
                    [sg.Text("Enter the length of the base of the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the height of the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Text("Enter the length of the top of the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val3')],  
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case Shape.ELLIPSE:
                num_of_values = 2
                layout = [
                    [sg.Text("Please enter the details of this obstacle:")], 
                    [sg.Text("Enter the vertical radius the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the horizontal radius the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case Shape.CIRCLE | Shape.SEMICIRCLE:
                num_of_values = 1
                layout = [
                    [sg.Text("Please enter the details of this obstacle:")], 
                    [sg.Text("Enter the radius the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            case _: # Default case is a square
                num_of_values = 1 
                layout = [
                    [sg.Text("Please enter the details of this obstacle:")], 
                    [sg.Text("Enter the length of one side of the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val1')], 
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]     
        
        window = sg.Window("Paint Calculator", layout)
        
        dimensions = []
        coats = 0
                
        while True:
          event, values = window.read()
          match event:
              case "CONFIRM":
                if num_of_values == 1:
                    dimensions.append(get_float_input(values['val1'], False))
                elif num_of_values == 2:
                    dimensions.append(get_float_input(values['val1'], False))
                    dimensions.append(get_float_input(values['val2'], False))
                else:
                    dimensions.append(get_float_input(values['val1'], False))
                    dimensions.append(get_float_input(values['val2'], False))
                    dimensions.append(get_float_input(values['val3'], False))
                break 
              case None | "CLOSE":
                  sys.exit()
              case _: 
                 pass
             
        window.Disable()        
        self.__surface_area = self._calc_area(shape, dimensions)
        window.close()


# Rooms
class Room():
    def __init__(self):
        self.__walls = []
        self.__name = "default room"
        self.__index = 0
    
    def get_walls(self):
        return self.__walls
        
    def define(self, room_index):
        import PySimpleGUI as sg
        import sys
        
        self.__index = room_index
        
        layout = [
                [sg.Text("Room No.%d" % self.__index)], 
                [sg.Text("Please enter the details of this room:")], 
                [sg.Text("Room name:")], 
                [sg.Multiline(size=(30,1), key='name')], 
                [sg.Text("Number of walls:")], 
                [sg.Multiline(size=(30,1), key='walls')], 
                [sg.Button("CONFIRM")],
                [sg.Button("CLOSE")]
            ] 
                
        window = sg.Window("Paint Calculator", layout)
        
        while True:
            event, values = window.read()
            match event:
                case "CONFIRM":
                    self.__name = values['name']
                    window.Disable()
                    self.__walls = [Wall()] * get_int_input(values['walls'], False)
                    break 
                case None | "CLOSE":
                    sys.exit()
                case _: 
                    pass
            
        self.__populate()
        window.close()
        
    def __populate(self): 
        import PySimpleGUI as sg
        import sys
        
        shape_types = ["Square", "Rectangle", "Parallelogram", "Trapezoid", "Triangle", "Ellipse", "Circle", "Semicircle"]
        colours = ["Red", "Green", "Blue"]
        
        wall_index = 1
        for wall in self.__walls:
            shape = "Square"
            layout = [
                    [sg.Text("Wall No.%d of %d in %s" % (wall_index, len(self.__walls), self.__name))], 
                    [sg.Text("Please enter the number of obstacles (doors/windows/etc): ")], 
                    [sg.Multiline(size=(30,1), key='obstacles')], 
                    [sg.Text("Please select the shape of the wall from the drop down menu: ")], 
                    [sg.OptionMenu(values=shape_types,size=(30,8), default_value='Square',key='shape')],
                    [sg.Text("Please select the colour of the wall from the drop down menu: ")], 
                    [sg.OptionMenu(values=colours,size=(30,8), default_value='Red',key='colour')],
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ] 

            window = sg.Window("Paint Calculator", layout)

            while True:
                event, values = window.read()
                match event:
                    case "CONFIRM":
                        shape = Shape.to_shape(values['shape'].lower())
                        colour = Paint.to_paint(values['colour'].lower())
                        window.Disable()
                        num_of_obstacles = get_int_input(values['obstacles'], True)
                        wall.define(shape, colour, num_of_obstacles)  
                        break 
                    case None | "CLOSE":
                        sys.exit()
                    case _: 
                        pass   
            window.close()
        
   
        
# The Calculator
class Calculator():
    def __init__(self):       
        self.__rooms = []
  
        
    def main(self):
        self.__rooms = self.__get_rooms()
        
        room_index = 1
        for room in self.__rooms: 
            room.define(room_index)
            room_index += 1
        
        ## Final Screen    
        self.__final_screen()

    def __final_screen(self): 
        import PySimpleGUI as sg
        import sys

        layout = [
            [sg.Text("All values have been entered")], 
            [sg.Button("Total Cost")],
            [sg.Button("Total Paint")],
            [sg.Button("Per Room")],
            [sg.Button("CLOSE")]
        ]
        window = sg.Window("Paint Calculator", layout)

        while True:
            event, values = window.read()
            match event:
                case "Total Cost":
                    window.Disable()
                    total_cost = 0
                    for room in self.__rooms:
                        for wall in room.get_walls():
                            total_cost += wall.cost()
                    temp_layout = [
                        [sg.Text("Total Cost: %.2f" % total_cost)], 
                        [sg.Button("OK")]
                    ]

                    temp_window = sg.Window("Total Cost", temp_layout)

                    while True:
                        event, values = temp_window.read()
                        match event:
                            case None | "OK":
                                temp_window.close()
                                break
                            case _: 
                                temp_window.close()
                                break
                            
                    window.Enable()
                case "Total Paint":
                    pass
                case "Per Room:": 
                    pass
                case None | "CLOSE":
                    sys.exit()
                    break
                case _: 
                    sys.exit()
                    break

        window.close()
        
    def __calc_cost(self):
        cost = 0
        for room in self.__rooms:
            for wall in room.walls():
                cost += wall.cost()
        
        return cost

    def __get_rooms(self): 
        import PySimpleGUI as sg
        import sys
        
        layout = [[sg.Text('Please enter the number of rooms you wish to paint in the box below:')], [sg.Multiline(size=(30,1), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]] 
        window = sg.Window("Paint Calculator", layout)
        
        while True:
            event, values = window.read()
            match event:
                case "CONFIRM":
                    window.Disable()
                    num_of_rooms = get_int_input(values['textbox'], False)
                    rooms = [Room()] * num_of_rooms
                    window.close()
                    return rooms
                case None | "CLOSE":
                    sys.exit()
                case _: 
                    pass
        


##### Public Functions ##### 
def get_float_input(usr_input, allow_zero):
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

        if not valid_input or (not allow_zero and user_input == 0) or user_input < 0:
            layout = [[sg.Text('Error: Please enter a positive, non-zero, whole number:')], [sg.Multiline(size=(30,5), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
            window = sg.Window("Paint Calculator", layout) 
        elif valid_input:
            window = sg.Window("Paint Calculator") 
            window.close()
            return user_input

        while True:
          event, values = window.read()
          if event == "CONFIRM":
              usr_input = values['textbox']
              window.close()
              break
          elif event == "CLOSE":
              sys.exit()
    
def get_int_input(usr_input, allow_zero):
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

        if not valid_input or (not allow_zero and user_input == 0) or user_input < 0:
            layout = [[sg.Text('Error: Please enter a positive, non-zero, whole number:')], [sg.Multiline(size=(30,1), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
            window = sg.Window("Paint Calculator", layout)  
        elif valid_input:
            window = sg.Window("Paint Calculator") 
            window.close()
            return user_input

        window.refresh()
        while True:
          event, values = window.read()
          if event == "CONFIRM":
              usr_input = values['textbox']
              window.close()
              break
          elif event == "CLOSE":
              sys.exit()


def clear_console():
    import os
    clear = lambda: os.system('clear')

if __name__ == '__main__':
    calculator = Calculator()
    calculator.main()