from graphics import *

WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700

win = GraphWin("client window", WINDOW_WIDTH, WINDOW_HEIGHT)


def initial_buttons():
    singIn = Rectangle(Point(25, 55), Point(255, 285))  # points are ordered ll, ur
    singUp = Rectangle(Point(25, 355), Point(255, 585))
    quit = Rectangle(Point(85, 116), Point(315, 346))

    singUp.setFill("red")
    singIn.setFill("green")
    text = Text(Point(100, 133), "Exit")
    text.draw(win)

    singUp.draw(win)
    singIn.draw(win)
    quit.draw(win)

    return singUp, singIn, quit


def inside(point, rectangle):
    """ Is point inside rectangle? """

    ll = rectangle.getP1()  # assume p1 is ll (lower left)
    ur = rectangle.getP2()  # assume p2 is ur (upper right)

    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()


left, right, quit = initial_buttons()

centerPoint = Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
text = Text(centerPoint, "")
text.draw(win)

while True:
    clickPoint = win.getMouse()

    if clickPoint is None:  # so we can substitute checkMouse() for getMouse()
        text.setText("")
    elif inside(clickPoint, left):
        text.setText("left")
    elif inside(clickPoint, right):
        text.setText("right")
    elif inside(clickPoint, quit):
        break
    else:
        text.setText("")

win.close()
