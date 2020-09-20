import glfw
from OpenGL.GL import *
import numpy as np


def render(T):
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
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

 
def main():
    #init glfw
    if not glfw.init():
        return
    #init window    
    window = glfw.create_window(480,480,"2016025687",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    #set the number of screen refresh to wait before calling glfw.swap_buffer()
    glfw.swap_interval(1)
     
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # get time after execute proram, and using it as radian value
        th = glfw.get_time()

        # rotatation matrix 
        R = np.array([[np.cos(th), -np.sin(th),0.],
                      [np.sin(th), np.cos(th),0.],
                      [0.,         0.,        1.]])

        # translation matrix
        T = np.array([[1.,0.,0.5],
                      [0.,1.,0.],
                      [0.,0.,1.]]) 

        # transelattion first then rotatation
        C =  R @ T
        render(C)
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()
