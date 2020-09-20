import glfw 
from OpenGL.GL import*
from OpenGL.GLU import *
import numpy as np
import ctypes

#file name
gPath = ["BodyMesh.obj", "sphere-tri.obj" ,"cube-tri.obj"] 
OnlyVertex =[ np.array([]),np.array([]),np.array([])]
OnlyIndex = [np.array([]),np.array([]), np.array([])]
OnlyNormal =[ np.array([]), np.array([]), np.array([])]
gPosition = [np.array([0,0,0]),np.array([3,0,3]),np.array([-3,0,-3])]

bezier = np.array([[-1.,3.,-3.,1.],
                   [3.,-6, 3., 0.],
                   [-3., 3.,0.,0.],
                   [1.,0.,0.,0.]])
gCurvePoint =[np.array([5.,0.,5.]),np.array([0.,0.,0.]),np.array([2.,0.,-2.]),np.array([5.,0.,-5.])]
gDegree = [0,0,0]
gReflect = -1
gM = np.identity(4)
gView = 1
gScale = 1
gCurveEnd = 1
Count = 0.

    

def render():
    global gCurvePoint , Count, gCurveEnd
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_RESCALE_NORMAL)
   
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(90,1,1,100)

    # Quater View
    if(gView == 1) :
        gluLookAt(gPosition[0][0]+3,gPosition[0][1]+8,gPosition[0][2]+3,gPosition[0][0],gPosition[0][1],gPosition[0][2],0,1,0)

    # First-Person View
    else: 

        th = np.radians(gDegree[0])
        look = np.array([[np.cos(th),0, np.sin(th)],
                         [0,1,0],
                         [-np.sin(th),0,np.cos(th)]])@ np.array([0,0,gReflect*-1])
        x= gPosition[0][0]
        y= gPosition[0][1]
        z= gPosition[0][2]
        gluLookAt(x,(y+2)*gScale,z,x+look[0],(y+look[1]+2)*gScale,z+look[2],0,1,0)

    glMatrixMode(GL_MODELVIEW)


    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_RESCALE_NORMAL)


     # draw coordinate: x in red, y in green, z in blue

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.) 
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

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


    #Light Settings
    glPushMatrix()
    lightPos = (10,10,10,1)
    glLightfv(GL_LIGHT0, GL_POSITION,lightPos)
    glPopMatrix()
    lightColor = (1.,.0,.0,1.0)
    ambientLightColor = (.1,0.,0.,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
     
    glPushMatrix()
    lightPos = (-10, -10,-10,1)
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
    #Rotating Light
    t = glfw.get_time()
    lightPos = (10*np.sin(t),10,10*np.cos(t),1.)
    glLightfv(GL_LIGHT3, GL_POSITION,lightPos)
    glPopMatrix()
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (0.1,0.1,0.1,1.)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT3, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor)
    
       
      

    #draw objectes

    #main obejct
    glPushMatrix()
    glTranslatef(gPosition[0][0],gPosition[0][1],gPosition[0][2])
    glRotatef(gDegree[0],0,1,0)
    glPushMatrix()
    glMultMatrixf(gM.T)

    #main object color
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.) 
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    draw_glDrawElement(OnlyVertex[0], OnlyIndex[0],OnlyNormal[0])

    glPopMatrix()

    #cube object
    glPushMatrix()

    glTranslatef(gPosition[2][0],gPosition[2][1],gPosition[2][2])

    time = glfw.get_time()
    glRotatef(10*time,0,1,0) 

    #cube object color
    objectColor = (0.,1,0.,1.)
    specularObjectColor = (0.,1.,0.,1.) 
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    draw_glDrawElement(OnlyVertex[2], OnlyIndex[2],OnlyNormal[2])

   
    glPopMatrix()

    glPopMatrix()

    #shpere obejct
    glPushMatrix()
    #draw curve
    if gCurveEnd == 1:
        if Count >= 1 : 
            gCurveEnd = 0
        else : 
            Count = Count + 0.01
    elif gCurveEnd == 0 :
        if Count <= 0 :
            gCurveEnd = 1
        else :
            Count = Count - 0.01

    p = np.array([Count*Count*Count,Count*Count,Count,+1] @ bezier @ np.array(gCurvePoint))

    x = gPosition[1][0] + p[0]
    y = gPosition[1][1] + p[1]
    z = gPosition[1][2] + p[2]

    #check_collision
    curve_point = np.array([x,y,z])

    #collision with main object
    tmp = curve_point - gPosition[0]
    distance = np.sqrt(np.dot(tmp,tmp))
    if distance <= 1 :
        gPosition[1] = gPosition[1] + 3* tmp
#   print("collision\n")

    th = np.radians(gDegree[0])
    R = np.array([[np.cos(th),0,np.sin(th)],
                      [0,1,0],
                      [-np.sin(th),0,np.cos(th)]])
 

    #collision with cube object
    tmp = curve_point - (R@ gPosition[2]+gPosition[0])
    distance = np.sqrt(np.dot(tmp,tmp))
    if distance <= 1.5: 
        gPosition[1] = gPosition[1] + 3* tmp
#       print("collision2\n")
    


    glTranslatef(x,y,z)

    #set shpere obejct color
    objectColor = (0,0.,1.,1.)
    specularObjectColor = (0,0,1.,1.) 
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    draw_glDrawElement(OnlyVertex[1], OnlyIndex[1],OnlyNormal[1])
    glPopMatrix()


    glDisable(GL_LIGHT3)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)



   
def load_obj(path):
    
    Varr = []
    VNarr = []
    Iarr = []
    Normal = []
    Niarr = []
 
    VertexArray = np.array([]) 
    OnlyVertex = np.array([])
    OnlyIndex = np.array([])
    OnlyNormal = np.array([])
    fin = open(path,'rt')
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
            Varr.append((float(line_info[1]), float(line_info[2]),float(line_info[3])))
            VNarr.append((0,0,0))
        #parsing vertex normal 
        elif line_info[0] == "vn": 
            Normal.append((float(line_info[1]), float(line_info[2]),float(line_info[3])))

        #parsing face
        elif line_info[0] == "f":
            tmp_list1 = []#tmp list for storing v information
            tmp_list2 = []#tmp list for storing vn information
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

                i1,i2,i3 = tuple(tmp_list1)

                v1 = np.array(Varr[i1])
                v2 = np.array(Varr[i2])
                v3 = np.array(Varr[i3])

                t_norm = np.cross((v2-v1),(v3-v1))
                t_size = np.sqrt(np.dot(t_norm,t_norm))
                if t_size != 0 : 
                     t_norm = t_norm/t_size
                
                n1 = np.array(VNarr[i1]) + t_norm
                n2 = np.array(VNarr[i2]) + t_norm
                n3 = np.array(VNarr[i3]) + t_norm
                VNarr[i1] = (n1[0],n1[1],n1[2])
                VNarr[i2] =  (n2[0],n2[1],n2[2])
                VNarr[i3] = (n3[0],n3[1],n3[2])

                Iarr.append(tuple(tmp_list1))
                if len(tmp_list2) > 0 :
                    Niarr.append(tuple(tmp_list2))

            #for the face which have more than 3 vertice
            else : 
                
               
                #when theie is normal index in file 
                if len(tmp_list2) > 0 :
                    for i in range(len(tmp_list2)-1):
                        Niarr.append((tmp_list2[0],tmp_list2[i],tmp_list2[i+1]))

               #divide face into triangles 

                for i in range(len(tmp_list1)-1):

                    #get index information
                    i1 = tmp_list1[0]
                    i2 = tmp_list1[i]
                    i3 = tmp_list1[i+1]

                    #add face index
                    Iarr.append((i1,i2,i3))

                    v1 = np.array(Varr[i1])
                    v2 = np.array(Varr[i2])
                    v3 = np.array(Varr[i3])

                    #caculate normal vector
                    t_norm = np.cross((v2-v1),(v3-v1))
                    t_size = np.sqrt(np.dot(t_norm,t_norm))
                    if t_size != 0 :
                        t_norm = t_norm/t_size

                    # make sum list of normal vector 
                    n1 = np.array(VNarr[i1]) + t_norm
                    n2 = np.array(VNarr[i2]) + t_norm
                    n3 = np.array(VNarr[i3]) + t_norm
                    VNarr[i1] = (n1[0],n1[1],n1[2])
                    VNarr[i2] =  (n2[0],n2[1],n2[2])
                    VNarr[i3] = (n3[0],n3[1],n3[2])

    #caculate average of normal verctor 
    for i in range(len(VNarr)):
        normal = VNarr[i]
        size = np.sqrt(np.dot(normal,normal))
        if size != 0 :
            normal = normal/size
        VNarr[i] = normal
   

    fin.close()
    OnlyVertex, OnlyIndex, OnlyNormal = createVertex(Varr,Iarr,VNarr)
    return OnlyVertex, OnlyIndex, OnlyNormal    



#make smooth sading ver array
def createVertex(Varr,Iarr,VNarr):
    varr = np.array(Varr,'float32')
    iarr = np.array(Iarr)
    narr = np.array(VNarr,'float32')
    return varr, iarr, narr

#smooth shading ver
def draw_glDrawElement(OnlyVertex,OnlyIndex,OnlyNormal):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    varr = OnlyVertex
    iarr = OnlyIndex
    narr = OnlyNormal
    glNormalPointer(GL_FLOAT, 3*narr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3* varr.itemsize,varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT,iarr)



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

def init_obj(path) :
    global OnlyVertex, OnlyIndex,OnlyNormal
    for i in range(3):
        vertex,index,normal = load_obj(path[i])
        OnlyVertex[i] = vertex
        OnlyIndex[i] = index
        OnlyNormal[i] =normal


def key_callback(window, key, scancode, action, mods):
    global gDegree, gPosition, gReflect , gM, gView , gScale
    if action == glfw.PRESS or action == glfw.REPEAT:
        th = np.radians(gDegree[0])
        M = np.array([[np.cos(th),0,np.sin(th)],
                      [0,1,0],
                      [-np.sin(th),0,np.cos(th)]])
        # go -X 
        if key == glfw.KEY_A:
            gPosition[0] = gPosition[0] + M @ np.array([-0.5,0,0])
        # go +Z
        elif key == glfw.KEY_S:
            gPosition[0] = gPosition[0] + M @ np.array([0,0,0.5*gReflect])
        # go +X
        elif key == glfw.KEY_D:
            gPosition[0] = gPosition[0] + M @ np.array([0.5,0,0])
        # go -Z
        elif key == glfw.KEY_W:
            gPosition[0] = gPosition[0] + M @ np.array([0,0,-0.5*gReflect])
        # rotation 1
        elif key == glfw.KEY_Q:
            gDegree[0] = gDegree[0] + 10
        # rotation 2
        elif key == glfw.KEY_E:
            gDegree[0] = gDegree[0] - 10
        # reflect xy plane     
        elif key ==glfw.KEY_Z:
            gReflect = gReflect * -1
            gM =  np.array([[1.,.0,.0,.0],
                            [.0,1.,.0,.0],
                            [.0,.0,-1.,.0],
                            [.0,.0,.0,1.]]) @ gM 
       # scale x 1.2
        elif key == glfw.KEY_X:
            gM =  np.array([[1.2,.0,.0,.0],
                            [.0,1.2,.0,.0],
                            [.0,.0,1.2,.0],
                            [.0,.0,.0,1.]]) @ gM 
            gScale = gScale * 1.2
        # scale x 0,8
        elif key == glfw.KEY_C:
            gM =  np.array([[0.8,.0,.0,.0],
                            [.0,0.8,.0,.0],
                            [.0,.0,0.8,.0],
                            [.0,.0,.0,1.]]) @ gM 
            gScale = gScale * 0.8
        # shear 1
        elif key == glfw.KEY_1:
            gM =  np.array([[1,0.2,.0,.0],
                            [.0,1,.0,.0],
                            [.0,.0,1,.0],
                            [.0,.0,.0,1]]) @ gM 

        # shear 2
        elif key == glfw.KEY_2:
            gM =  np.array([[1.,-0.2,.0,.0],
                            [.0,1.,.0,.0],
                            [.0,.0,1.,.0],
                            [.0,.0,.0,1.]]) @ gM 
 
        # change view
        elif key == glfw.KEY_V:
            gView = gView * -1


      
     
def main():
    global OnlyVertex , OnlyIndex, OnlyNormal

    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,"2016025687",None,None)
   
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window,key_callback)
    glfw.swap_interval(1)
    init_obj(gPath)

    while not glfw.window_should_close(window):       
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
 
if __name__ == "__main__":
    main()
