import pygame
import random
import math


SCREEN_DIM = (1024, 768)


class Vec2d():
    def __init__(self, x):
        super().__init__()
        self.x = x[0]
        self.y = x[1]

    def __len__(self):
        """функция len() возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __add__(self, v):
        """возвращает сумму двух векторов"""
        return Vec2d((self.x + v.x, self.y + v.y))

    def __sub__(self, v):
        """"возвращает разность двух векторов"""
        return Vec2d((self.x - v.x, self.y - v.y))

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x * k, self.y * k))

    def int_pair(self):
        """возврщает текущие координаты вектора"""
        return self.x, self.y


class Polyline():
    def __init__(self):
        super().__init__()
        self.points = []
        self.speeds = []

    def slow_down(self):
        for i in range(len(self.speeds)):
            self.speeds[i] *= 0.5

    def speed_up(self):
        for i in range(len(self.speeds)):
            self.speeds[i] *= 2

    def add_vec2d(self, vec, speed):
        """функция добавления координаты точки и ее скорости, обе переменных должны принадлежать классу Vec2d"""
        self.points.append(vec)
        self.speeds.append(speed)

    def remove_vec2d(self):
        """убирает поседнюю опорную точку"""
        if len(self.points) > 0:
            self.points.pop(-1)
            self.speeds.pop(-1)

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p].x = self.points[p].x + self.speeds[p].x
            self.points[p].y = self.points[p].y + self.speeds[p].y
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x = - self.speeds[p].x
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y = - self.speeds[p].y

    def draw_points(self, points=None, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if points is None:
            points = self.points

        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)


class Knot(Polyline):
    def __init__(self, count=5):
        super().__init__()
        self.count = count

    def add_vec2d(self, vec, speed):
        super().add_vec2d(vec, speed)
        self.get_knot()

    def remove_vec2d(self):
        super().remove_vec2d()
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def get_knot(self):
        """функция сглаживания кривой"""
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self._get_points(ptn))
        return res

    def _get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self._get_point(base_points, i * alpha))
        return res

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self._get_point(points, alpha, deg - 1) * (1 - alpha)


def draw_help(polyline, polyline2):
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["", ""])
    data.append(["", "First polyline"])
    data.append(["Left mouse button", "New dot"])
    data.append(["Delete", "Remove last dot"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Q", "Speed up"])
    data.append(["W", "Slow down"])
    data.append([str(polyline.count), "Current points"])
    data.append(["", ""])
    data.append(["", "Second polyline"])
    data.append(["Right mouse button", "New dot"])
    data.append(["Backspace", "Remove last dot"])
    data.append(["=", "More points"])
    data.append(["-", "Less points"])
    data.append(["A", "Speed up"])
    data.append(["S", "Slow down"])
    data.append([str(polyline2.count), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (1024, 0), (1024, 768), (0, 768)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (400, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    show_help = False
    pause = True
    polyline = Knot()
    polyline2 = Knot()

    hue = 0
    color = pygame.Color(0)
    color2 = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline.points = []
                    polyline.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    polyline.count += 1
                if event.key == pygame.K_EQUALS:
                    polyline2.count += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    polyline.count -= 1 if polyline.count > 1 else 0
                if event.key == pygame.K_MINUS:
                    polyline2.count -= 1 if polyline2.count > 1 else 0
                if event.key == pygame.K_DELETE:
                    polyline.remove_vec2d()
                if event.key == pygame.K_BACKSPACE:
                    polyline2.remove_vec2d()
                if event.key == pygame.K_q:
                    polyline.speed_up()
                if event.key == pygame.K_w:
                    polyline.slow_down()
                if event.key == pygame.K_a:
                    polyline2.speed_up()
                if event.key == pygame.K_s:
                    polyline2.slow_down()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                polyline.add_vec2d(Vec2d(event.pos), Vec2d((random.random() * 2, random.random() * 2)))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                polyline2.add_vec2d(Vec2d(event.pos), Vec2d((random.random() * 2, random.random() * 2)))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        color2.hsla = (hue, 100, 70, 10)
        polyline.draw_points()
        polyline2.draw_points(color=(0, 255, 0))
        polyline.draw_points(polyline.get_knot(), "line", 3, color)
        polyline2.draw_points(polyline2.get_knot(), "line", 3, color2)
        if not pause:
            polyline.set_points()
            polyline2.set_points()
        if show_help:
            draw_help(polyline, polyline2)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
