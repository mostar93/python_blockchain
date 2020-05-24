class Car:
    # top speed = 100
    # warning = []
    ''' when attributes are declared outside of the __init__ function, they are applied to every instance of the class. 
        the init function allows for each instance to have different values for shared attributes
    '''

    def __init__(self, top_speed=100):
        self.top_speed = top_speed
        self.warnings = []
    
    def drive(self):
        print(f'i am doing {self.top_speed} miles per hour')


car1 = Car(150)
car1.drive()
print(car1.__dict__) # prints car1 as a dict. if saved, you will have a seperate dict instance of the object seperate from the OG car1 obj