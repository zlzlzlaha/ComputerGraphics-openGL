import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
    # draw point p
    glBegin(GL_POINTS)
    glColor3ub(255, 255, 255)
    # use point (x,y,1)
    glVertex2fv((M @ np.array([.5,.0,1.]))[:-1])
    glEnd()
    # draw vector v
    glBegin(GL_LINES)      
    glColor3ub(255, 255, 255)
    # use vector (x,y,0)
    glVertex2fv( (M @ np.array([.0,.0,.0]))[:-1] )
    glVertex2fv( (M @ np.array([0.5,.0,.0]))[:-1] ) 
    glEnd()
   

def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2016025687",None,None)

    if not window :
        glfw.terminate()
        return

    glfw.make_context_current(window) 
   
    #set the number of screen refresh to wait before calling glfw.swap_buffer()
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        
        th = glfw.get_time()

        # do rotatation in  counter clock-wise by th radian
        R = np.array([[np.cos(th),-np.sin(th),0.],
                      [np.sin(th), np.cos(th),0.],
                      [0.,      0.,         1.]])
        # do translation by 0.5 in x direction
        T = np.array([[1.,0.,0.5],
                      [0.,1.,0.],
                      [0.,0.,1.]])

        # translate first then rotate 
        M = R @ T

        glfw.poll_events()
        render(M)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

