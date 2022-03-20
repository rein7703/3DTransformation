from graphics import *
import numpy as np
from math import *
import sys


#Class ini untuk melakukan operasi terhadap titik 3 dimensi termasuk memproyeksikannya dalam bidang 2 dimensi
class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
    #Rotasi pada sumbu x
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array(
            [[1,0,0,0], 
            [0, cosa, -sina, 0], 
            [0,sina, cosa, 0], 
            [0,0,0,1]])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Rotasi pada sumbu Y
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array([
            [cosa,0,sina,0], 
            [0, 1, 0, 0], 
            [-sina,0, cosa, 0], 
            [0,0,0,1]
            ])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Rotasi pada sumbu Z
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array([
            [cosa, -sina ,0,0], 
            [sina, cosa , 0, 0], 
            [0 ,0, 1, 0], 
            [0,0,0,1]
            ])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Translasi
    def translate(self, xTrans, yTrans, zTrans):
        matrix = np.array([
            [1,0,0,xTrans], 
            [0,1,0,yTrans], 
            [0,0,1,zTrans], 
            [0,0,0,1]
            ])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    #Shear
    def Shear(self, Shx,Shy,Shz):
        Shxy = np.array([
            [1, 0, Shx, 0], 
            [0, 1, Shy, 0],
            [0, 0, 1, 0],
            [0,0,0,1]
            ])
        Shyz = np.array([
            [1,0,0,0],
            [0, Shy, 0,0],
            [0, Shz, 1,0],
            [0,0,0,1]
            ])
        Shxz = np.array([
            [Shx, 0, 0, 0],
            [0, 1, 0, 0],
            [Shz, 0, 1,0],
            [0,0,0,1]
            ])
        vector = np.array ([self.x, self.y, self.z, 1])
        if Shz == 0:
            result = Shxy.dot(vector)
        elif Shy == 0:
            result = Shxz.dot(vector)
        elif Shx == 0:
            result = Shyz.dot(vector)
        
        return Point3D(result[0], result[1], result[2])

    def rotateArbitraryAxis(self, point1, point2, angle):
        #Determining arbitrary axis
        xVect = point2[0] - point1[0]
        yVect = point2[1] - point1[1]
        zVect = point2[2] - point1[2]
        beta, miu = 0,0
        if zVect == 0:
            if xVect > 0: 
                beta = 90
            else:
                beta = 270
        else:
            beta = atan(xVect/ zVect) * 180 / pi
        if xVect **2 + zVect**2 == 0:
            if yVect > 0:
                miu = 90
            else:
                miu = 270
        else:
            miu = atan (yVect / sqrt(xVect **2 + zVect**2)) * 180 / pi
        step1 = self.translate(0 - point1[0], 0 - point1[1], 0 - point1[2])
        step2 = step1.rotateY(-beta).rotateX(miu).rotateZ(angle)
        step3 = step2.rotateX(-miu).rotateY(beta)
        result = step3.translate(point1[0] - 0, point1[1] - 0, point1[2] - 0)

        return result
    #Scaling
    def scale(self, factor):
        matrix = np.array([
            [factor, 0, 0, 0],
            [0, factor, 0, 0],
            [0,0,factor, 0],
            [0,0,0,1]
        ])
        vector = np.array([self.x, self.y, self.z, 1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
    
    #Proyeksi ke bidang 2 dimensi
    def project(self, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

#Fungsi ini berfungsi untuk meminta input dari pengguna
def question():
    values = []
    #Program mendeteksi transformasi yang akan dilakukan dengan input dibawah
    operation =int(input(
        """Which transformation would you like to do?
        1. Translation
        2. Rotation about x, y, or z axis
        3. Shear
        4. Rotation about arbitrary axis
        5. Scaling
        6. I just wanna see the untransformed box
        Only answer with the number from 1 to 6!
        (example: to do translation, input '1' without the quotation)
        Input: """))
    #Ketika pengguna memasukan nilai diluar yang diterima, program akan dihentikan
    if operation > 6 or operation < 1:
        print("INVALID INPUT")
        sys.exit()
    
    #Operasi 1 adalah translasi, bagian ini untuk memasukan nilai translasi
    if operation == 1:
        xTrans = int(input("Translate along x axis by how much? ONLY input integer\nInput: "))
        yTrans = int(input("Translate along y axis by how much? ONLY input integer\nInput: "))
        zTrans = int(input("Translate along z axis by how much? ONLY input integer\nInput: "))
        values = [xTrans, yTrans, zTrans]

    #Operasi 2 adalah rotasi, bagian ini untuk memasukan sudut rotasi
    elif operation == 2:
        xRot = float(input("Rotate about x axis by how many degree? ONLY input number\n"))
        yRot = float(input("Rotate about y axis by how many degree? ONLY input number\n"))
        zRot = float(input("Rotate about z axis by how many degree? ONLY input number\n"))
        values = [xRot, yRot, zRot] 

    #Operasi 3 adalah Shear, bagian ini untuk memasukkan nilai shear
    elif operation == 3:
        xShear = float(input("Shear x by how much? ONLY input numbers!\nInput: "))
        yShear = float(input("Shear y by how much? ONLY input numbers!\nInput: "))
        zShear = float(input("Shear z by how much? ONLY input numbers!\nInput: "))
        if(xShear != 0 and yShear != 0 and zShear != 0):
            print("INVALID INPUT! Only fill 2 non-zero input")
            sys.exit()
        values = [xShear, yShear, zShear]
        
    #Operasi 4 adalah rotasi pada arbitrary axis, bagian ini untuk memasukan axis dan sudut rotasi
    elif operation == 4:
        x1, y1,z1 = input("Enter the 1st point of the arbitrary axis (Format: x y z, Example: for point P(1,1,1) please input '1 1 1' without the quotation\nInput: ").split()
        x2, y2,z2 = input("Enter the 2nd point of the arbitrary axis (Format: x y z, Example: for point P(1,1,1) please input '1 1 1' without the quotation\nInput: ").split()
        angle = int(input("By how many degrees?\nInput: "))
        values = [[int(x1), int(y1), int(z1)], [int(x2), int(y2), int(z2)], [angle,0,0]]
    #Operasi 5 adalah scaling, bagian ini untuk memasukan seberapa besar scaling akan dilakukan
    elif operation == 5:
        factor = float(input("scale by how much? Only input numbers!\nInput: "))
        values = [factor]
    #tidak dilakukan transformasi
    elif operation == 6:
        values = [0]

    #Nilai ini bertujuan agar fungsi utama tahu operasi apa yang dilakukan dan besaran nilai transformasinya
    return operation, values


#Fungsi ini merupakan fungsi operasi utama dari program 
def main(operation, values, points):
    #Koordinat titik telah pre-assigned 
    p = 0
    # variabel ini menyimpan titik yang harus dihubungkan untuk membentuk sebuah permukaan pada balok
    # misal 0 1 2 3 artinya sisi pertama terbentuk dengan menghubungkan titik 0 1 2 dan 3
    # 0 1 2 3 tersebut merujuk kepada index pada array points
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]

    width, height = 1280, 720
    #Untuk menyimpan garis yang dibentuk:
    lines = []
    #Untuk menyimpan titik yang dilakukan transformasi:
    operatedPoints = []
    #Untuk menyimpan titik yang telah diproyeksi
    transformedPoints = []

    #Melakukan translasi
    if operation == 1:
        xTrans, yTrans, zTrans = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].translate(xTrans, yTrans, zTrans))
            
    #Melakukan Rotasi terhadap sumbu x y dan z
    elif operation == 2:
        angleX, angleY, angleZ = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ))

    #Melakukan Shear
    elif operation == 3:
        xShear, yShear, zShear = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].Shear(xShear, yShear, zShear))

    #Melakukan rotasi terhadap arbitrary axis
    elif operation == 4:
        point1 = [values[0][0], values[0][1], values[0][2]]
        point2 = [values[1][0], values[1][1], values[1][2]]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateArbitraryAxis(point1, point2, values[2][0]))

    #Melakukan scaling
    elif operation == 5:
        factor = values[0]
        for i in range(len(points)):
            operatedPoints.append(points[i].scale(factor))
    #tidak dilakukan apa apa
    elif operation == 6:
        for i in range(len(points)):
            operatedPoints.append(points[i])
    
    #Melakukan proyeksi koordinat yang telah di transformasi pada bidang 2 dimensi
    for i in range(len(operatedPoints)):
        transformedPoints.append(operatedPoints[i].project(width, height, 500, 6))

    win = GraphWin('3D Transformation', width, height)
    win.setBackground('white')

    #Menentukan nilai garis pembentuk balok
    for i in faces:
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y)))
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
        lines.append(Line(Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y), Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y)))
        lines.append(Line(Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
    #Menggambar garis pembentuk balok
    for i in lines:
        i.draw(win)

    #Menampilkan titik koordinat di x y z
    for i in range(len(transformedPoints)):
        p = Text(Point(transformedPoints[i].x, transformedPoints[i].y), "{:.2f}, {:.2f}, {:.2f}".format(operatedPoints[i].x, operatedPoints[i].y, operatedPoints[i].z))
        p.setSize(8)
        p.setTextColor('Red')
        p.draw(win) 

    ask = int(input("Do you want to do another operation?\nInput 1 for yes, another to exit (number only).\nInput: "))
    if ask==1:
        op, val = question()
        win.close()
        main(op,val, operatedPoints)
    else:
        sys.exit()  
    win.getMouse()
    win.close()

#Nilai ini bertujuan agar fungsi utama tahu operasi apa yang dilakukan dan besaran nilai transformasinya
points = [Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
            ]

op, val = question()
main(op, val, points)