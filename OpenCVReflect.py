import numpy as np
import cv2
import math



pointSelected = False
lineDrawn = False
calculate_slope = True
mouseX = 0
mouseY = 0
clickPointX = 0
clickPointY = 0
lineArray = []

m_slope = 0

def get_click(event, x, y, flag, param):
    global mouseX, mouseY, pointSelected, lineArray,lineDrawn
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX, mouseY = x,y

        print(mouseX," ",mouseY)
        pointSelected = True
        #blank_img[mouseY][mouseX] = 0
        draw_point()

        if len(lineArray)<2:
            point = [mouseX, mouseY]
            lineArray.append(point)

        if len(lineArray)>=2:
            lineDrawn = True

def draw_point():
    #print(lineArray)
    for point in lineArray:
        for i in range(0,6):
            for j in range(0,6):
                blank_img[i-4+point[1]][j-4+point[0]] = 0
    #print(mouseX, " ", mouseY)


def reflect_Image(m_slope,x,y,pixelVal):

    #reflected_x = ( ( (1 - math.pow(m_slope,2)) / (1 + math.pow(m_slope,2)) ) * x) + ( ( (2*m_slope) / (1 + math.pow(m_slope,2)) ) * y)

    #reflected_y = ( ( (2*m_slope) / (1 + math.pow(m_slope,2)) ) * x) + ( ( (math.pow(m_slope,2) - 1) / (1 + math.pow(m_slope,2)) ) * y)

    c_val = lineArray[0][1] - (m_slope*lineArray[0][0])
    b_val = -1
    a_val = m_slope

    reflected_x = (( ( math.pow( b_val,2 )-math.pow( a_val,2 ) )*y )-(2*a_val*b_val*x)-(2*a_val*c_val)) / (math.pow(a_val,2)+math.pow(b_val,2))

    reflected_y = ((-2*a_val*b_val*y) + ((math.pow(a_val,2)-math.pow(b_val,2))*x) - (2*b_val*c_val)) / (math.pow(a_val,2)+math.pow(b_val,2))

    print(reflected_x," ------------- ",reflected_y)
    if reflected_x < 399 and reflected_x > 0:
        if reflected_y < 399 and reflected_y > 0:
            blank_img[int(reflected_y)][int(reflected_x)] = pixelVal

    #print(m_slope)




def rotate_Image(imageSizeX,imageSizeY,randomOffsetX,randomOffsetY):
    global m_slope, calculate_slope
    rotationArray = np.array([[math.cos(angle), math.sin(angle)],
                              [math.sin(angle) * -1, math.cos(angle)]])
    blank_img.fill(255)
    draw_point()
    if pointSelected:
        draw_point()
    for i in range(0, imageSizeX):
        for j in range(0, imageSizeX):

            imgHalfSizeX = imageSizeX/2
            imgHalfSizeY = imageSizeY/ 2

            rotPoints = np.array([i-imgHalfSizeX , j-imgHalfSizeY])

            tmp = np.matmul(rotPoints, rotationArray)

            blank_img[int(tmp[0]+imgHalfSizeX+randomOffsetX), int(tmp[1]+imgHalfSizeY+randomOffsetY)] = m[i][j]

            pointx = int(tmp[0]+imgHalfSizeX+randomOffsetX)
            pointy = int(tmp[1]+imgHalfSizeY+randomOffsetY)

            if lineDrawn:
                if calculate_slope:
                    m_slope = (lineArray[1][1] - lineArray[0][1]) / (lineArray[1][0] - lineArray[0][0])
                    calculate_slope = False
                reflect_Image(m_slope,pointx,pointy,m[i][j])


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

    if pointSelected:
        draw_point()
        angleToCircle = angleToCircle + incrOneDeg

    rotate_Image(m.shape[0],m.shape[1],randOffsetX,randOffsetY)






    k = cv2.waitKey(100)
    if (k == 27): break


    #cv2.destroyAllWindows()

