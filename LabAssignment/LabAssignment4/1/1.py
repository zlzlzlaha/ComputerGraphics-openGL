import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

#input key array
input_keys = []

def key_callback(window, key, scancode, action, modes):
    global input_keys  
    if action == glfw.PRESS :
        #insert preesed key in first index of list
        input_keys.insert(0,key)
     
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
    # get key list information and call gl according key
    global input_keys 
    if input_keys:
        for key in input_keys:
            #translate -0.1 to x direction
            if key == glfw.KEY_Q :
                glTranslatef(-0.1,0,0)
            # trlate 0.1 to x direction
            elif key == glfw.KEY_E:
                glTranslatef(0.1,0,0)
            #rotate by 1- degree
            elif key == glfw.KEY_A:
                glRotatef(10,0,0,1)
            #rotate by -10 degree
            elif key == glfw.KEY_D:
                glRotatef(-10,0,0,1) 
            #intialize input keys
            elif key == glfw.KEY_1:
                 input_keys = []
    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def main():

    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2016025687",None,None)

    if not window :
        glfw.terminate()
        return

    glfw.make_context_current(window) 
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
    main()

