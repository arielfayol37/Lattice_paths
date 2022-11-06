 
import ctypes, turtle, random
user32 = ctypes.windll.user32
x_size, y_size = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
 
  
#sc=turtle.Screen()
#s=turtle.Turtle()
#trtl.up
#x_or =-0.5*x_size+200
#y_or = -y_size*0.5+200
#s.penup()
#s.setposition(x_or, y_or)
#s.pendown()
# method to draw y-axis lines
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
        s=turtle.Turtle()
        s.speed(0)
        s.width(2)
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
#s.hideturtle()
def draw_path(pat_A,m,n,o):
        x_or =-0.5*x_size+200
        y_or = -y_size*0.5+200        
        x_forward = (x_size-2*200)/m
        y_forward = (y_size-2*200)/n        
        s=turtle.Turtle()
        s.color((random.random(),random.random(),random.random()))
        s.speed(10)
        s.penup()
        s.setposition(x_or-o, y_or-o)
        s.pendown()        
        for i in pat_A:
                if i == 0:
                        s.seth(0)
                        s.forward(x_forward)
                else:
                        s.seth(90)
                        s.forward(y_forward)
        
        s.hideturtle()
