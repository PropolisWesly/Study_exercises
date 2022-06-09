import csv
import os


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        split = os.path.splitext(self.photo_file_name)
        ext = split[1] or split[0]
        return ext


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'

        #делим строку по x, смотрим: отвечают ли подстроки вещественному числу
        body_list = body_whl.rsplit(sep='x')
        body_list_test = []
        for element in body_list:
            dig = element.replace('.', '', 1)
            body_list_test.append(dig.isdigit())

        if False in body_list_test or len(body_list_test) != 3:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
        else:
            self.body_length = float(body_list[0])
            self.body_width = float(body_list[1])
            self.body_height = float(body_list[2])

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            #проверка общих столбцов на правильность ввода
            #проверяем 0 столбец
            #print(row)
            if len(row) != 7:
                continue
            if row[0] not in ('car', 'truck', 'spec_machine'):
                continue
            #проверяем 1 столбец
            if not row[1]:
                continue
            #проверяем 3 столбец
       #     ext_list = ['.png', '.jpg', '.gif', '.jpeg']
        #    i = True
         #   for element in ext_list:
          #      if element in row[3]:
           #         i = False
           # if i:
           #     continue

            ext_list_without_jpeg = ['.png', '.jpg', '.gif']
            if not ((row[3][-4:] in ext_list_without_jpeg) or (row[3][-5:] == '.jpeg')):
                continue
            if row[3][0] == '.':
                continue
                #проверяем 5 столбец
            dig = row[5].replace('.', '', 1)
            if not dig.isdigit():
                continue
            row[5] = float(row[5])

            #рассмотр отдельных столбцов для каждого класса
            #работаем с car
            if row[0] == 'car':
                #проверяем 2 на int
                if not row[2].isdigit():
                    continue
                #проверяем 4 и 6 на отсутствие
                if row[4] or row[6]:
                    continue
                #переводим в класс cars
                ittery = Car(row[1], row[3], row[5], row[2])
                car_list.append(ittery)
            #    print('car add...')
                continue
            #работаем с классом truck
            elif row[0] == 'truck':
                #4 столбец работаетв классе, проверяем отсутствие 2 и 6
                if row[2] or row[6]:
                    continue
                #переводим в класс Truck
                ittery = Truck(row[1], row[3], row[5], row[4])
                car_list.append(ittery)
             #   print('truck add...')
                continue
            #работаем с классом SpecMachine
            else:
                #6 столбец должен содержать что-то
                if not row[6]:
                    continue
                #2 и 4 должны быть пусты
                if row[2] or row[4]:
                    continue
                #переводим в класс SpecMachine
                ittery = SpecMachine(row[1], row[3], row[5], row[6])
                car_list.append(ittery)
              #  print('spec_machine add...')
                continue

    return car_list





#truck = Truck('Glory', 'OwO.jpeg', 12345, '1x4x15')
#print(truck.get_body_volume())
#print(truck.get_photo_file_ext())


#cars = get_car_list('cars_week3.csv')
##print(len(cars))
#print(type(cars[2]))



