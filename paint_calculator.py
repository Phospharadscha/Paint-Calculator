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
    RED = [1.00, 1.25, 0.75]
    BLUE = [1.25, 1.25, 0.5]
    GREEN = [ 2.75, 0.75, 1.34]
    
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
    
### A wall
class Wall():
    def __init__(self):
        self.paint = Paint.RED
        self.shape = Shape.SQUARE
        self.surface_area = 0.0
        self.paint_required = 0.0
        self.coats = 1
        self.protrustions = []
        
    def define(self):
        self.colour = self._get_paint()
        self.shape = self._get_shape()
        self.surface_area = self._calc_area()
    
    def cost(self):
        litres_required = (self.surface_area * self.coats) // self.paint[2]
        buckets_required = round(litres_required // self.paint[1])
        
        return buckets_required * self.paint[0]
        
        

        
    def _get_paint(self):
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

    def _get_shape(self):
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
    
    def _calc_area(self):
        wall_surface_area = None
        
        if self.shape is Shape.SQUARE:
            base_metres = get_float_input("Please enter the length of one side of your wall in metres: ")
            wall_surface_area = self.shape(base_metres)
        elif self.shape is Shape.RECTANGLE or self.shape is Shape.PARALLELOGRAM or self.shape is Shape.TRIANGLE:
            base_metres = get_float_input("Please enter the length of the base of your wall in metres: ")
            height_metres = get_float_input("Please enter the the height of your wall in metres: ")
            wall_surface_area = self.shape(base_metres, height_metres)
        elif self.shape is Shape.TRAPEZOID:
            base_metres = get_float_input("Please enter the length of the base of your wall in metres: ")
            top_metres = get_float_input("Please enter the length of the top of your wall in metres: ")
            height_metres = get_float_input("Please enter the the height of your wall in metres: ")
            wall_surface_area = self.shape(base_metres, height_metres, top_metres)
        elif self.shape is Shape.ELLIPSE:
            vertical_metres = get_float_input("Please enter the vertical radius of your wall in metres: ")
            horizontal_metres = get_float_input("Please enter the horizontal radius of your wall in metres: ")
            wall_surface_area = self.shape(horizontal_metres, vertical_metres)
        elif self.shape is Shape.CIRCLE or self.shape is Shape.SEMICIRCLE:
            radius_metres = get_float_input("Please enter the radius of your wall in metres: ")
            wall_surface_area = self.shape(radius_metres)
            
        return wall_surface_area
    
    def _calc_required_volume(self):
        return self.surface_area / self.paint.coverage_per_unit

# Rooms
class Room():
    def __init__(self):
        self.walls = []
    
    def define(self):
        num_of_walls = get_int_input("Please enter the number of walls for this room: ")
        
        valid_input = False
        while not valid_input:
            try:
                self.walls = [Wall()] * num_of_walls
                valid_input = True 
            except: 
                num_of_walls = get_int_input("Error! Please enter the number of walls for this room as a whole number: ")
        
        for wall in self.walls:
            wall.define()

### The Calculator
class Calculator():
    def __init__(self):
        self.rooms = self._get_rooms() 
        
    # def calc_cost(self):
    #     for room in self.rooms:
    #         for wall in room:
    #             cost += wall.colour.cost

    def _get_rooms(self):
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


    def _get_paint_details(self):
        paint_name = input("What is the name/colour is the paint? ")   
        valid_input = False
        while not valid_input:
            confirmation = input("Are you sure you would like to identify this paint as: %s? (Y/N): "% paint_name).lower()  
            if confirmation == 'y' or confirmation == 'yes':
                valid_input = True
                break;
            elif confirmation == 'n' or confirmation == 'no':
                paint_name = input("Please enter a new identifier: ")
            else:
                print("Error: You have not provided a valid answer!")   
        paint_coverage = get_float_input("Please enter the many square meters your paint can cover per litre of paint: ")  
        return (paint_name, paint_coverage)


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
    
    # Iterate through all walls 
    for wall in calculator.Walls:
        print("For the specified wall, you would need %.2f litres of the %s paint" % (wall.paint_required, wall.paint.colour))
    

# GUI (Do last): https://realpython.com/pysimplegui-python/

# TODO
# Output floats as rounded up values
# Divide pre-existing functions into smaller, more specific functions
# Implement doors/windows
# Implement multiple paints
# Implement multiple walls
# Simple GUI
# Maybe store the walls as rooms. Do this after I have multiple walls implemented 
# Once paints are tied to individual walls, ask how many coats need to be applied. 
# Cost of paint
# Paint colours as enum
# Convert lists into tuples
# Saving to a file 


# Assumptions :
# Buying paint by volume, not by bucket.
# User will choose their own paints, and not have to select the paint from a table, or some other data storage system.
# Distance measurements in metres
# Liquid measurements in litres
