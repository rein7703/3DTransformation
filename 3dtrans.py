from graphics import *
import numpy as np
from math import *
import sys



class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
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

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

def question():
    values = []
    operation =int(input(
        """Which operation would you like to do?
        1. Translation
        2. Rotation about x, y, or z axis
        3. Shear
        4. Rotation about arbitrary axis
        5. Scaling
        Only answer with the number from 1 to 5!
        (example: to do rotation, input '1' without the quotation)
        Input: """))
    if operation > 8 or operation < 1:
        print("INVALID INPUT")
        sys.exit
    if operation == 1:
        xTrans = int(input("Translate along x axis by how much? ONLY input integer\nInput: "))
        yTrans = int(input("Translate along y axis by how much? ONLY input integer\nInput: "))
        zTrans = int(input("Translate along z axis by how much? ONLY input integer\nInput: "))
        values = [xTrans, yTrans, zTrans]
    elif operation == 2:
        xRot = float(input("Rotate about x axis by how many degree? ONLY input number\n"))
        yRot = float(input("Rotate about y axis by how many degree? ONLY input number\n"))
        zRot = float(input("Rotate about z axis by how many degree? ONLY input number\n"))
        values = [xRot, yRot, zRot] 
    elif operation == 3:
        xShear = float(input("Shear x by how much? ONLY input numbers!\nInput: "))
        yShear = float(input("Shear y by how much? ONLY input numbers!\nInput: "))
        zShear = float(input("Shear z by how much? ONLY input numbers!\nInput: "))
        if(xShear != 0 and yShear != 0 and zShear != 0):
            print("INVALID INPUT! Only fill 2 non-zero input")
            sys.exit()
        values = [xShear, yShear, zShear]
        
    elif operation == 4:
        x1, y1,z1 = input("Enter the 1st point of the arbitrary axis (Format: x y z, Example: for point P(1,1,1) please input '1 1 1' without the quotation\nInput: ").split()
        x2, y2,z2 = input("Enter the 1st point of the arbitrary axis (Format: x y z, Example: for point P(1,1,1) please input '1 1 1' without the quotation\nInput: ").split()
        angle = int(input("By how many degrees?\nInput: "))
        values = [[int(x1), int(y1), int(z1)], [int(x2), int(y2), int(z2)], [angle,0,0]]
    elif operation == 5:
        factor = int(input("scale by how much? Only input numbers!\nInput: "))
        values = [factor]
    return operation, values



def main(operation, values):
    points = [Point3D(-1,1,-1),
                Point3D(1,1,-1),
                Point3D(1,-1,-1),
                Point3D(-1,-1,-1),
                Point3D(-1,1,1),
                Point3D(1,1,1),
                Point3D(1,-1,1),
                Point3D(-1,-1,1)
            ]
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]

    width, height = 640, 400
    lines = []
    operatedPoints = []
    transformedPoints = []
    if operation == 1:
        xTrans, yTrans, zTrans = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].translate(xTrans, yTrans, zTrans))
            
    elif operation == 2:
        angleX, angleY, angleZ = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ))

    elif operation == 3:
        xShear, yShear, zShear = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].Shear(xShear, yShear, zShear))

    elif operation == 4:
        point1 = [values[0][0], values[0][1], values[0][2]]
        point2 = [values[1][0], values[1][1], values[1][2]]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateArbitraryAxis(point1, point2, values[2][0]))

    elif operation == 5:
        factor = values[0]
        for i in range(len(points)):
            operatedPoints.append(points[i].scale(factor))
    for i in range(len(operatedPoints)):
        transformedPoints.append(operatedPoints[i].project(640, 400, 500, 4))

    win = GraphWin('Test', width, height)
    win.setBackground('white')
    for i in faces:
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y)))
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
        lines.append(Line(Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y), Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y)))
        lines.append(Line(Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))

    for i in lines:
        i.draw(win)
        #print(i)
    win.getMouse()
    win.close()


op, val = question()
main(op, val)