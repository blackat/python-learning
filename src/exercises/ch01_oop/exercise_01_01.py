class Rectangle:
    
    # Constructor/Initializer
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def area(self):
        return self.height * self.width

    def perimeter(self):
        return (self.height + self.width) * 2

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

    def is_square(self):
        return self.width == self.height
    

