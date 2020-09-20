import glfw
from OpenGL.GL import *
import numpy as np

#transformation matrix which is homogemeous coordinate 3 by 3 
gComposedM = np.identity(3)


#define key : homogeneous coordinate matrix     
key_matrix = { glfw.KEY_W: np.array([[0.9,0.,0.],
                                    [0.,1.,0.],
                                    [0.,0.,1.]]),
              glfw.KEY_E:np.array([[1.1,0.,0.],
                                   [0.,1.,0.],
                                   [0.,0.,1.]]) ,
              glfw.KEY_S: np.array([[np.cos(np.radians(10)), -np.sin(np.radians(10)),0.],
				                    [np.sin(np.radians(10)), np.cos(np.radians(10)),0.],
				                    [0., 0., 1.]]),
              glfw.KEY_D: np.array([[np.cos(np.radians(-10)),-np.sin(np.radians(-10)),0.],
                                    [np.sin(np.radians(-10)), np.cos(np.radians(-10)),0.],
                                    [0.,0.,1.]]), 
              glfw.KEY_X: np.array([[1.,-0.1,0.],
                                    [0.,1.,0.],
                                    [0.,0.,1.]]),
              glfw.KEY_C: np.array([[1.,0.1,0.],
                                    [0.,1.,0.],
                                    [0.,0.,1.]]),
              glfw.KEY_R: np.array([[1.,0.,0.],
                                    [0.,-1.,0.],
                                    [0.,0.,1.]])
            }


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


def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if action == glfw.PRESS:
        #when press key 1, reset gComposedM in identity matrix
        if key == glfw.KEY_1 :
            gComposedM = np.identity(3)
        else :
            gComposedM = key_matrix[key] @ gComposedM 
def main():
     
    #initialize glfw
    if not glfw.init():
        return
   
    #initialize window
    window = glfw.create_window(480,480,"2016025687",None,None)       
    if not window:
        glfw.terminate()
        return

    #set key callback function    
    glfw.set_key_callback(window, key_callback)
   
    glfw.make_context_current(window)

    #set number of screen refresh to wait before calling glfw.swap_buffer()
    glfw.swap_interval(1)


    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render(gComposedM)
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
