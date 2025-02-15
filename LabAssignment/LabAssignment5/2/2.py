import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
    
gCamAng = 0
gComposedM = np.identity(4)
th = np.radians(10)
#make dictionary key - matrix
key_matrix = { 
                glfw.KEY_Q :  np.array([[1.0,.0,.0,-0.1,],
                                        [.0,1.0,.0,.0],
                                        [.0,.0,1.0,.0],
                                        [.0,.0,.0,1.0]]),
                glfw.KEY_E :  np.array([[1.0,.0,.0,0.1],
                                        [.0,1.0,.0,.0],
                                        [.0,.0,1.0,.0],
					                    [.0,.0,.0,1.0]]),
                glfw.KEY_W :  np.array([[1.0,.0,.0,.0],
                                        [.0,np.cos(-th),-np.sin(-th),.0],
                                        [.0,np.sin(-th),np.cos(-th),.0],
					                    [.0,.0,.0,1.0]]),
                glfw.KEY_S :  np.array([[1.0,.0,.0,.0],
                                        [.0,np.cos(th),-np.sin(th),.0],
                                        [.0,np.sin(th),np.cos(th),.0],
					                    [.0,.0,.0,1.0]]),
                glfw.KEY_A : np.array([[np.cos(-th),.0,np.sin(-th),.0],
                                       [.0,1.0,.0,.0],
                                       [-np.sin(-th),.0,np.cos(-th),0],
					                    [.0,.0,.0,1.0]]),
                glfw.KEY_D : np.array([[np.cos(th),.0,np.sin(th),.0],
                                       [.0,1.0,.0,.0],
                                       [-np.sin(th),.0,np.cos(th),.0],
				                        [.0,.0,.0,1.0]])
             
              }
def render(M, camAng):
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    # use orthogonal projection (we'll see details later)
    glOrtho(-1,1, -1,1, -1,1)
    # rotate "camera" position to see this 3D space better (we'll see details later)
    gluLookAt(.1*np.sin(camAng),.1, .1*np.cos(camAng), 0,0,0, 0,1,0)
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex3fv((M @ np.array([.0,.5,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.0,.0,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.5,.0,0.,1.]))[:-1])
    glEnd()
def key_callback(window, key, scancode, action, mods):
    global gCamAng, gComposedM
    if action==glfw.PRESS or action==glfw.REPEAT:
        # keys for cam rotation
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)

        # keys for global coorinate translation
        elif (key==glfw.KEY_Q) or (key == glfw.KEY_E):
            gComposedM =  key_matrix[key] @ gComposedM
    
        # keys for local coordinate translation and rotation
        else:
            gComposedM =  gComposedM @ key_matrix[key] 

def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2016025687",None,None)
   
    if not window:
        glfw.terminate()
        return
       
    glfw.make_context_current(window)
    glfw.set_key_callback(window,key_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):       
        glfw.poll_events()
        render(gComposedM, gCamAng)
        glfw.swap_buffers(window)

    glfw.terminate()
        
if __name__ == "__main__":
            main()

