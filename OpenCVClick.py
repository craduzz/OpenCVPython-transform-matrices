import numpy as np
import matplotlib.pyplot as plt
import cv2
import math



pointSelected = False
mouseX = 0
mouseY = 0
clickPointX = 0
clickPointY = 0

def get_click(event, x, y, flag, param):
    global mouseX, mouseY, pointSelected, clickPointX, clickPointY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX, mouseY = x,y
        clickPointX, clickPointY = mouseX, mouseY
        #print(mouseX," ",mouseY)
        pointSelected = True
        #blank_img[mouseY][mouseX] = 0
        draw_point()

def draw_point():
    for i in range(0,6):
        for j in range(0,6):
            blank_img[i-4+mouseY][j-4+mouseX] = 0
    #print(mouseX, " ", mouseY)


def rot_around_point():
    global clickPointX, clickPointY
    #print(angleToCircle)
    rotationArray = np.array([[math.cos(angleToCircle), math.sin(angleToCircle)],
                              [math.sin(angleToCircle) * -1, math.cos(angleToCircle)]])
    print(rotationArray,"\n","--------------------------------------------------")
    clickPointX = clickPointX - mouseX
    clickPointY = clickPointY - mouseY

    newOffset = np.array([randOffsetY - mouseX,randOffsetX - mouseY])
    #print(newOffset)
    finalPos = np.matmul(rotationArray,newOffset)
    finalPos[0] = finalPos[0] + mouseX
    finalPos[1] = finalPos[1] + mouseY
    return finalPos




def rotate_Image(imageSizeX,imageSizeY,randomOffsetX,randomOffsetY):
    rotationArray = np.array([[math.cos(angle), math.sin(angle)],
                              [math.sin(angle) * -1, math.cos(angle)]])

    if pointSelected:
        newOff = rot_around_point()
        #print(newOff)
        randomOffsetY = newOff[0]
        randomOffsetX = newOff[1]
    blank_img.fill(255)
    if pointSelected:
        draw_point()
    for i in range(0, imageSizeX):
        for j in range(0, imageSizeX):

            imgHalfSizeX = imageSizeX/2
            imgHalfSizeY = imageSizeY/ 2

            rotPoints = np.array([i-imgHalfSizeX , j-imgHalfSizeY])

            tmp = np.matmul(rotPoints, rotationArray)

            xval = int(tmp[0]+imgHalfSizeX+randomOffsetX)
            yval = int(tmp[1]+imgHalfSizeY+randomOffsetY)

            if xval < 399 and xval > 0:
                if yval < 399 and yval > 0:

                    blank_img[int(tmp[0]+imgHalfSizeX+randomOffsetX), int(tmp[1]+imgHalfSizeY+randomOffsetY)] = m[i][j]


m = cv2.imread("letra-M.jpeg",0)

blank_img = np.zeros((400, 400), np.uint8)
blank_img = np.add(blank_img, 255)

# busca la mitad del tamaño de las 2 imagenes
middle_largeX = int(blank_img.shape[0] / 2)
middle_largeY = int(blank_img.shape[1] / 2)
middle_smallX = int(m.shape[0] / 2)
middle_smallY = int(m.shape[1] / 2)

# coordenadas para centrar la imagen chica en la imagen grande
a = middle_largeX - middle_smallX
b = middle_largeY - middle_smallY

# coordenada random en y
randOffsetY = np.random.randint(300)
randOffsetY = a + randOffsetY - 150


# coordenada random en x
randOffsetX = np.random.randint(300)
randOffsetX = b + randOffsetX - 150


# angulo random para la rotacion
randomRotation = np.random.randint(180)

angle = randomRotation * math.pi / 180
incrOneDeg = 3 * math.pi / 180

angleToCircle = angle


#--------------------------------------------------------------------------------------------------------------------------------

print(randOffsetX)
print(randomRotation)

setPoint = False


while True:
    cv2.namedWindow('test')
    cv2.setMouseCallback('test', get_click)
    cv2.imshow('test',blank_img)

    #print(angle)


    if pointSelected:
        draw_point()
        angleToCircle = angleToCircle + incrOneDeg

    #print(mouseX," ",mouseY)

    rotate_Image(m.shape[0],m.shape[1],randOffsetX,randOffsetY)
    k = cv2.waitKey(100)
    if (k == 27): break


    #cv2.destroyAllWindows()

