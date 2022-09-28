from abc import abstractmethod
from asyncio import constants
from email.utils import parseaddr
from enum import Enum
from functools import total_ordering
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
            
    def to_string(self):
        return self.name.lower()
            

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
        for i in range(0, num_of_obstacles):
            self.__obstacles.append(Obstacle())
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
        if len(self.__obstacles) != 0: 
            self.__area_with_obstacles
        window.close()
    
    def required_buckets(self):
        litres_required = (self.__surface_area * self.__coats) // self.__paint(2)
        return  round(litres_required // self.__paint(1))
    
    def get_cost(self):
        return self.required_buckets() * self.__paint(0)
    
    def get_paint(self): 
        return self.__paint
    
    def __area_with_obstacles(self):
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
    
    def get_name(self):
        return self.__name
    
    def get_cost(self):
        total_cost = 0
        for wall in self.__walls:
            total_cost += wall.get_cost()
            
        return total_cost
        
    def get_paint(self):
        pass
        
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
                    num_of_rooms = get_int_input(values['walls'], False)
                    for i in range(0, num_of_rooms):
                        self.__walls.append(Wall()) 
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
            wall_index += 1

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
                    self.__total_cost()
                    window.Enable()
                case "Total Paint":
                    window.Disable()
                    self.__total_paint()
                    window.Enable()
                case "Per Room": 
                    window.Disable()
                    self.__per_room()
                    window.Enable()
                case None | "CLOSE":
                    sys.exit()
                    break
                case _: 
                    sys.exit()
                    break

        window.close()
        
    def __total_cost(self):
        import PySimpleGUI as sg
        
        total_cost = 0
        for room in self.__rooms:
            for wall in room.get_walls():
                total_cost += wall.get_cost()
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
    def __total_paint(self):
        import PySimpleGUI as sg
        
        total_paint = {}
        
        for room in self.__rooms:
            for wall in room.get_walls():
                paint_colour = wall.get_paint()            
                total_paint[wall.get_paint()] = wall.required_buckets()
                
        temp_layout = []
        
        for key, value in total_paint.items():
            temp_layout.append([sg.Text("Total %s: %.2f" % (key.to_string(), value))])
        temp_layout.append( [sg.Button("OK")])
        
        temp_window = sg.Window("Total Paint", temp_layout)
        while True:
            event, values = temp_window.read()
            match event:
                case None | "OK":
                    temp_window.close()
                    break
                case _: 
                    temp_window.close()
                    break
        

    def __per_room(self):
        import PySimpleGUI as sg
        
        temp_layout = [
            [sg.Text("Please select a room: ")] 
        ]
        
        name_check = []
        for room in self.__rooms:
            if room.get_name() not in name_check:
                name_check.append(room.get_name())
                temp_layout.append([sg.Button(room.get_name())])
            
        temp_layout.append([sg.Button("OK")])
        
        temp_window = sg.Window("Per Room", temp_layout)
        while True:
            event, values = temp_window.read()
            match event:
                case None | "OK":
                    temp_window.close()
                    break
                case _: 
                    for room in self.__rooms:
                        if event == room.get_name():
                            temp_window.Disable()
                            self.__room_info(room)
                            temp_window.Enable()
        

    def __room_info(self, room):
        import PySimpleGUI as sg 
        
        layout = [
            [sg.Text("Room: %s" % room.get_name())], 
            [sg.Button("Cost")],
            [sg.Button("Paint")],
            [sg.Button("CLOSE")]
        ]
        
        window = sg.Window("Per Room", layout)
        while True:
            event, values = window.read()
            match event:
                case "Cost":
                    cost = room.get_cost()
                    temp_layout = [
                        [sg.Text("Total Cost: %.2f" % cost)], 
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
                case "Paint":
                    total_paint = {}
        
                    for room in self.__rooms:
                        for wall in room.get_walls():
                            paint_colour = wall.get_paint()            
                            total_paint[wall.get_paint()] = wall.required_buckets()

                    temp_layout = []

                    for key, value in total_paint.items():
                        temp_layout.append([sg.Text("Total %s: %.2f" % (key.to_string(), value))])
                    temp_layout.append( [sg.Button("OK")])

                    temp_window = sg.Window("Total Paint", temp_layout)
                    while True:
                        event, values = temp_window.read()
                        match event:
                            case None | "OK":
                                temp_window.close()
                                break
                            case _: 
                                temp_window.close()
                                break
                case None | "CLOSE":
                    window.close()
                    break
                case _: 
                    window.close()
                    break
                
        
       
        
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
                    rooms = [] 
                    for i in range(0, num_of_rooms):
                        rooms.append(Room())
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

        if not valid_input or user_input < 0:
            text = "'Error: Please enter a positive, "
            if not allow_zero:
                text += "non zero, "
            text += "number: "
            layout = [[sg.Text(text)], [sg.Multiline(size=(30,1), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
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

        if not valid_input or user_input < 0:
            # append the non-zero bit here
            text = "'Error: Please enter a positive, "
            if not allow_zero:
                text += "non zero, "
            text += "whole number: "
            layout = [[sg.Text(text)], [sg.Multiline(size=(30,1), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
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
    
# TODO - Important
# Change box headers to suit context
# Mention what measurement is being used
# Implement a test
    # Pytest
# Dictionary for total paints



# Assumptions :
# Buying paint by bucket, not raw volume 
# User will choose their own paints, and not have to select the paint from a table, or some other data storage system.
# Distance measurements in metres
# Liquid measurements in litres
# This is a system that will be deployed by a company. They will specify what paints are available.
    # User does not specify paints
