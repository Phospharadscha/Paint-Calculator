from enum import Enum
import math 

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

### A wall
class Wall():
    def __init__(self, shape, surface_area, paint):
        self.paint = paint
        self.shape = shape
        self.surface_area = surface_area
        self.paint_required = self.calculate_required_volume()
        # self.coats = coats
        # self.protrustions = []
    
    def calculate_required_volume(self):
        return self.surface_area / self.paint.coverage_per_unit

### A paint bucket
class Paint():
    def __init__(self, colour, rate_per_unit):
        self.colour = colour
        self.coverage_per_unit = rate_per_unit
        # self.volume_per_bucket = volume_per_bucket
        # self.cost = cost

class Calculator():
    def __init__(self):
        paint_details = self.get_paint_details()
        temp_paint = Paint(paint_details[0], paint_details[1])

        wall_details = self.get_wall_details()
        temp_wall = Wall(wall_details[0], wall_details[1], temp_paint)
        
        self.Walls = [temp_wall]

    def get_wall_details(self):
        wall_shape = self.get_wall_shape()
        wall_surface_area = self.calc_wall_area(wall_shape)
        
        print("The surface area of this wall is: %.2f metres squared" % wall_surface_area) if wall_surface_area is not None else print("Surface area has not been calculated correctly!")
        return (wall_shape, wall_surface_area)

    def get_float_input(self, question):
        user_input = ""
        valid_input = False

        while not valid_input:
            try:
                user_input = float(input(question))
                valid_input = True
            except:
                print("Error: Please enter a number. Try again!")

        return user_input

    def get_wall_shape(self):
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
    
    def calc_wall_area(self, wall_shape):
        wall_surface_area = None
        
        if wall_shape is Shape.SQUARE:
            base_metres = self.get_float_input("Please enter the length of one side of your wall in metres: ")
            wall_surface_area = wall_shape(base_metres)
        elif wall_shape is Shape.RECTANGLE or wall_shape is Shape.PARALLELOGRAM or wall_shape is Shape.TRIANGLE:
            base_metres = self.get_float_input("Please enter the length of the base of your wall in metres: ")
            height_metres = self.get_float_input("Please enter the the height of your wall in metres: ")
            wall_surface_area = wall_shape(base_metres, height_metres)
        elif wall_shape is Shape.TRAPEZOID:
            base_metres = self.get_float_input("Please enter the length of the base of your wall in metres: ")
            top_metres = self.get_float_input("Please enter the length of the top of your wall in metres: ")
            height_metres = self.get_float_input("Please enter the the height of your wall in metres: ")
            wall_surface_area = wall_shape(base_metres, height_metres, top_metres)
        elif wall_shape is Shape.ELLIPSE:
            vertical_metres = self.get_float_input("Please enter the vertical radius of your wall in metres: ")
            horizontal_metres = self.get_float_input("Please enter the horizontal radius of your wall in metres: ")
            wall_surface_area = wall_shape(horizontal_metres, vertical_metres)
        elif wall_shape is Shape.CIRCLE or wall_shape is Shape.SEMICIRCLE:
            radius_metres = self.get_float_input("Please enter the radius of your wall in metres: ")
            wall_surface_area = wall_shape(radius_metres)
            
        return wall_surface_area

    def get_paint_details(self):
        paint_name = input("What is the name/colour is the paint?: ")

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

        paint_coverage = self.get_float_input("Please enter the many square meters your paint can cover per litre of paint: ")

        return (paint_name, paint_coverage)


if __name__ == '__main__':
    # Create calculator object
    calculator = Calculator()
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


# Assumptions :
# Buying paint by volume, not by bucket.
# User will choose their own paints, and not have to select the paint from a table, or some other data storage system.
# Distance measurements in metres
# Liquid measurements in litres
