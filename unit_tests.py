import unittest
import math
from enum import Enum

#########################################################################################
################################# Testing ###############################################
#########################################################################################
class TestShapes(unittest.TestCase):
        ############### Shape-related tests ############### 
    def test_area_square(self):
        lengths = [1, 10, 100, 1000, 10000]   
        square = Shape.SQUARE
        
        for length in lengths:
            self.assertEqual(square(length), length * length)
        
    def test_area_rectangle(self):
        heights = [1, 10, 100, 1000, 10000]   
        widths = [1, 10, 100, 1000, 10000]  
        rect = Shape.RECTANGLE
        
        for height in heights:
            for width in widths:
                self.assertEqual(rect(height, width), height * width)
    
    def test_area_parallelogram(self):
        bases = [1, 10, 100, 1000, 10000]   
        heights = [1, 10, 100, 1000, 10000] 
        para = Shape.PARALLELOGRAM 
        
        for base in bases:
            for height in heights:
                self.assertEqual(para(base, height), height * base)
    
    def test_area_trapezoid(self):
        bases = [1, 10, 100, 1000, 10000]   
        heights = [1, 10, 100, 1000, 10000] 
        tops = [1, 10, 100, 1000, 10000] 
        trap = Shape.TRAPEZOID 

        for base in bases:
            for height in heights:
                for top in tops:
                    self.assertEqual(trap(base, height, top), ((top + base) // 2) * height)
    
    def test_area_triangle(self):
        bases = [1, 10, 100, 1000, 10000]   
        heights = [1, 10, 100, 1000, 10000] 
        tri = Shape.TRIANGLE
        
        for base in bases: 
            for height in heights: 
                self.assertEqual(tri(base, height), (base * height) * 0.5)
    
    def test_area_circle(self):
        radis =  [1, 10, 100, 1000, 10000]
        circ = Shape.CIRCLE
  
        for radi in radis:
            self.assertEqual(circ(radi), (math.pi * pow(radi, 2))) 
    
    def test_area_semicircle(self):
        radis =  [1, 10, 100, 1000, 10000]
        scirc = Shape.SEMICIRCLE
  
        for radi in radis:
            self.assertEqual(scirc(radi), (math.pi * pow(radi, 2)) // 2)
            
    def test_string_to_shape(self):
        self.assertEqual(Shape.to_shape('square'), Shape.SQUARE)
        self.assertEqual(Shape.to_shape('rectangle'), Shape.RECTANGLE)
        self.assertEqual(Shape.to_shape('parallelogram'), Shape.PARALLELOGRAM)
        self.assertEqual(Shape.to_shape('trapezoid'), Shape.TRAPEZOID)
        self.assertEqual(Shape.to_shape('triangle'), Shape.TRIANGLE)
        self.assertEqual(Shape.to_shape('ellipse'), Shape.ELLIPSE)
        self.assertEqual(Shape.to_shape('circle'), Shape.CIRCLE)
        self.assertEqual(Shape.to_shape('semicircle'), Shape.SEMICIRCLE)
        
        self.assertEqual(Shape.to_shape('foobar'), None)
        self.assertEqual(Shape.to_shape('SQUARE'), None)
        self.assertEqual(Shape.to_shape('RECTANGLE'), None)
        self.assertEqual(Shape.to_shape('PARALLELOGRAM'), None)
        self.assertEqual(Shape.to_shape('TRAPEZOID'), None)
        self.assertEqual(Shape.to_shape('TRIANGLE'), None)
        self.assertEqual(Shape.to_shape('ELLIPSE'), None)
        self.assertEqual(Shape.to_shape('CIRCLE'), None)
        self.assertEqual(Shape.to_shape('SEMICIRCLE'), None)

class TestInputHandling(unittest.TestCase):
    
    ############### Integer-related tests ############### 
    def test_int_pos(self):
        pos_integers = ["1", "2", "10", "20", "250", "1050"]
        for i in pos_integers: 
            self.assertEqual(get_int_input(i, True), "Valid Input")
            self.assertEqual(get_int_input(i, False), "Valid Input")
    
    def test_int_negative(self):
        neg_integers = ["-1", "-2", '-10', "-20", "-250", "-1050"]
        for i in neg_integers: 
            self.assertEqual(get_int_input(i, True), 'Error: Please enter a positive whole number: ')
            self.assertEqual(get_int_input(i, False), 'Error: Please enter a positive, non zero, whole number: ')

    def test_int_zero(self):
        self.assertEqual(get_int_input("0", True), "Valid Input")
        self.assertEqual(get_int_input("0", False), 'Error: Please enter a positive, non zero, whole number: ')
    
    def test_int_float(self):
        floats = ["1.0", "2.1", "10.21", "20.321", "250.4321", "1050.54321", "-1.0", "-2.1", "-10.21", "-20.321", "-250.4321", "-1050.54321"]
        for i in floats: 
            self.assertEqual(get_int_input(i, True), 'Error: Please enter a positive whole number: ')
            self.assertEqual(get_int_input(i, False), 'Error: Please enter a positive, non zero, whole number: ') 
    
    def test_int_string(self):
        strings = ["Test", "Wall", "Room", "La-Li-Lu-Le-Lo"]
        for i in strings:
            self.assertEqual(get_int_input(i, True), 'Error: Please enter a positive whole number: ')
            self.assertEqual(get_int_input(i, False), 'Error: Please enter a positive, non zero, whole number: ')  

    ############### Float-related tests ############### 
    def test_float_pos(self):
        pos_floats = ["1.0", "2.1", "10.21", "20.321", "250.4321", "1050.54321"]
        for i in pos_floats: 
            self.assertEqual(get_float_input(i, True), "Valid Input")
            self.assertEqual(get_float_input(i, False), "Valid Input")
    
    def test_float_negative(self):
        neg_floats = ["-1.0", "-2.1", "-10.21", "-20.321", "-250.4321", "-1050.54321"]
        for i in neg_floats: 
            self.assertEqual(get_float_input(i, True), "Error: Please enter a positive number: ")
            self.assertEqual(get_float_input(i, False), "Error: Please enter a positive, non zero, number: ")
               
    def test_float_zero(self):
        self.assertEqual(get_float_input("0", True), "Valid Input")
        self.assertEqual(get_float_input("0", False), 'Error: Please enter a positive, non zero, number: ')
        
    def test_float_int(self):
        integers_pos = ["1", "2", "10", "20", "250", "1050"]
        integers_neg = ["-1", "-2", '-10', "-20", "-250", "-1050"]
        
        for i in integers_pos: 
            self.assertEqual(get_float_input(i, True), 'Valid Input')
            self.assertEqual(get_float_input(i, False), 'Valid Input') 
        
        for i in integers_neg: 
            self.assertEqual(get_float_input(i, True), 'Error: Please enter a positive number: ')
            self.assertEqual(get_float_input(i, False), 'Error: Please enter a positive, non zero, number: ')  
        
    def test_float_string(self):
        strings = ["Test", "Wall", "Room", "La-Li-Lu-Le-Lo"]
        for i in strings:
            self.assertEqual(get_float_input(i, True), 'Error: Please enter a positive number: ')
            self.assertEqual(get_float_input(i, False), 'Error: Please enter a positive, non zero, number: ')  

#########################################################################################
########################### Methods/Classes being tested ###############################
#########################################################################################
"""Methods have been altered to remove the GUI elements
Now. they Just return a string used which reference "branch" has been addressed
"""

class Shape(Enum):
    """Shapes store a lambda function used to evaluate their area
    They can then be easily calculated if I store a shape object on a wall/obstacles/etc. 
    """
    SQUARE = lambda b: pow(b, 2)
    RECTANGLE = lambda b, h: b * h
    PARALLELOGRAM = lambda b, h: b * h
    TRAPEZOID = lambda b, h, a: ((a + b) // 2) * h
    TRIANGLE = lambda b, h: 0.5 * (b * h)
    ELLIPSE = lambda b, a: math.pi * (a*b)
    CIRCLE = lambda r: math.pi * pow(r, 2)
    SEMICIRCLE = lambda r: (math.pi * pow(r, 2)) // 2
    
    def __call__(self, args):
        """Override the usual call method to instead allow for the supplying of a variety of multiple args.
        These args are then passed to the matching lambda function to calculate the respective area. 
        """
        return self.value[0](args)
    
    @classmethod
    def to_shape(self, shape_name):
        """This is a class method, meaning it does not need to be called on a Shape object.
        The method is passed a string, which it will then attempt to return a matching shape for.  
        Error handling is not needed, because the user will only ever select from a drop down. 
        """
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

def get_float_input(usr_input, allow_zero):
    """ Returns a provided string input as a float. 
    When called, you can specify if you want the a valid input to be non-zero, or if zero can be included. 
    """
    # Temporary assignment of values
    user_input = ""
    valid_input = False
    
    # Loops until a valid input is given
    # Attempt casting of string into float
    try:
        user_input = float(usr_input)
        valid_input = True
    except ValueError:
        valid_input = False

    # If the input is invalid, or if it's valid but less than 0, then:
    if not valid_input or user_input < 0 or user_input == 0:
        if allow_zero and user_input == 0:
            return "Valid Input"
        
        text = "Error: Please enter a positive"
        # Alter string if zero is not allowed as a valid input
        if not allow_zero:
            text += ", non zero,"
        text += " number: "
        
        return text
    elif valid_input:
        return "Valid Input"

def get_int_input(usr_input, allow_zero):
    """ Returns a provided string input as a float. 
    When called, you can specify if you want the a valid input to be non-zero, or if zero can be included. 
    """
    # Temporary assignment of values
    user_input = ""
    valid_input = False
    
    # Loops until a valid input is given
    # Attempt casting of string into float
    try:
        user_input = int(usr_input)
        valid_input = True
    except ValueError:
        valid_input = False

    # If the input is invalid, or if it's valid but less than 0, then:
    if not valid_input or user_input < 0 or user_input == 0:
        if allow_zero and user_input == 0:
            return "Valid Input"
        
        text = "Error: Please enter a positive"
        # Alter string if zero is not allowed as a valid input
        if not allow_zero:
            text += ", non zero,"
        text += " whole number: "
        return text
    elif valid_input:
        return "Valid Input"

if __name__ == "__main__":
    unittest.main(verbosity=2)