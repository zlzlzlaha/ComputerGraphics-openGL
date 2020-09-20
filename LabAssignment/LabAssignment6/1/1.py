import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# draw a cube of side 1, centered at the origin
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)

    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)

    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)

    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)

    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

def drawFrame():
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
                
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    #same with glOrtho(-5,5, -5,5, -8,8)
    myOrtho(-5,5, -5,5, -8,8)
    #same with gluLookAt(5,3,5, 1,1,-1,0,1,0)
    myLookAt(np.array([5,3,5]), np.array([1,1,-1]), np.array([0,1,0]))
    
    drawFrame()

    glColor3ub(255, 255, 255)
    drawCubeArray()

def myOrtho(left, right, bottom, top, near, far):
    M_orth = np.array([[2/(right-left),0.,0.,-((right+left)/(right-left))],
                       [0., 2/(top-bottom),0., -((top+bottom)/(top-bottom))],
                       [0., 0., -2/(far-near), -(far+near)/(far-near)],
                       [0,0,0,1]])
    glMultMatrixf(M_orth.T)

def myLookAt(eye, at, up):
   M_camera = np.identity(4)
   w = eye-at
   w = w/np.sqrt(np.dot(w,w))
   u = np.cross(up,w)
   u = u/np.sqrt(np.dot(u,u))
   v = np.cross(w,u)
   M_camera[0,:3] = u
   M_camera[1,:3] = v
   M_camera[2,:3] = w
   M_camera[0][3] = -u@eye
   M_camera[1][3] = -v@eye
   M_camera[2][3] = -w@eye
   glMultMatrixf(M_camera.T)  

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025687",None,None);

    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window) 

    while not glfw.window_should_close(window) :  
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()  


if __name__ == "__main__":
    main()

