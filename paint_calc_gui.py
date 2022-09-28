from abc import abstractmethod
from asyncio import constants
from email.utils import parseaddr
from enum import Enum
from functools import total_ordering
import math
from tkinter import Button 
import PySimpleGUI as sg
import sys

# Global var for icon

#########################################################################################
##################################### Enums #############################################
#########################################################################################

# Shapes
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

# Paints
class Paint(Enum):
    """Paints are stored by their colour, with the value being the:
    (Price per bucket, litres per bucket, coverage per litre)
    Error handling is not needed, because the user will only ever select from a drop down.
    """
    EMERALD = (24, 2.5, 13)
    SAPPHIRE = (20, 2.5, 13)
    WHITE = (45, 2.5, 12)
    BLACK = (20, 2.5, 13)
    BERRY = (20, 2.5, 13)
    COTTON = (10, 0.75, 16)
    PEBBLE = (32, 5, 13)
    IVORY = (10, 5, 13)
    
    def __call__(self, args):
        """Override the usual call method. 
        The method can be passed an argument, which will be used to return one element from the list value of the paint. 
        """
        return self.value[args]
    
    @classmethod
    def to_paint(self, paint_name):
        """This is a class method, meaning it does not need to be called on a Paint object.
        The method is passed a string, which it will then attempt to return a matching paint for.  
        """
        # Iterates through all paints until a matching paint is found. Then returns that paint. 
        for paint in self:
            if paint_name.lower() == paint.name.lower():
                return paint
        
        #if no match is found, then return white as a default value. 
        return Paint.WHITE 

#########################################################################################
################################### Classes #############################################
#########################################################################################

class Architecture():
    """The parent class of Wall() and Obstacle(). 
    An architecture object has an area- which can be calculated, and an index used to specify when asking for user input. 
    Shape and dimensions are not stored, because they are not needed once area has been calculated. 
    """
    def __init__(self):
        self.__surface_area = 0  
        self.__index = 0
        self.__shape = Shape.SQUARE

    @abstractmethod
    def define(self):
        pass

    def _area(self):
        return self.__surface_area

    def _calc_area(self, shape, dimensions):
        """This area is used to calculate the area of an Architecture object.  
        It takes a provided shape (the shape of the architecture object), and its dimensions. 
        """
        surface_area = 0
        
        # It uses the provided shape to call the lambda function assigned with it to calculate area. 
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
            return surface_area

class Wall(Architecture):
    """A wall is a child class of Architecture. 
    Walls have additional methods to find the required number of buckets and the cost to paint the wall. 
    """
    def __init__(self):
        """init is overrided due to additional variables.
        All values are assigned as a defualt and updated later. 
        """
        self.__paint = Paint.WHITE
        self.__surface_area = 0.0
        self.__coats = 1
        self.__obstacles = []
        
    def define(self, shape, colour, num_of_obstacles):  
        """Deine in wall is used to specify the details of the wall, including:
        - Dimensions
        - Number of coats they want to apply
        """
        
        # Populates self.__obstacles with the supplied number of Obstacle objects
        num_of_values = 0 
        for i in range(0, num_of_obstacles):
            self.__obstacles.append(Obstacle())
        obstacle_index = 1
        
        # Define each obstacle before defining the wall
        for obstacle in self.__obstacles:
            obstacle.define(obstacle_index, len(self.__obstacles))
            obstacle_index += 1 
        
        # Define the layout for the prompt window so that it asks for the variables required of the supplied shape. 
        # E.g. a square only needs the length of one side, but a rectangle needs the height and width. 
        # num_of_values is used later to specify the number of expected inputs later. 
        match shape:
            case Shape.RECTANGLE | Shape.PARALLELOGRAM | Shape.TRIANGLE:
                num_of_values = 2 
                layout = [
                    [sg.Text("Please enter the details for this wall:")], 
                    [sg.Text("Enter the length of the base of the wall in metres:")], 
                    [sg.Multiline(size=(30,1), key='val1')], 
                    [sg.Text("Enter the height of the wall in metres:")], 
                    [sg.Multiline(size=(30,1), key='val2')]
                ]
            case Shape.TRAPEZOID:
                num_of_values = 3 
                layout = [
                    [sg.Text("Please enter the details for this wall:")], 
                    [sg.Text("Enter the length of the base of the wall in metres:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the height of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Text("Enter the length of the top of the wall in metres:")], 
                    [sg.Multiline(size=(30,1), key='val3')]
                ]
            case Shape.ELLIPSE:
                num_of_values = 2
                layout = [
                    [sg.Text("Please enter the details for this wall:")], 
                    [sg.Text("Enter the vertical radius the wall in metres:")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the horizontal radius the wall in metres:")], 
                    [sg.Multiline(size=(30,1), key='val2')] 
                ]
            case Shape.CIRCLE | Shape.SEMICIRCLE:
                num_of_values = 1
                layout = [
                    [sg.Text("Please enter the details for this wall:")], 
                    [sg.Text("Enter the radius the wall:")], 
                    [sg.Multiline(size=(30,1), key='val1')]
                ]
            case _: # Default case is a square
                num_of_values = 1 
                layout = [
                    [sg.Text("Please enter the details of this wall:")], 
                    [sg.Text("Enter the length of one side of the wall:")], 
                    [sg.Multiline(size=(30,1), key='val1')]     
                ]
        
        # This is shared across all shapes. So it is simply added at the end. 
        layout.append([sg.Text("Enter the number of coats of paint you plan to apply to the wall:")])
        layout.append([sg.Multiline(size=(30,1), key='paint')])
        layout.append([sg.Button("CONFIRM")])
        layout.append([sg.Button("CLOSE")])

        
        # Draw the new window 
        window = sg.Window("Wall Definition" , layout)
        
        dimensions = []
        coats = 0
        
        # Until loop (keep the window open) until a valid input is given     
        while True:
          event, values = window.read()
          
          # Match the event (user interaction)
          match event:
              case "CONFIRM":
                # If the user presses the confirm button, then retrieve all of thir inputs 
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
        
        # Assign inputted values
        self.__paint = colour
        self.__coats = coats
        
        window.Disable()
        
        # Calculate the area of the wall
        self.__surface_area = self._calc_area(shape, dimensions)
       
        # If there are obstacles, then remove their surface area from the wall. 
        if len(self.__obstacles) != 0: 
            self.__area_with_obstacles
        window.close()
    
    def required_buckets(self):
        """Returns the amount of paint required to cover the wall. 
        """
        import math
        
        litres_required = (self.__surface_area * self.__coats) // self.__paint(2)
        
        # Value is rounded up, since you can't purchase .something of a bucket. 
        return math.ceil(litres_required // self.__paint(1))
    
    def get_cost(self):
        """Returns the cost of covering the wall.
        """
        return self.required_buckets() * self.__paint(0)
    
    def get_paint(self): 
        """Returns the paint used on the wall. 
        """
        return self.__paint
    
    def __area_with_obstacles(self):
        """Calculates the area of the wall when accounting for obstacles
        """
        
        for obstacle in self.__obstacles:
            self.__surface_area -= obstacle._area()

class Obstacle(Architecture): 
    """Obstacle is a child of the Architecture() class. 
    Obstacles would be anything on the wall that cannot be painted. Such as doors or windows. 
    The user is never asked to specify what the obstacle is, because it ultimately doesn't matter. 
    What matters, is the shape of the obstacle.
    """
    
    def define(self, index, total_num):
        """Like in the Wall() class, define is used here to retrieve information about the obstacle. 
        """
        
        # Valid Shapes     
        shape_types = ["Square", "Rectangle", "Parallelogram", "Trapezoid", "Triangle", "Ellipse", "Circle", "Semicircle"]
        
        layout = [
                [sg.Text("Obstacle No.%d of %d" % (index, total_num))], 
                [sg.Text("Please enter the details for this obstacle:")], 
                [sg.Text("Please select the shape of the obstacle from the drop down menu: ")], 
                [sg.OptionMenu(values=shape_types,size=(30,8), default_value='Square',key='shape')],
                [sg.Button("CONFIRM")],
                [sg.Button("CLOSE")]
            ] 
        
        # Create a window and keep it open until a valid interaction is given. 
        window = sg.Window("Obstacle Definition", layout)
        while True:
            event, values = window.read()
            match event:
                case "CONFIRM":
                    # When the user clicks confirm, convert the input into a shape object
                    shape = Shape.to_shape(values['shape'].lower())
                    break 
                case None | "CLOSE":
                    sys.exit()
                case _: 
                    pass
        
        # Freeze the window so the user cannot interact with it.
        # This is because we will be making a new window, and do not want them to interact with this current one whilst it is open. 
        window.Disable()
        self.__define_area(shape)   
        window.close()
        
    def __define_area(self, shape):
        '''This is used to define the area of the obstacle.
        The area itself is calculated within the Shape object.
        '''
        
        # Generate different window layouts depending upon the shape. 
        match shape:
            case Shape.RECTANGLE | Shape.PARALLELOGRAM | Shape.TRIANGLE:
                num_of_values = 2 
                layout = [
                    [sg.Text("Please enter the details for this obstacle:")], 
                    [sg.Text("Enter the length of the base of the obstacle in metres:")], 
                    [sg.Multiline(size=(30,1), key='val1')], 
                    [sg.Text("Enter the height of the obstacle:")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                ]
            case Shape.TRAPEZOID:
                num_of_values = 3 
                layout = [
                    [sg.Text("Please enter the details for this obstacle:")], 
                    [sg.Text("Enter the length of the base of the obstacle in metres::")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the height of the obstacle in metres::")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                    [sg.Text("Enter the length of the top of the obstacle in metres::")], 
                    [sg.Multiline(size=(30,1), key='val3')],  
                ]
            case Shape.ELLIPSE:
                num_of_values = 2
                layout = [
                    [sg.Text("Please enter the details for this obstacle:")], 
                    [sg.Text("Enter the vertical radius the obstacle in metres::")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                    [sg.Text("Enter the horizontal radius the obstacle in metres::")], 
                    [sg.Multiline(size=(30,1), key='val2')], 
                ]
            case Shape.CIRCLE | Shape.SEMICIRCLE:
                num_of_values = 1
                layout = [
                    [sg.Text("Please enter the details for this obstacle in metres::")], 
                    [sg.Text("Enter the radius the obstacle in metres::")], 
                    [sg.Multiline(size=(30,1), key='val1')],
                ]
            case _: # Default case is a square
                num_of_values = 1 
                layout = [
                    [sg.Text("Please enter the details for this obstacle in metres::")], 
                    [sg.Text("Enter the length of one side of the obstacle in metres::")], 
                    [sg.Multiline(size=(30,1), key='val1')], 
                ]     
        
        # These buttons are shared regardless of the shape. So they are appended afterwards. 
        layout.append([sg.Button("CONFIRM")])
        layout.append([sg.Button("CLOSE")])
        
        # Create a new window with the above layout. 
        window = sg.Window("Paint Calculator", layout)
        
        dimensions = []
        coats = 0
        
        # Keep the window open until a valid interaction is made.       
        while True:
          event, values = window.read()
          match event:
              case "CONFIRM":
                # If the user clicks confirm, then attempt to get their inputs what they entered. 
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
        
        # The surface area of the obstacle is calculated and assigned. 
        window.Disable()        
        self.__surface_area = self._calc_area(shape, dimensions)
        window.close()

class Room():
    '''Rooms do not inherit from Architecture as they do not share enough with how they have been defined. 
    Instead, a room is functionally a collection of Wall() objects, with its own methods. 
    '''
    def __init__(self):
        self.__walls = []
        self.__name = "default room"
        self.__index = 0
    
    def get_walls(self):
        return self.__walls
    
    def get_name(self):
        return self.__name
    
    def get_cost(self):
        """Calculates the total cost to paint the room by finding the cost of every wall and adding them together
        """
        total_cost = 0
        for wall in self.__walls:
            total_cost += wall.get_cost()
            
        return total_cost
        
    def define(self, room_index):
        """Used to define the room itself.
        It it just passed an index, which is used so the user can keep track of what room they are defining.
        """
        
        self.__index = room_index
        
        # Create a window to ask for user input
        # They will enter the details for the wall 
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
        window = sg.Window("Room Definition", layout)
        
        # Keep the window open until a valid input is given 
        while True:
            event, values = window.read()
            match event:
                case "CONFIRM":
                    # Once the user clicks confirm, attempt to store their inputs
                    self.__name = values['name']

                    num_of_rooms = get_int_input(values['walls'], False)
                    # Populate self.__walls() with the relative number of Wall() objects
                    # They will be defined later
                    for i in range(0, num_of_rooms):
                        self.__walls.append(Wall()) 
                    break 
                case None | "CLOSE":
                    sys.exit()
                case _: 
                    pass
        
        # Populate the room
        # This is in regards to getting information on each wall
        window.Disable()
        self.__populate()
        window.close()
        
    def __populate(self): 
        '''The room is populated by get details on each wall within the room, and then defining the Wall() objects
        '''
        
        # Valid shapes and colour choices used in the drop down menu 
        shapes = ["Square", "Rectangle", "Parallelogram", "Trapezoid", "Triangle", "Ellipse", "Cirlce", "Semicicle"]        
        colours = []
        for colour in Paint:   
            colours.append(colour.name.title())
        
        
        wall_index = 1
        for wall in self.__walls:
            shape = "Square"
            
            # For each wall create a new window which will ask the user to enter information on that wall. 
            layout = [
                    [sg.Text("Wall No.%d of %d in %s" % (wall_index, len(self.__walls), self.__name))], 
                    [sg.Text("Please enter the number of obstacles (doors/windows/areas that cannot be painted): ")], 
                    [sg.Multiline(size=(30,1), key='obstacles')], 
                    [sg.Text("Please select the shape of the wall from the drop down menu: ")], 
                    [sg.OptionMenu(values=shapes,size=(30,8), default_value='Square',key='shape')],
                    [sg.Text("Please select the colour of the wall from the drop down menu: ")], 
                    [sg.OptionMenu(values=colours,size=(30,8), default_value='White',key='colour')],
                    [sg.Button("CONFIRM")],
                    [sg.Button("CLOSE")]
                ]
            wall_index += 1
            window = sg.Window("Room Definition", layout)

            # Keep window open until valid input is given
            while True:
                event, values = window.read()
                match event:
                    case "CONFIRM":
                        # When the user clicks confirm, attempt to store their inputs
                        
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
        
class Calculator():
    '''Calculator is the main class for running the program.
    This is where the base windows are called from in the hierarchy of windows. It is also where the program loop is located
    '''
    
    def __init__(self):       
        self.__rooms = []
     
    def main(self):
        '''Main simply loops through until the user closes the program.
        On the final screen, the user can choose to restart. Which will return to the loop. 
        '''
        while True:
            # Get the number of rooms
            self.__rooms = self.__get_rooms()

            # Define and populate each room
            room_index = 1
            for room in self.__rooms:
                room.define(room_index)
                room_index += 1

            # Present the final screen where the user can get the results
            self.__final_screen()

        

    def __final_screen(self): 
        '''This is the final window.
        Here, the user can ask for:
        - Total cost
        - Total number of puckets per paint
        - Per Room:
            - Cost
            - Number of buckets of each paint
        '''
        
        # Create a new window to present results to the user 
        layout = [
            [sg.Text("All values have been entered!")], 
            [sg.Text("Please select an option below: ")], 
            [sg.Button("Total Cost")],
            [sg.Button("Total Paint")],
            [sg.Button("Per Room")],
            [sg.Button("START AGAIN")], 
            [sg.Button("CLOSE")]
        ]
        window = sg.Window("Paint Calculator", layout)

        # Loop until valid input is given
        while True:
            event, values = window.read()
            match event:
                case "Total Cost":
                    # Call the total_cost() method, which will present a pop up with the costs 
                    window.Disable()
                    self.__total_cost()
                    window.Enable()
                case "Total Paint":
                    # Call the total_paint() method, which will present a pop up with the total number of buckets required for each paint used 
                    window.Disable()
                    self.__total_paint()
                    window.Enable()
                case "Per Room": 
                    # Call the per_room() method
                    # This method creates a new winodw where the user can select one of their defined rooms
                    window.Disable()
                    self.__per_room()
                    window.Enable()
                case "START AGAIN":
                    # Exit this method and return to the main loop
                    window.close()
                    print("Test")
                    break
                case None | "CLOSE":
                    sys.exit()
                case _: 
                    sys.exit()
        
    def __total_cost(self):
        '''Calculates the total cost for all rooms.
        '''
        # Iterates through each room, then each wall in each room, and adds the cost of that wall to the total 
        total_cost = 0
        for room in self.__rooms:
            for wall in room.get_walls():
                total_cost += wall.get_cost()
            
        # Popup window created to present cost to user.     
        temp_layout = [
            [sg.Text("Total Cost: £%.2f" % total_cost)], 
            [sg.Button("OK")]
        ] 
        temp_window = sg.Window("Total Cost", temp_layout)
        
        # Keep window open until valid input is given
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
        '''Calculate the total number of buckets required for each paint used. 
        This is across all rooms.
        '''
        # Iterate through each room, then each wall in each room, and retrieve the amount of paint needed. 
        # This is stored as a dictionary, with the {Paint: total cost}
        total_paint = {}
        for room in self.__rooms:
            for wall in room.get_walls():  
                keys = total_paint.keys()
                if wall.get_paint() in keys:
                    total_paint[wall.get_paint()] += wall.required_buckets()
                else: 
                    total_paint[wall.get_paint()] = wall.required_buckets()
            
        # Generate a layout so that the correct number of paints are displayed.     
        temp_layout = []
        for key, value in total_paint.items():
            temp_layout.append([sg.Text("Total %s: %.2f litres" % (key.name.title(), value))])
        temp_layout.append( [sg.Button("OK")])
        
        # Create new popup window to display result 
        temp_window = sg.Window("Total Paint", temp_layout)
        
        # Keep window open until valid input is given
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
        '''This method allows the user to view a list of rooms they have specified
        They can then select a room, and view information on that room.
        '''
        
        # the layout is appended to for each room 
        layout = [
            [sg.Text("Please select a room: ")] 
        ]
        
        # Iterate through each room 
        # If rooms have duplicate names, then only one button is added
        # In this case, both rooms will be presented one after the other 
        name_check = []
        for room in self.__rooms:
            if room.get_name() not in name_check:
                name_check.append(room.get_name())
                layout.append([sg.Button(room.get_name())])
        layout.append([sg.Button("OK")])
        
        # Create new window
        temp_window = sg.Window("Per Room", layout)
        
        # Keep window open until valid input is given 
        while True:
            event, values = temp_window.read()
            match event:
                case None | "OK":
                    temp_window.close()
                    break
                case _: 
                    # If the user selects a room, then iterate through the list of rooms until one with a matching name is found
                    # Then, call the room_info() method with that room
                    for room in self.__rooms:
                        if event == room.get_name():
                            temp_window.Disable()
                            self.__room_info(room)
                            temp_window.Enable()
        

    def __room_info(self, room):
        '''Allows the user to view individual information on each room
        '''
        
        # Generate layout for the window, then create the window
        layout = [
            [sg.Text("Room: %s" % room.get_name())], 
            [sg.Button("Cost")],
            [sg.Button("Paint")],
            [sg.Button("CLOSE")]
        ]
        window = sg.Window("Per Room", layout)
        
        # Keep window open until valid input is given
        while True:
            event, values = window.read()
            match event:
                case "Cost":
                    # Display the cost fort this room in a popout window
                    cost = room.get_cost()
                    temp_layout = [
                        [sg.Text("Total Cost: £%.2f" % cost)], 
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
                    # Calculate the total amount of each paint used
                    # This is stored in a dict = {Paint : Total cost}
                    total_paint = {}
        
                    # Get the paint used in each room and add it
                    for room in self.__rooms:
                        for wall in room.get_walls():  
                            keys = total_paint.keys()
                            if wall.get_paint() in keys:
                                total_paint[wall.get_paint()] += wall.required_buckets()
                            else: 
                                total_paint[wall.get_paint()] = wall.required_buckets()

                    
                    # Create a layout to display each used paint and the amount required
                    temp_layout = []
                    for key, value in total_paint.items():
                        temp_layout.append([sg.Text("Total %s: %.2f litres" % (key.name.title(), value))])
                    temp_layout.append( [sg.Button("OK")])

                    # Create popup window to display information
                    temp_window = sg.Window("Total Paint", temp_layout)
                    
                    # Keep window open until valid input is given
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
        '''Get the number of rooms which are being painted
        '''
        layout = [[sg.Text('Please enter the number of rooms you wish to paint in the box below:')], [sg.Multiline(size=(30,1), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]] 
        window = sg.Window("Paint Calculator", layout)
        
        # Keep window open until valid input is given
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
        


#########################################################################################
############################## Error - Handling #########################################
#########################################################################################

def get_float_input(usr_input, allow_zero):
    """ Returns a provided string input as a float. 
    When called, you can specify if you want the a valid input to be non-zero, or if zero can be included. 
    """
    
    # Temporary assignment of values
    user_input = ""
    valid_input = False
    
     # Loops until a valid input is given
    while True:
        # Attempt casting of string into float
        try:
            user_input = float(usr_input)
            valid_input = True
        except ValueError:
            valid_input = False

        # If the input is invalid, or if it's valid but less than 0, then:
        if not valid_input or user_input < 0 or user_input == 0:
            if allow_zero and user_input == 0:
                return user_input
            
            text = "'Error: Please enter a positive"
             # Alter string if zero is not allowed as a valid input
            if not allow_zero:
                text += ", non zero,"
            text += " number: "
            
            # Create new window asking for corrected input
            layout = [[sg.Text(text)], [sg.Multiline(size=(30,1), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
            window = sg.Window("Error! Invalid Input", layout) 
        elif valid_input:
             # Temporary window is created so that any actual window can be closed before method exits. 
            window = sg.Window("Paint Calculator") 
            window.close()
            return user_input

        window.refresh()
        while True:
          event, values = window.read()
          if event == "CONFIRM":
               # Get user input
              usr_input = values['textbox']
              window.close()
              break
          elif event == "CLOSE":
              sys.exit()
    
def get_int_input(usr_input, allow_zero):
    """ Returns a provided string input as an integer. 
    When called, you can specify if you want the a valid input to be non-zero, or if zero can be included. 
    """
    
    # Temporary assignment of values
    user_input = ""
    valid_input = False
    
    # Loops until a valid input is given
    while True:
        # Attempt casting of string into int 
        try:
            user_input = int(usr_input)
            valid_input = True
        except ValueError:
            valid_input = False

        # If the input is invalid, or if it's valid but less than 0, then:
        if not valid_input or user_input < 0 or user_input == 0 :
            if allow_zero and user_input == 0:
                return user_input
            
            text = "'Error: Please enter a positive"
            # Alter string if zero is not allowed as a valid input
            if not allow_zero:
                text += ", non zero,"
            text += " whole number: "
            
            # Create new window asking for corrected input
            layout = [[sg.Text(text)], [sg.Multiline(size=(30,1), key='textbox')], [sg.Button("CONFIRM")], [sg.Button("CLOSE")]]
            window = sg.Window("Error! Invalid Input", layout) 
        elif valid_input:
            # Temporary window is created so that any actual window can be closed before method exits. 
            window = sg.Window("Paint Calculator") 
            window.close()
            return user_input

        window.refresh()
        while True:
          event, values = window.read()
          if event == "CONFIRM":
              # Get user input
              usr_input = values['textbox']
              window.close()
              break
          elif event == "CLOSE":
              sys.exit()

if __name__ == '__main__':
    # All of the program is run through the Calculator class
    # Create a calculator object, and then call its main() function
    calculator = Calculator()
    calculator.main()
    
# TODO - Important
# Change box headers to suit context
# Mention what measurement is being used
# Implement a test
    # Pytest



# Assumptions :
# Buying paint by bucket, not raw volume 
# Distance measurements in metres
# Liquid measurements in litres
# This is a system that will be deployed by a company. They will specify what paints are available.
    # User does not specify paints
# User does specify how many coats they intend to apply
