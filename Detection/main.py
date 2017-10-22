import matplotlib.pyplot as plt

from help import *
from hough import my_hough, my_hough_mask
from reader import *


from PIL import Image


images = read_images('Camera1/')

length = len(images)

if (length == 0):
    print ('Фотографий по данному пути не найдено')

else:
    print('Найдено ', length, ' фотографий')


    for image in images:
        imshape = image.shape

        # Черно-белое изображение
        #print (imshape[0], imshape[1])
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 1: Исходное изображение
        plt.subplot(3, 3, 1)
        plt.imshow(gray, cmap="gray")

        # Сглаживанем изображение
        blurred_grey = gaussian_blur(gray, 17)

        #  Получение черно-белого сглаженного изображения
        bw_blurred_grey = cv2.cvtColor(blurred_grey, cv2.COLOR_GRAY2BGR)

        # 2: Черно-белое сглаженное изображение
        plt.subplot(3, 3, 2)
        plt.imshow(bw_blurred_grey)

        # Применяем оператор Canny
        edges = canny(blurred_grey, 23, 13)

        # Применяем маску для изображения
        vertices = np.array([[(0, 0), (0, imshape[0]-128), (imshape[1], imshape[0]-128), (imshape[1], 0)]], dtype=np.int32)

        # Находим необходимые ребра
        edges_with_mask = region_of_interest(edges, vertices)

        # 3: Ребра полученные опертором Canny, в нужной нам области
        plt.subplot(3, 3, 3)
        plt.imshow(edges_with_mask, cmap="gray")

        # Применяем алгоритм Хафа для Canny
        lines_hough = my_hough(edges_with_mask, 0)
        bw_grey1 = cv2.cvtColor(gray2, cv2.COLOR_GRAY2BGR)
        lines_image = draw_lines(bw_grey1, lines_hough)

        # 4: Необходимые нам линии
        plt.subplot(3, 3, 4)
        plt.imshow(lines_image)

        # Фильтрованный Хаф
        lines_hough_mask = my_hough_mask(edges_with_mask)
        bw_grey2 = cv2.cvtColor(gray2, cv2.COLOR_GRAY2BGR)

        lines_image_mask = draw_lines_inf(bw_grey2, lines_hough_mask)



        bw_grey3 = cv2.cvtColor(gray2, cv2.COLOR_GRAY2BGR)
        linesH, linesL, linesR = lines_analizator(bw_grey3, lines_hough_mask)

        # 5: Изображение с 3мя вида линий: горизонтальные, наклонно-возрастающие и наклонно-убывающие
        plt.subplot(3, 3, 5)
        plt.imshow(bw_grey3)

        #6 Изображение лобового стекла
        bw_grey4 = cv2.cvtColor(gray2, cv2.COLOR_GRAY2BGR)
        bw_grey5  = searchPoints(bw_grey4, linesH, linesL, linesR)

        plt.subplot(3, 3, 6)
        plt.imshow(bw_grey5)



        cv2.imwrite("temp_image.jpg", bw_grey5)

        im = Image.open('temp_image.jpg')

        # Определяем размер фотографии
        width, height = im.size
        '''
        data = []
        total = 0
        total2 = 0
        for i in range(10, width-10):
            for j in range(0, height-30):
                total += im.getpixel((i, j))[0]

            print("subtotal[ ",i ,"] = ", total / height)
            if i % 1 == 0:
                data.append([total, i])
                total2  = 0
            else:
                total2 += total

            total = 0


        '''
        rgb1 = []
        rgb2 = []
        for i in range (0, 256):
            rgb1.append(0)
            rgb2.append(0)

        area = (width // 2 - 10)*(height-25)

        dataY1 = []
        total = 0
        average11 = 0
        average12 = 0
        average22 = 0
        average21 = 0

        for i in range(5, height-30):
            for j in range(20, width // 2 - 10):
                temp = im.getpixel((j, i))[0]
                total += temp
                rgb1[ temp ] += 1
            if (i<35):
                average11 += total
            else:
                average12 += total
            dataY1.append([total, i])
            total = 0

        dataY2 = []
        total = 0
        for i in range(5, height-30):
            for j in range(width // 2 + 10, width - 20):
                temp = im.getpixel((j, i))[0]
                total += temp
                rgb2[temp] += 1
            if (i<35):
                average21 += total
            else:
                average22 += total
            dataY2.append([total, i])
            total = 0


        '''
        sum1 = 0
        sum2 = 0
        sumSr1 = 0
        sumSr2 = 0

        for i in range(0, 256):
            rgb1[i] = rgb1[i] / area
            rgb2[i] = rgb2[i] / area

            sum1 += rgb1[i]
            sum2 += rgb2[i]
        x1 = sum1/255
        x2 = sum2/255

        print('Среднее арифметическое пассажира', x1)
        print('Среднее арифметическое водителя', x2)

        for i in range(0, 256):
            sumSr1 += (rgb1[i] - x1) **2
            sumSr2 += (rgb2[i] - x2) **2

        sumSr1 = sumSr1/255
        sumSr2 = sumSr2 / 255

        print('Дисперсия пассажира', math.sqrt(sumSr1))
        print('Дисперсия водителя',  math.sqrt(sumSr2))
        '''

        MX11 = 0
        MX12 = 0
        MX1 = 0
        MX2 = 0
        xs = [x for x in rgb1]
        ys = [x for x in rgb2]
        for i in range (0, 256):
            rgb1[i] = rgb1[i] / area
            rgb2[i] = rgb2[i] / area
            MX1 += i * rgb1[i]
            MX2 += i * rgb2[i]

        for i in range(0, 256):
            MX11 += i*i * rgb1[i]
            MX12 += i*i * rgb2[i]

        DX1 = MX11 - (MX1 * MX1)
        DX2 = MX12 - (MX2 * MX2)


        print('Дисперсия пассажира', math.sqrt(DX1))
        print('Дисперсия водителя', math.sqrt(DX2))


        print('_____________________________')

        area1 = 30 * (width // 2 - 30)
        area2 = (height - 65) * (width // 2 - 30)


        if (area1>0 and area2 >0):
            average11 = average11 / area1
            average12 = average12 / area2

            average21 = average21 / area1
            average22 = average22 / area2
        else:
            average11 = 0
            average21 = 100

        print("Среднее арифметичекое значение для области лица пассажира и водителя:", average11, average21 )
        print("Среднее арифметичекое значение для области туловища пассажира и водителя:", average12, average22)


        plt.subplot(3, 3, 8)
        plt.axis('off')
        if (height >200 and width > 300):
            plt.text(0.5, 0.5, 'Не удалось выделить лобовое стекло',
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize=20,
                     ha='center',
                     va='center')
        elif (math.fabs(average11 -average21)<6.52 ):
            plt.text(0.5,0.5, '2 человека',
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize=20,
                     ha='center',
                     va = 'center')
        else:
            plt.text(0.5, 0.5, '1 человек',
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize=20,
                     ha='center',
                     va='center'
                     )


        sum = 0
        for i in range(0, width ):
            for j in range(0, height):
                sum += im.getpixel((i, j))[0]

        sum = sum /(width * height)
        print("Среднее значение ", sum)
        print('_____________________________')
        print('')



        plt.show()




