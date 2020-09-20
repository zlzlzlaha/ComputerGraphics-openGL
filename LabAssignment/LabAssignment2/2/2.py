import numpy as np
import glfw
from OpenGL.GL import *

#declare global variable for primitive type 
primitive = GL_LINE_LOOP

#compute vertex loacation 
degree = np.linspace(0,360,13)*np.pi/180
x = np.cos(degree)
y = np.sin(degree)


#Make keyboard key : primitive type dictionary
key_primitive = {
    0:GL_POLYGON,
    1:GL_POINTS,
    2:GL_LINES,
    3:GL_LINE_STRIP,
    4:GL_LINE_LOOP,
    5:GL_TRIANGLES,
    6:GL_TRIANGLE_STRIP,
    7:GL_TRIANGLE_FAN,
    8:GL_QUADS,
    9:GL_QUAD_STRIP
}
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(primitive)

    # set 12 numbers of vertexs
    for i in range(12):
        glVertex2f(x[i],y[i])
    glEnd()

def key_callback(window , key , scancode ,action, mods):
    global primitive

    #when press keyboard number key, change primitive type 
    if action==glfw.PRESS:
        primitive = key_primitive[key-glfw.KEY_0]

def main():
    #Initialize the library
    if not glfw.init() : 
        return

    #Create window size :480 * 480  
    window = glfw.create_window(480,480,"2016025687",None,None )
    
    #when failed to create window
    if not window:
        glfw.terminate()
        return

    #set key_callback function
    glfw.set_key_callback(window, key_callback)
    
    #Make window's context
    glfw.make_context_current(window)

    #Loop until the user closes the window 
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
