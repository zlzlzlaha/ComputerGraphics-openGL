import glfw
from OpenGL.GL import*
from OpenGL.GLU import *
import numpy as np

inputKey = -1
inputButton = -1
gCamAng = 0
gYOff = -10
gM = np.identity(4)
x  = 0 
y  = 0
  

def render():
    global gCamAng, gYOff
  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity() 
    gluPerspective(90,1,1,100)
  
    # set zoom limit
    if gYOff  > -10 :
        gYOff = -10
    #move obeject about camera

    #zoom    
    glTranslatef(.0,.0, 0.1 * gYOff)
    #elevation
    glRotatef(gCamAng,1,0,0)
    #rotate, panning
    glMultMatrixf(gM.T)

    # draw coordinate: x in red, y in green, z in blue
    draw_line()
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
    
    t= glfw.get_time()
    #push core body
    glPushMatrix()
    glRotatef((0.5*t)*(180/np.pi),0,1,0)
    glTranslatef(3,2,0)
    #draw core body
    glPushMatrix()
    glScalef(0.15,0.5,0.15)
    glColor3ub(0,0,255)
    drawCube()
    glPopMatrix()
    #push head
    glPushMatrix()
    glTranslatef(0,0.4,0)
    glRotatef(t*(180/np.pi),0,1,0)
    #draw head
    glPushMatrix()
    glScalef(0.15,0.15,0.15)
    glColor3ub(255,0,0)
    drawCube()
    glPopMatrix()
    #pop head
    glPopMatrix()

    #push high arm1
    glPushMatrix()
    glTranslatef(-0.6,0,0)
    glRotatef(np.sin(t)*45-15,1,0,0)
    #draw high arm1
    glPushMatrix()
    glScalef(0.1,0.25,0.1)
    glColor3ub(255,0,0)
    drawCube()
    glPopMatrix()
    #push low arm1
    glPushMatrix()
    glTranslatef(0,-0.6,0)  
    glRotatef(-1*np.sin(t)*60+30,1,0,0)
    #draw low arm1 
    glPushMatrix()
    glScalef(0.1,0.25,0.1)
    glColor3ub(0,255,0)
    drawCube()
    glPopMatrix()
    #pop low arm1
    glPopMatrix()
    #pop high arm1
    glPopMatrix()
    #push high arm2
    glPushMatrix()
    glTranslatef(0.6,0,0)
    glRotatef(-np.sin(t)*45+15,1,0,0)
    #draw high arm 2
    glPushMatrix()
    glScalef(0.1,0.25,0.1)
    glColor3ub(255,0,0)
    drawCube()
    glPopMatrix()
    #push low arm2
    glPushMatrix()
    glTranslatef(0,-0.6,0)
    glRotatef(-1*np.sin(t)*60+30,1,0,0)
    #draw low arm2  
    glPushMatrix()
    glScalef(0.1,0.25,0.1)
    glColor3ub(0,255,0)
    drawCube()
    glPopMatrix()
    #pop low arm2
    glPopMatrix()

    #pop high arm2
    glPopMatrix()

###########
    #push high leg1
    glPushMatrix()
    glTranslatef(-0.3,-1,0)
    glRotatef(-np.sin(t)*45-15,1,0,0)
    #draw high leg1
    glPushMatrix()
    glScalef(0.1,0.35,0.1)
    glColor3ub(255,0,0)
    drawCube()
    glPopMatrix()
    #push low leg1
    glPushMatrix()
    glTranslatef(0,-0.75,0)  
    glRotatef(1*np.sin(t)*60-30,1,0,0)
    #draw low leg1  
    glPushMatrix()
    glScalef(0.1,0.35,0.1)
    glColor3ub(0,255,0)
    drawCube()
    glPopMatrix()
    #pop low leg1
    glPopMatrix()
    #pop high leg1
    glPopMatrix()
    #push high leg2
    glPushMatrix()
    glTranslatef(0.3,-1,0)
    glRotatef(np.sin(t)*45+15,1,0,0)
    #draw high leg2
    glPushMatrix()
    glScalef(0.1,0.35,0.1)
    glColor3ub(255,0,0)
    drawCube()
    glPopMatrix()
    #push low leg2
    glPushMatrix()
    glTranslatef(0,-0.75,0)
    glRotatef(1*np.sin(t)*60-30,1,0,0)
    #draw low leg2  
    glPushMatrix()
    glScalef(0.1,0.35,0.1)
    glColor3ub(0,255,0)
    drawCube()
    glPopMatrix()
    #pop low leg2
    glPopMatrix()

    #pop high leg2
    glPopMatrix()

    #pop core body
    glPopMatrix()



def cursor_callback(window, xpos, ypos) :
    global x,y,gCamAng,gM

    #orbit  
    if inputButton == glfw.MOUSE_BUTTON_LEFT:
       CamAng = -0.001*(x-xpos)
       R = np.array([[np.cos(CamAng),.0,np.sin(CamAng),.0],
                       [.0,1,.0,.0],
                       [-np.sin(CamAng),.0,np.cos(CamAng),.0],
                       [.0,.0,.0,1]])
       #accumulate rotate in gM
       gM = R @ gM

       #save elevation degree
       gCamAng = gCamAng - 0.1*(y-ypos) 
       x = xpos
       y = ypos

    # not simultaneously  azimuth and elevation
#    if inputButton == glfw.MOUSE_BUTTON_LEFT:
        #azimuth
#       if np.abs(x-xpos)  > np.abs(y-ypos) : 
#           CamAng = -0.001*(x-xpos)
#           R = np.array([[np.cos(CamAng),.0,np.sin(CamAng),.0],
#                         [.0,1,.0,.0],
#                         [-np.sin(CamAng),.0,np.cos(CamAng),.0],
#                         [.0,.0,.0,1]]) 
#           gM = R @ gM
#           x = xpos
#           y = ypos
  
#       #save elevation degree
#       elif np.abs(x-xpos) < np.abs(y-ypos)  : 
#           gCamAng = gCamAng -0.001*(y-ypos)
          
    #panning         
    elif inputButton == glfw.MOUSE_BUTTON_RIGHT:
        MoveU =  0.005* (x-xpos)
        MoveV =  0.005*(y-ypos) 
        T = np.array([ [1,.0,.0,-1*MoveU],
                       [.0,1,.0,MoveV],
                       [.0,.0,1,.0],
                       [.0,.0,.0,1]])
        #accmulate panning in gM matrix
        gM =  T @ gM
        x = xpos
        y = ypos
  
    #when not click mouse button, keep xpos, ypos  
    else :
        y = ypos
        x = xpos    

def button_callback(window, button, action, mod) :
    global inputButton
    if action == glfw.PRESS:
        if button ==glfw.MOUSE_BUTTON_LEFT :
            inputButton = glfw.MOUSE_BUTTON_LEFT
        elif button == glfw.MOUSE_BUTTON_RIGHT :
            inputButton = glfw.MOUSE_BUTTON_RIGHT
    elif action == glfw.RELEASE :
       inputButton = -1
def scroll_callback(window, xoffset, yoffset):
    global gYOff
    gYOff = gYOff+ yoffset

#draw xz plane line 
def draw_line():
    glColor3ub(255, 255, 255)
    glBegin(GL_LINES)
    for i in range (31) :
        glVertex3fv(np.array([-i,0,-30]))
        glVertex3fv(np.array([-i,0,30]))
        glVertex3fv(np.array([i,0,-30]))
        glVertex3fv(np.array([i,0,30]))

        glVertex3fv(np.array([-30,0,-i]))
        glVertex3fv(np.array([30,0,-i]))
        glVertex3fv(np.array([-30,0,i]))  
        glVertex3fv(np.array([30,0,i]))
          
          
    glEnd()
def main():
    if not glfw.init():
        return

    window = glfw.create_window(1000,1000,"2016025687",None,None)
   
    if not window:
        glfw.terminate()
        return
       
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_mouse_button_callback(window,button_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):       
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
 
def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 0.0,-1.0)
    glVertex3f(-1.0, 0.0,-1.0)
    glVertex3f(-1.0, 0.0, 1.0)
    glVertex3f( 1.0, 0.0, 1.0)
    glVertex3f( 1.0,-2.0, 1.0)
    glVertex3f(-1.0,-2.0, 1.0)
    glVertex3f(-1.0,-2.0,-1.0)
    glVertex3f( 1.0,-2.0,-1.0)
    glVertex3f( 1.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.0, 1.0)
    glVertex3f(-1.0,-2.0, 1.0)
    glVertex3f( 1.0,-2.0, 1.0)
    glVertex3f( 1.0,-2.0,-1.0)
    glVertex3f(-1.0,-2.0,-1.0)
    glVertex3f(-1.0, 0.0,-1.0)
    glVertex3f( 1.0, 0.0,-1.0)
    glVertex3f(-1.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.0,-1.0)
    glVertex3f(-1.0,-2.0,-1.0)
    glVertex3f(-1.0,-2.0, 1.0)
    glVertex3f( 1.0, 0.0,-1.0)
    glVertex3f( 1.0, 0.0, 1.0)
    glVertex3f( 1.0,-2.0, 1.0)
    glVertex3f( 1.0,-2.0,-1.0)
    glEnd()
# draw a sphere of radius 1, centered at the origin.
# numLats: number of latitude segments
# numLongs: number of longitude segments
def drawSphere(numLats=6, numLongs=18):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
    # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)

        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)

        glEnd()    

if __name__ == "__main__":
            main()

