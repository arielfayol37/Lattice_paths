import turtle, random

# Getting the screen size
canvas = turtle.Screen()
x_size = canvas.window_width()
y_size = canvas.window_height()

# Your color list
colors = [(60, 180, 75), (255, 225, 25), (245, 130, 48),(170, 110, 40), 
    (70, 240, 240),(145, 30, 180), (128, 128, 128), (240, 50, 230), 
    (210, 245, 60),(0, 130, 200), (250, 190, 212), (0, 128, 128),
    (220, 190, 255), (255, 250, 200), (128, 0, 0), (170, 255, 195), 
    (230, 25, 75),(128, 128, 0), (255, 215, 180), (0, 0, 128)]
def drawy(x_forward,x_or, y_or, s):
	
	# line
 

	s.seth(90)
	s.forward(y_size-400)
	
	# set position
	s.up()
	s.setpos(x_or + x_forward,y_or)
	s.down()
	
def drawx(y_forward,x_or,y_or,s):
	
	# line
 

	s.seth(0)
	s.forward(x_size-400)
	
	# set position
	s.up()
	s.setpos(x_or,y_or+y_forward)
	s.down()
	 
def draw_lattice(m,n):
        canvas = turtle.Screen()
        turtle.TurtleScreen._RUNNING=True
        s=turtle.Turtle()
        
        s.speed(0)
        s.width(0.7)
        #trtl.up
        x_or =-0.5*x_size+200
        y_or = -y_size*0.5+200
        s.penup()
        s.setposition(x_or, y_or)
        s.pendown()
        x_forward = (x_size-2*200)/m
        y_forward = (y_size-2*200)/n
        for i in range(m+1):
                drawy((i+1)*x_forward,x_or,y_or,s)
        s.penup()
        s.setposition(x_or, y_or)
        s.pendown()
        for j in range(n+1):
                drawx((j+1)*y_forward,x_or,y_or,s)
        s.hideturtle()
        #canvas.exitonClick()
        #s.close()
#s.hideturtle()
def draw_path(pat_A,m,n,o,index):
        canvas = turtle.Screen()
        turtle.TurtleScreen._RUNNING=True        
        x_or =-0.5*x_size+200
        y_or = -y_size*0.5+200        
        x_forward = (x_size-2*200)/m
        y_forward = (y_size-2*200)/n        
        s=turtle.Turtle()
        s.width(1.7)
        try:
                s.color(colors[index])
        except:
                s.color((random.random(),random.random(),random.random()))
        s.speed(7)
        if pat_A[0]:
                s.penup()
                s.setposition(x_or-o, y_or+10-o)
                s.pendown()        
                for i in pat_A:
                        if i == 0:
                                s.seth(0)
                                s.forward(x_forward)
                        else:
                                s.seth(90)
                                s.forward(y_forward)
        else:
                s.penup()
                s.setposition(x_or+10-o, y_or-o)
                s.pendown()        
                for i in pat_A:
                        if i == 0:
                                s.seth(0)
                                s.forward(x_forward)
                        else:
                                s.seth(90)
                                s.forward(y_forward)
        
        s.hideturtle()
        #canvas.exitonclick()
        #s.close()
