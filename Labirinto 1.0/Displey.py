from graphics import *

win = None

def Start(dimension_in_pixel): #run at the very start
    global win
    win = GraphWin("Maze window", dimension_in_pixel, dimension_in_pixel)
    win.setBackground('black')
    return 0

def display_square(x, y, color, pixel_for_square):
    x1, y1 = x * pixel_for_square, y * pixel_for_square
    x2, y2 = x1 + pixel_for_square, y1 + pixel_for_square

    square = Rectangle(Point(x1, y1), Point(x2, y2))
    square.setFill(color)
    square.draw(win)

    win.update()
    return 0
def display_small_square(x, y, color, pixel_for_square_big, pixel_for_square_smoll):
    x1, y1 = x * pixel_for_square_big, y * pixel_for_square_big
    x2, y2 = x1 + pixel_for_square_smoll, y1 + pixel_for_square_smoll

    square = Rectangle(Point(x1, y1), Point(x2, y2))
    square.setFill(color)
    square.draw(win)

    win.update()
    return 0
def get_click_position():
    clic_point = win.getMouse()
    x = clic_point.getX()
    y = clic_point.getY()
    return x, y

def End(): #run when the maze has no more possible mutations
    win.getMouse()
    win.close()
    return 0