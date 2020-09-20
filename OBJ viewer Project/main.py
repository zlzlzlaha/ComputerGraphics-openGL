import glfw
from OpenGL.GL import*
from OpenGL.GLU import *
import numpy as np
import ctypes
inputKey = -1
inputButton = -1
gCamAng = 0
gYOff = -10
gM = np.identity(4)
x  = 0 
y  = 0
gVarr = []
gIarr = []
gNormal = []
gNiarr =[]
gVertexArray = np.array([])
gKeyToggle = 0 
gShadingToggle =0
gVNarr = []
gOnlyVertex = np.array([])
gOnlyIndex = np.array([])
gOnlyNormal = np.array([])

def render():
    global gCamAng, gYOff
  

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if gKeyToggle ==1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    elif gKeyToggle ==0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(90,1,1,100)
   
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

    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_RESCALE_NORMAL)
    
    glPushMatrix()
    lightPos = (10,10,10,0)
    glLightfv(GL_LIGHT0, GL_POSITION,lightPos)
    glPopMatrix()

    lightColor = (1.,.0,.0,1.0)
    ambientLightColor = (.1,0.,0.,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    
   
    glPushMatrix()
    lightPos = (-10,-10,-10,0)
    glLightfv(GL_LIGHT1, GL_POSITION,lightPos)
    glPopMatrix()

    lightColor = (0.,1.,0.,1.)
    ambientLightColor = (.0,.1,.0,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    

    glPushMatrix()
    lightPos = (10,-10 ,-10,1.)
    glLightfv(GL_LIGHT2, GL_POSITION,lightPos)
    glPopMatrix()
    lightColor = (0.,0.,1.,1.)
    ambientLightColor = (.0,.0,.1,1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)
    
    glPushMatrix()
    lightPos = (-10,10,10,1.)
    glLightfv(GL_LIGHT3, GL_POSITION,lightPos)
    glPopMatrix()
    lightColor = (.3,.5,.7,1.)
    ambientLightColor = (0.03,0.05,0.07,1.)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, lightColor)
#    glLightfv(GL_LIGHT3, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor)
   
       
    # material reflectance for each color channel
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.) 
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    if gShadingToggle == 0:
        draw_glDrawElements()
    else :
        draw_glDrawElements2()

    glDisable(GL_LIGHT3)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHT1)
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
    global gKeyToggle, gShadingToggle
    if action == glfw.PRESS :
        if key== glfw.KEY_Z:
            if gKeyToggle == 0:
                gKeyToggle =1
            else:
                gKeyToggle = 0
        if key== glfw.KEY_S:
            if gShadingToggle == 0:
                gShadingToggle =1
            else :
                gShadingToggle = 0

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
    global gVarr, gIarr, gNormal, gNiarr, gVertexArray, gVNarr, gOnlyVertex, gOnlyNormal, gOnlyIndex
    
    gVarr = []
    gIarr = []
    gNormal = []
    gNiarr = []
    totalFace = 0 
    face3  = 0#number of face which have 3 vertex
    face4 = 0 #number of face which have 4 vertex
    face5 = 0 #number of face which have more than 4 vertex
    fin = open(path[0],'rt')

    while True:
        line = fin.readline()
        if not line :
            break;
        line_info =line.split()
        #when there is only white space in the file
        if len(line_info) == 0 :
            pass

        #parsing vertex    
        elif line_info[0] == "v":
            gVarr.append((float(line_info[1]), float(line_info[2]),float(line_info[3])))
            gVNarr.append((0,0,0))
        #parsing vertex normal 
        elif line_info[0] == "vn": 
            gNormal.append((float(line_info[1]), float(line_info[2]),float(line_info[3])))

        #parsing face
        elif line_info[0] == "f":
            tmp_list1 = []#tmp list for storing v information
            tmp_list2 = []#tmp list for storing vn information
            totalFace = totalFace +1
            split_number = len(line_info)
            for info in line_info[1:]:
                if "//" in info :
                   tmp = info.split("//")
                   tmp_list1.append(int(tmp[0])-1)
                   tmp_list2.append(int(tmp[1])-1)
                elif "/" in info :
                    tmp = info.split("/")
                    if  len(tmp) == 3 :
                        tmp_list1.append(int(tmp[0])-1)
                        tmp_list2.append(int(tmp[2])-1)
                    else : 
                        tmp_list1.append(int(tmp[0])-1)
                else :
                     tmp_list1.append(int(info)-1)
            # 3 vertices face
            if split_number <= 4:
                face3 = face3 +1

                i1,i2,i3 = tuple(tmp_list1)

                v1 = np.array(gVarr[i1])
                v2 = np.array(gVarr[i2])
                v3 = np.array(gVarr[i3])

                t_norm = np.cross((v2-v1),(v3-v1))
                t_size = np.sqrt(np.dot(t_norm,t_norm))
                if t_size != 0 : 
                     t_norm = t_norm/t_size
                
                n1 = np.array(gVNarr[i1]) + t_norm
                n2 = np.array(gVNarr[i2]) + t_norm
                n3 = np.array(gVNarr[i3]) + t_norm
                gVNarr[i1] = (n1[0],n1[1],n1[2])
                gVNarr[i2] =  (n2[0],n2[1],n2[2])
                gVNarr[i3] = (n3[0],n3[1],n3[2])

                gIarr.append(tuple(tmp_list1))
                if len(tmp_list2) > 0 :
                    gNiarr.append(tuple(tmp_list2))

            #for the face which have more than 3 vertice
            else : 
                
                if split_number == 5 :
                    face4 = face4+1
                else : 
                    face5 = face5+1
                #when theie is normal index in file 
                if len(tmp_list2) > 0 :
                    for i in range(len(tmp_list2)-1):
                        gNiarr.append((tmp_list2[0],tmp_list2[i],tmp_list2[i+1]))

               #divide face into triangles 
                for i in range(len(tmp_list1)-1):

                    #get index information
                    i1 = tmp_list1[0]
                    i2 = tmp_list1[i]
                    i3 = tmp_list1[i+1]

                    #add face index
                    gIarr.append((i1,i2,i3))

                    v1 = np.array(gVarr[i1])
                    v2 = np.array(gVarr[i2])
                    v3 = np.array(gVarr[i3])

                    #caculate normal vector
                    t_norm = np.cross((v2-v1),(v3-v1))
                    t_size = np.sqrt(np.dot(t_norm,t_norm))
                    if t_size != 0 :
                        t_norm = t_norm/t_size

                    # make sum list of normal vector 
                    n1 = np.array(gVNarr[i1]) + t_norm
                    n2 = np.array(gVNarr[i2]) + t_norm
                    n3 = np.array(gVNarr[i3]) + t_norm
                    gVNarr[i1] = (n1[0],n1[1],n1[2])
                    gVNarr[i2] =  (n2[0],n2[1],n2[2])
                    gVNarr[i3] = (n3[0],n3[1],n3[2])

    #caculate average of normal verctor 
    for i in range(len(gVNarr)):
        normal = gVNarr[i]
        size = np.sqrt(np.dot(normal,normal))
        if size != 0 :
            normal = normal/size
        gVNarr[i] = normal
   

    fin.close()
#   print(gVarr)
#   print(gIarr)
#   print(gNormal)
#   print(gNiarr)
    print("File name : ", path[0])
    print("Total number of faces  : ", totalFace)
    print("Number of faces with 3 vertices : ",face3)
    print("Number of faces with 4 vertices : ",face4)
    print("Number of faces with more than 4 vertices : ",face5)
    print("")
    gVertexArray = createVertex()
    gOnlyVertex, gOnlyIndex, gOnlyNormal =createVertex2()
   

def createVertex() :
    tmp = []

    if len(gNiarr) > 0: 
        for i in range(len(gIarr)):
#make form of 'n1' 'v1' 'n2' 'v2' 'n3' 'v3'.......
            v1,v2,v3 = gIarr[i]
            n1,n2,n3 = gNiarr[i]
            tmp.append(gNormal[n1])
            tmp.append(gVarr[v1])
            tmp.append(gNormal[n2])
            tmp.append(gVarr[v2])
            tmp.append(gNormal[n3])
            tmp.append(gVarr[v3])
    else :
#when file dont have information about vn
       for i in range(len(gIarr)):
            v1,v2,v3 = gIarr[i]
            tmp.append(gVarr[v1])
            tmp.append(gVarr[v2])
            tmp.append(gVarr[v3])

    varr = np.array(tmp,'float32')
    return varr

#make smooth sading ver array
def createVertex2():
    varr = np.array(gVarr,'float32')
    iarr = np.array(gIarr)
    narr = np.array(gVNarr,'float32')
    return varr, iarr, narr

#smooth shading ver
def draw_glDrawElements2():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    varr = gOnlyVertex
    iarr = gOnlyIndex
    narr = gOnlyNormal
    glNormalPointer(GL_FLOAT, 3*narr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3* varr.itemsize,varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT,iarr)

#normal vector in file shading ver
def draw_glDrawElements():
    global gVertexArray
    varr = gVertexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    if len(gNiarr) > 0 :
        glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
        glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
        glDrawArrays(GL_TRIANGLES,0,int(varr.size/6))
    #when there is no noraml vector information
    else :
        glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
        glDrawArrays(GL_TRIANGLES,0,int(varr.size/3))

    
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

    glfw.set_drop_callback(window, drop_callback)
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_mouse_button_callback(window,button_callback)
    glfw.set_key_callback(window,key_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):       
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
 
if __name__ == "__main__":
    main()
