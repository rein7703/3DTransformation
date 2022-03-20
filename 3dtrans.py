from graphics import *
import numpy as np
from math import *
from time import sleep


class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array([[1,0,0,0], [0, cosa, -sina, 0], [0,sina, cosa, 0], [0,0,0,1]])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array([[cosa,0,sina,0], [0, 1, 0, 0], [-sina,0, cosa, 0], [0,0,0,1]])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        matrix = np.array([[cosa, -sina ,0,0], [sina, cosa , 0, 0], [0 ,0, 1, 0], [0,0,0,1]])
        vector = np.array([self.x, self.y, self.z,1])
        result = matrix.dot(vector)
        return Point3D(result[0], result[1], result[2])
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

        


def main():
    points = [Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]

    # Define the vertices that compose each of the 6 faces. These numbers are
    # indices to the vertices list defined above.
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]

    angleX, angleY, angleZ = 0, 0, 0

    win = GraphWin('Test', 640, 480)
    win.setBackground('white')
    lines = []
    transformedPoints = []
    for i in range(len(points)):
        transformedPoints.append(points[i].project(640, 400, 500, 4))

    for i in faces:
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y)))
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
        lines.append(Line(Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y), Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y)))
        lines.append(Line(Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))

    for i in lines:
        i.draw(win)

    win.getMouse()
    win.close()



main()