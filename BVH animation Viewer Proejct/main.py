import glfw
from OpenGL.GL import*
from OpenGL.GLU import *
import numpy as np
import ctypes
import os
inputKey = -1
inputButton = -1
gCamAng = 0
gYOff = -10
gM = np.identity(4)
x  = 0 
y  = 0
stack = []
frame = 0
motion = []
part = []
cube_name = []
frame_time = .0
frame_index =0
ct = 0
gKeyToggle = 0
gCube =0 
gVertexArraySeparate = np.array([])



#draw line Tpos    
def draw_skeleton() : 
    index = 0
    motion_index = 0
    glColor3ub(255, 0, 0)

    for st in stack : 
        if st == "{" :
            glPushMatrix() 
            offset = part[index][1]

            # when joint is not root
            if part[index][0] != "ROOT":
                start = np.array([0.,0.,0.,])
                end = start + np.array([offset[0],offset[1],offset[2]]) 
                #draw body line
                glBegin(GL_LINES) 
                glVertex3fv(start)
                glVertex3fv(end)
                glEnd()

            # translation about offset        
            glTranslatef(offset[0],offset[1],offset[2])
            index = index +1

        elif st == "}" :
            glPopMatrix()

#draw cube Tpos    
def draw_skeleton2() : 
    index = 0
    motion_index = 0
    glColor3ub(255, 0, 0)

    for st in stack : 
        if st == "{" :
            glPushMatrix() 
            offset = part[index][1]

            # when joint is not root
            if part[index][0] != "ROOT":
                start = np.array([0.,0.,0.,])
                end = start + np.array([offset[0],offset[1],offset[2]])
                length = 0.9 * np.sqrt(np.dot(end,end))
                
           
                abs_offset = np.array([np.abs(offset[0]), np.abs(offset[1]) , np.abs(offset[2])])
                max_num =  abs_offset[0]

                for num in abs_offset :
                    if max_num < num :
                        max_num = num
                #draw cube       
                glPushMatrix()
                if abs_offset[0] == max_num :
                    glScalef(length , 0.05,0.05)
                    if offset[0] >= 0 :
                        glTranslatef(0.5,0,0)
                    else :
                        glTranslatef(-0.5,0,0)
                elif abs_offset[1] == max_num :
                    glScalef(0.05,length ,0.05)
                    if offset[1] >= 0 :
                        glTranslatef(0,0.5,0)
                    else :
                        glTranslatef(0,-0.5,0)

                elif abs_offset[2] == max_num : 
                     glScalef(0.05,0.05,length)  
                     if offset[2] >= 0 :
                        glTranslatef(0,0,0.5)
                     else :
                        glTranslatef(0,0,-0.5)

                cname = cube_name[index]
                if cname != "RIGHTUPLEG" and cname != "LEFTUPLEG" : 
                    drawCube_glDrawArray() 
                glPopMatrix()

            # translation about offset
            glTranslatef(offset[0],offset[1],offset[2])
            index = index +1

        elif st == "}" :
            glPopMatrix()

   
# draw line body motion
def draw_animation() : 
    index = 0
    motion_index = 0
    glColor3ub(255, 0, 0)

    for st in stack : 
        if st == "{" :
            glPushMatrix() 
            offset = part[index][1]

            # when joint is not root
            if part[index][0] != "ROOT":
                start = np.array([0.,0.,0.,])
                end = start + np.array([offset[0],offset[1],offset[2]]) 
                #draw line
                glBegin(GL_LINES) 
                glVertex3fv(start)
                glVertex3fv(end)
                glEnd()

            # translation about offset        
            glTranslatef(offset[0],offset[1],offset[2])
            
            # do motion operation
            if len(part[index]) == 3 :
                for channel in part[index][2] :
                    if (channel == "XROTATION") :
                        degree = motion[frame_index][motion_index]
                        glRotatef(degree,1,0,0)
                    elif (channel == "YROTATION") :
                        degree = motion[frame_index][motion_index] 
                        glRotatef(degree,0,1,0)
                    elif (channel == "ZROTATION") :
                        degree = motion[frame_index][motion_index]
                        glRotatef(degree,0,0,1)
                    elif (channel == "XPOSITION") :
                        pos =motion[frame_index][motion_index]
                        glTranslatef(pos,0.,0.)
                    elif (channel == "YPOSITION") :
                        pos =motion[frame_index][motion_index]
                        glTranslatef(.0,pos,.0)
                    elif (channel == "ZPOSITION") :
                        pos =motion[frame_index][motion_index]
                        glTranslatef(.0,.0,pos)
                    motion_index = motion_index +1
            index = index +1
 
        elif st == "}" :
            glPopMatrix()

#draw cube body motion
def draw_animation2() : 
    index = 0
    motion_index = 0
    glColor3ub(255, 0, 0)

    for st in stack : 
        if st == "{" :
            glPushMatrix() 
            offset = part[index][1]

            # when joint is not root
            if part[index][0] != "ROOT":
                start = np.array([0.,0.,0.,])
                end = start + np.array([offset[0],offset[1],offset[2]])
                
                length = 0.9 * np.sqrt(np.dot(end,end))
             
                abs_offset = np.array([np.abs(offset[0]), np.abs(offset[1]) , np.abs(offset[2])])
                max_num =  abs_offset[0]

                for num in abs_offset :
                    if max_num < num :
                        max_num = num


                #draw_cube 
                glPushMatrix()
                if abs_offset[0] == max_num :    
                    glScalef(length, 0.05,0.05)
                    if offset[0] >= 0 :
                        glTranslatef(0.5,0,0)
                    else :
                        glTranslatef(-0.5,0,0)
                elif abs_offset[1] == max_num :
                    glScalef(0.05,length,0.05)
                    if offset[1] >= 0 :
                        glTranslatef(0,0.5,0)
                    else :
                        glTranslatef(0,-0.5,0)

                elif abs_offset[2] == max_num :     
                     glScalef(0.05,0.05,length)  
                     if offset[2] >= 0 :
                        glTranslatef(0,0,0.5)
                     else :
                        glTranslatef(0,0,-0.5)
                  
                cname = cube_name[index]
                if cname != "RIGHTUPLEG" and cname != "LEFTUPLEG" : 
                    drawCube_glDrawArray()
                glPopMatrix()
            # translation about offset        
            glTranslatef(offset[0],offset[1],offset[2])

            # do motion operation
            if len(part[index]) == 3 :
                for channel in part[index][2] :
                    if (channel == "XROTATION") :
                        degree = motion[frame_index][motion_index]
                        glRotatef(degree,1,0,0)
                    elif (channel == "YROTATION") :
                        degree = motion[frame_index][motion_index] 
                        glRotatef(degree,0,1,0)
                    elif (channel == "ZROTATION") :
                        degree = motion[frame_index][motion_index]
                        glRotatef(degree,0,0,1)
                    elif (channel == "XPOSITION") :
                        pos =motion[frame_index][motion_index]
                        glTranslatef(pos,0.,0.)
                    elif (channel == "YPOSITION") :
                        pos =motion[frame_index][motion_index]
                        glTranslatef(.0,pos,.0)
                    elif (channel == "ZPOSITION") :
                        pos =motion[frame_index][motion_index]
                        glTranslatef(.0,.0,pos)
                    motion_index = motion_index +1
            index = index +1
 
        elif st == "}" :
            glPopMatrix()

def createVertexArraySeparate():
    varr = np.array([
    (0,0,1), # v0 normal
    ( -0.5 , 0.5 , 0.5 ), # v0 position
    (0,0,1), # v2 normal
    ( 0.5 , -0.5 , 0.5 ), # v2 position
    (0,0,1), # v1 normal
    ( 0.5 , 0.5 , 0.5 ), # v1 position
    (0,0,1), # v0 normal
    ( -0.5 , 0.5 , 0.5 ), # v0 position
    (0,0,1), # v3 normal
    ( -0.5 , -0.5 , 0.5 ), # v3 position
    (0,0,1), # v2 normal
    ( 0.5 , -0.5 , 0.5 ), # v2 position
    (0,0,-1),
    ( -0.5 , 0.5 , -0.5 ), # v4
    (0,0,-1),
    ( 0.5 , 0.5 , -0.5 ), # v5
    (0,0,-1),
    ( 0.5 , -0.5 , -0.5 ), # v6
    (0,0,-1),
    ( -0.5 , 0.5 , -0.5 ), # v4
    (0,0,-1),
    ( 0.5 , -0.5 , -0.5 ), # v6
    (0,0,-1),
    ( -0.5 , -0.5 , -0.5 ), # v7
    (0,1,0),
    ( -0.5 , 0.5 , 0.5 ), # v0
    (0,1,0),
    ( 0.5 , 0.5 , 0.5 ), # v1
    (0,1,0),
    ( 0.5 , 0.5 , -0.5 ), # v5
    (0,1,0),
    ( -0.5 ,0.5 , 0.5 ), # v0
    (0,1,0),
    ( 0.5 , 0.5 , -0.5 ), # v5
    (0,1,0),
    ( -0.5 , 0.5 , -0.5 ), # v4
    (0,-1,0),
    ( -0.5 , -0.5 , 0.5 ), # v3
    (0,-1,0),
    ( 0.5 , -0.5 , -0.5 ), # v6
    (0,-1,0),
    ( 0.5 , -0.5 , 0.5 ), # v2
    (0,-1,0),
    ( -0.5 , -0.5 , 0.5 ), # v3
    (0,-1,0),
    ( -0.5 , -0.5 , -0.5 ), # v7
    (0,-1,0),
    ( 0.5 , -0.5 , -0.5 ), # v6
    (1,0,0),
    ( 0.5 , 0.5 , 0.5 ), # v1
    (1,0,0),
    ( 0.5 , -0.5 , 0.5 ), # v2
    (1,0,0),
    ( 0.5 , -0.5 , -0.5 ), # v6
    (1,0,0),
    ( 0.5 , 0.5 , 0.5 ), # v1
    (1,0,0),
    ( 0.5 , -0.5 , -0.5 ), # v6
    (1,0,0),
    ( 0.5 , 0.5 , -0.5), # v5
    (-1,0,0),
    ( -0.5 , 0.5 , 0.5 ), # v0
    (-1,0,0),
    ( -0.5 , -0.5 , -0.5 ), # v7
    (-1,0,0),
    ( -0.5 , -0.5 , 0.5 ), # v3
    (-1,0,0),
    ( -0.5 , 0.5 , 0.5 ), # v0
    (-1,0,0),
    ( -0.5 , 0.5 , -0.5 ), # v4
    (-1,0,0),
    ( -0.5 , -0.5 , -0.5 ), # v7
    ], 'float32')
    return varr


def drawCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
    ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))
 
def render():
    global gCamAng, gYOff,frame_index,gKeyToggle, gCube
  
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(90,1,1,300)
   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
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
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd() 

    # Draw line animation
    if gCube == 0:
      
        if gKeyToggle ==1:
            if frame_index+1 >= frame: 
                frame_index = 0
            else :
                frame_index = frame_index + 1
            draw_animation()
   
        #draw Tpos
        elif gKeyToggle == 0:
            frame_index = 0
            draw_skeleton()

    # Draw cube animaton
    elif gCube == 1:
          
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
   
        glEnable(GL_RESCALE_NORMAL)
   
        #set light pos
        glPushMatrix()
        lightPos = (0,10,0,0)
        glLightfv(GL_LIGHT0, GL_POSITION,lightPos)
        glPopMatrix()
     
        #set light color
        lightColor = (1.,1,1,1.0)
        ambientLightColor = (.1,.1,.1,1.)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

        #draw cube animation
        if gKeyToggle ==1:
            if frame_index+1 >= frame: 
                frame_index = 0 
            else :
                frame_index = frame_index+1
            draw_animation2()
        #draw Tpos
        elif gKeyToggle == 0:
            frame_index = 0
            draw_skeleton2()

        # material reflectance for each color channel
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.) 
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
  
   

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
def key_callback(window, key, scancode, action, mode) :
    global gKeyToggle
    if action == glfw.PRESS :
        if key== glfw.KEY_SPACE:
            if gKeyToggle == 0:
                gKeyToggle =1
            else:
                gKeyToggle = 0
            
     
def button_callback(window, button, action, mod) :
    global inputButton
    if action == glfw.PRESS:
        if button ==glfw.MOUSE_BUTTON_LEFT :
            inputButton = glfw.MOUSE_BUTTON_LEFT
        elif button == glfw.MOUSE_BUTTON_RIGHT :
            inputButton = glfw.MOUSE_BUTTON_RIGHT
    elif action == glfw.RELEASE :
       inputButton = -1

def drop_callback(window, path):
   
    global stack, part, frame, motion, frame_time,start,gKeyToggle ,gCube, cube_name, frame_index
    start = 1
  
    part_name = []
    part = []
    stack = []
    cube_name = []
    part_count = 0
    index = -1
    frame = 0
    motion = []
    isMotion = 0
    frame_time = 0
    motion_index =0 
    gKeyToggle = 0
    gCube = 0
    frame_index =0
    fin = open(path[0],'rt')
    file_name = os.path.basename(path[0])

    # when cube animiation file
    if(file_name == "sample-walk.bvh"):
        gCube = 1

    while True:
        line = fin.readline()
        if not line :
            break;
        lineinfo =line.split()
        if(lineinfo[0] == "ROOT" or lineinfo[0] == "JOINT" or lineinfo[0] == "End"):
            index = index +1    
            part.append([]) #make new part
            part[index].append(lineinfo[0].upper()) #add kind of part
            cube_name.append(lineinfo[1].upper())

            #except end join in name and the number of joint
            if lineinfo[0] != "End" :
                part_name.append(lineinfo[1])
                part_count = part_count+1

        elif(lineinfo[0] == "{") :
            stack.append(lineinfo[0])

        elif(lineinfo[0] == "}") :
            stack.append(lineinfo[0])
        
        elif(lineinfo[0] == "OFFSET") :
            part[index].append([float(lineinfo[1]),float(lineinfo[2]),float(lineinfo[3])]) #save offset

        elif(lineinfo[0] == "CHANNELS"):
            
            #add CHANNELES INFORMATION
            tmp_channel = []
            for i in range(2,len(lineinfo)):
                tmp_channel.append(lineinfo[i].upper())
            
            part[index].append(tmp_channel.copy()) 

        elif(lineinfo[0] == "MOTION"): 
            isMotion =1

        #add number of frames
        elif(lineinfo[0] == "Frames:"): 
            frame = int(lineinfo[1])

        #add frame_time
        elif(lineinfo[0] == "Frame" and lineinfo[1] == "Time:"):
            frame_time = float(lineinfo[2])

        #when space line
        elif(len(lineinfo) == 0):
            pass

        #parsing motion information
        else :
            if(isMotion == 1):
              #make motion inforamtions per frame
              motion. append([])
              tmp_motion = []
              for info in lineinfo:
                 motion[motion_index].append(float(info))
              motion_index = motion_index +1
                                
        
   #print(stack,"\n")
   #print(part,"\n")
   #print(part_name,"\n")
   #print(motion, "\n")
    print("Filename :",path[0], "\n")
    print("Number of fames : ", frame,"\n")
    print("FPS : ",1/frame_time,"\n")
    print("Number of Joints : ",part_count,"\n")
    print("List of all joint names",part_name,"\n")
    fin.close()

    
def scroll_callback(window, xoffset, yoffset):
    global gYOff
    gYOff = gYOff+ yoffset

#draw xz plane line anslatef(pos,0.,0.)
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

    global gVertexArraySeparate
    if not glfw.init():
        return
    window = glfw.create_window(800,800,"2016025687",None,None)
   
    if not window:
        glfw.terminate()
        return

    glfw.set_drop_callback(window, drop_callback)
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_mouse_button_callback(window,button_callback)
    glfw.set_key_callback(window,key_callback)
    glfw.swap_interval(1)
    gVertexArraySeparate = createVertexArraySeparate()
    while not glfw.window_should_close(window):       
        glfw.poll_events()       
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
 
if __name__ == "__main__":
    main()
