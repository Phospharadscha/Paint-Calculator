from enum import Enum
import math 

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
    
# A wall
class Wall():
    def __init__(self):
        self.__paint = Paint.RED
        self.__shape = Shape.SQUARE
        self.__surface_area = 0.0
        self.__coats = 1
        self.__protrustions = []
        
    def define(self):
        self.__colour = self.__get_paint()
        self.__shape = self.__get_shape()
        self.__surface_area = self.__calc_area()
    
    def required_buckets(self):
        litres_required = (self.__surface_area * self.__coats) // self.__paint(2)
        return  round(litres_required // self.__paint(1))
        
       
    
    def cost(self):
        return self.required_buckets() * self.__paint(0)
        
    def __get_paint(self):
        valid_input = False
        
        while not valid_input:
            print("Red | Green | Blue")
            colour = input("Of the colours listed above, which do you want to use on your wall? ").lower()

            paint_colour = Paint.to_paint(colour)
            if paint_colour is not None:
                colour = paint_colour
                valid_input = True
            else:
                print("Invalid Shape!")
        
        return colour

    def __get_shape(self):
        valid_input = False
        
        while not valid_input:
            print("Square | Rectangle | Parallelogram | Trapezoid | Triangle | Ellipse | Circle | Semicircle")
            wall_shape = input("Of the shapes listed above, which best describes the shape of your wall?: ").lower()

            shape_type = Shape.to_shape(wall_shape)
            if shape_type is not None:
                wall_shape = shape_type
                valid_input = True
            else:
                print("Invalid Shape!")
        
        return wall_shape
    
    def __calc_area(self):
        wall_surface_area = None
        
        if self.__shape is Shape.SQUARE:
            base_metres = get_float_input("Please enter the length of one side of your wall in metres: ")
            wall_surface_area = self.__shape(base_metres)
        elif self.__shape is Shape.RECTANGLE or self.shape is Shape.PARALLELOGRAM or self.shape is Shape.TRIANGLE:
            base_metres = get_float_input("Please enter the length of the base of your wall in metres: ")
            height_metres = get_float_input("Please enter the the height of your wall in metres: ")
            wall_surface_area = self.__shape(base_metres, height_metres)
        elif self.__shape is Shape.TRAPEZOID:
            base_metres = get_float_input("Please enter the length of the base of your wall in metres: ")
            top_metres = get_float_input("Please enter the length of the top of your wall in metres: ")
            height_metres = get_float_input("Please enter the the height of your wall in metres: ")
            wall_surface_area = self.__shape(base_metres, height_metres, top_metres)
        elif self.__shape is Shape.ELLIPSE:
            vertical_metres = get_float_input("Please enter the vertical radius of your wall in metres: ")
            horizontal_metres = get_float_input("Please enter the horizontal radius of your wall in metres: ")
            wall_surface_area = self.__shape(horizontal_metres, vertical_metres)
        elif self.__shape is Shape.CIRCLE or self.shape is Shape.SEMICIRCLE:
            radius_metres = get_float_input("Please enter the radius of your wall in metres: ")
            wall_surface_area = self.__shape(radius_metres)
            
        return wall_surface_area

# Rooms
class Room():
    def __init__(self):
        self.__walls = []
    
    def define(self):
        num_of_walls = get_int_input("Please enter the number of walls for this room: ")
        
        valid_input = False
        while not valid_input:
            try:
                self.__walls = [Wall()] * num_of_walls
                valid_input = True 
            except: 
                num_of_walls = get_int_input("Error! Please enter the number of walls for this room as a whole number: ")
        
        for wall in self.__walls:
            wall.define()
            
    def walls(self):
        return self.__walls

### The Calculator
class Calculator():
    def __init__(self):
        self.__rooms = self.__get_rooms() 
           
    def calc_cost(self):
        cost = 0
        for room in self.__rooms:
            for wall in room.walls():
                cost += wall.cost()
        
        return cost

    def __get_rooms(self):
        num_of_rooms = get_int_input("How many rooms are you wanting to paint? ")
        
        valid_input = False
        while not valid_input:
            try:
                rooms = [Room()] * num_of_rooms
                valid_input = True 
            except: 
                num_of_rooms = get_int_input("Error! Please enter the number of rooms you are wanting to paint as a whole number: ")
        
        for room in rooms:
            room.define()
            
        return rooms

def get_float_input(question):
    user_input = ""
    valid_input = False
    while not valid_input:
        try:
            user_input = float(input(question))
            valid_input = True
        except:
            print("Error: Please enter a number. Try again!")
    return user_input
    
def get_int_input(question):
    user_input = ""
    valid_input = False
    while not valid_input:
        try:
            user_input = int(input(question))
            valid_input = True
        except:
            print("Error: Please enter a number. Try again!")
    return user_input

if __name__ == '__main__':
    # Create calculator object
    calculator = Calculator()
    print("The total cost is: %.2f" % calculator.calc_cost())
    

# GUI (Do last): https://realpython.com/pysimplegui-python/

# TODO
# Implement doors/windows
# Implement multiple paints
# Implement multiple walls
# Simple GUI
# Once paints are tied to individual walls, ask how many coats need to be applied. 
# Saving to a file 


# Assumptions :
# Buying paint by volume, not by bucket.
# User will choose their own paints, and not have to select the paint from a table, or some other data storage system.
# Distance measurements in metres
# Liquid measurements in litres
