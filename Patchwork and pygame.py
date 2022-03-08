import pygame
import numpy
import os

tile_1 = numpy.array([
    [0, 0, 1],
    [1, 1, 1]
])
tile_2 = numpy.array([
    [0, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 0]
])
tile_3 = numpy.array([
    [0, 1],
    [1, 1]
])
tile_4 = numpy.array([
    [0, 0, 1, 1],
    [1, 1, 1, 1]
])
tile_5 = numpy.array([
    [1, 1, 1, 1, 1]
])
tile_6 = numpy.array([
    [1, 1, 1, 1],
    [0, 0, 0, 1]
])
tile_7 = numpy.array([
    [0, 0, 0, 1],
    [1, 1, 1, 1],
    [0, 0, 0, 1]
])
tile_8 = numpy.array([
    [1, 1],
    [1, 1]
])
tile_9 = numpy.array([
    [0, 0, 1],
    [0, 1, 1],
    [1, 1, 0]
])
tile_10 = numpy.array([
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0]

])

tiles_list = [(tile_1, 'tile_1.bmp'), (tile_2, 'tile_2.bmp'), (tile_3, 'tile_3.bmp'),
              (tile_4, 'tile_4.bmp'), (tile_5, 'tile_5.bmp'), (tile_6, 'tile_6.bmp'),
              (tile_7, 'tile_7.bmp'), (tile_8, 'tile_8.bmp'), (tile_9, 'tile_9.bmp'),
              (tile_10, 'tile_10.bmp')]


class Tile:
    '''цена, время, базовые конфигурации'''

    def __init__(self, price, time_taken, basic_configuration):
        self.price = price
        self.time_taken = time_taken
        self.basic_configuration = basic_configuration

    def get_all_configurations(self):
        configurations = [self.basic_configuration]
        configurations.append(self.basic_configuration.rotated_90)
        configurations.append(self.basic_configuration.rotated_180)
        configurations.append(self.basic_configuration.rotated_90.rotated_180)
        configurations.append(self.basic_configuration.mirrored)
        configurations.append(self.basic_configuration.mirrored.rotated_90)
        configurations.append(self.basic_configuration.mirrored.rotated_180)
        configurations.append(self.basic_configuration.mirrored.rotated_90.rotated_180)
        return configurations


class Shape:
    '''Генератор всех возможных шейпов'''

    def __init__(self, tile, cost):  # tile типа numpy.array
        self.shape = tile
        self.cost = cost

    def mirrored(self):
        return numpy.flip(self.shape, axis=1)

    def rotated_90(self):
        return numpy.rot90(self.shape)

    def rotated_180(self):
        return numpy.rot90(self.shape, 2)


class QuiltBoard:
    def __init__(self):
        self.board_list = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def check_7x7(self):
        pass

    def check_tile(self, x, y, tile):
        '''
        проверка, можно ли поставить тайл в координаты x, y,
        где x и y - координаты левого верхнего угла
        '''
        tile_height, tile_width = len(tile), len(tile[0])
        if (tile_height + y >= 9) or (tile_width + x >= 9):
            return False
        empty_field_with_tile = numpy.zeros((9, 9), dtype=int)
        empty_field_with_tile[y:(y + tile_height), x:(x + tile_width)] = tile
        return numpy.all(empty_field_with_tile & self.board_list == 0)

    def place_tile(self, x, y, tile):
        '''
        перед вызовом метода нужно проверить, можно ли вставить тайл
        x и y - координаты верхнего левого угла
        '''
        for index_i, i in enumerate(tile):
            for index_j, j in enumerate(i):
                self.board_list[y + index_i][x + index_j] += j

    def check_bonus(self, tile):
        pass

    def get_empties(self):
        pass


class TimeLine:
    def __init__(self):
        pass


class Player:
    def __init__(self):
        self.bonus = 0
        self.money = 0
        self.tiles = []


class Board:
    def __init__(self, width, height, tiles_list):
        self.width = width
        self.height = height
        self.board = QuiltBoard()
        self.left = 20
        self.top = 20
        self.cell_size = 50
        self.color = 0
        self.tiles_list = tiles_list  # нампаевские тайлы
        self.condition = False  # отвечает за то, можно ли ставить тайл

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        x, y, s = self.left, self.top, self.cell_size
        for i in self.board.board_list:
            for j in i:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, s, s), 1)
                x += s
            x = self.left
            y += s
        # рисуем окошко, где будут показываться детальки
        pygame.draw.rect(screen, (255, 255, 255), (323, 8, 154, 154), 2)
        # к нему кнопку, которая должна пролистывать детальки, это спрайт
        # нет, блин, кола
        pygame.draw.rect(screen, (74, 55, 97), (325, 170, 30, 30))
        # которая поворачивает детальку
        pygame.draw.rect(screen, (74, 172, 214), (370, 170, 30, 30))
        # кнопка, при нажатии на которую мы переходи в режим выставления детальки на поле
        pygame.draw.rect(screen, (94, 148, 118), (415, 170, 30, 30))

    def get_click(self, mouse_pos, index, screen):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, index, screen)
        elif self.check_button_rot(mouse_pos):
            self.rotate_tile()
        elif self.check_button_next(mouse_pos):
            self.do_next()
            return True
        elif self.check_button_set(mouse_pos):
            self.waiting_for_position()

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or x > self.left + self.width * self.cell_size:
            return None
        if y < self.top or y > self.top + self.height * self.cell_size:
            return None
        x_num = (x - self.left) // self.cell_size
        y_num = (y - self.top) // self.cell_size
        return (x_num, y_num)

    def check_button_rot(self, mouse_pos):
        x, y = mouse_pos
        if 325 <= x <= 355 and 170 <= y <= 200:
            print('rot')
            return True
        return False

    def check_button_next(self, mouse_pos):
        x, y = mouse_pos
        if 370 <= x <= 400 and 170 <= y <= 200:
            print('next')
            return True
        return False

    def check_button_set(self, mouse_pos):
        x, y = mouse_pos
        if 415 <= x <= 445 and 170 <= y <= 200:
            print('set')
            return True
        return False

    def on_click(self, cell, index, screen):
        print(cell)
        # если мы нажали на кнопку согласия на постановку тайла
        if self.condition:
            # если мы можем поставить тайл (проверяем при помощи метода класса квилтбоардъ)
            if self.board.check_tile(*cell, self.tiles_list[index][0]):
                # закрашиваем
                self.board.place_tile(*cell, self.tiles_list[index][0])
                for y in range(len(self.board.board_list)):
                    for x in range(y):
                        if self.board.board_list[y][x]:
                            pygame.draw.rect(screen, (244, 196, 8), (10 + x * 30, 10 + y * 30, 30, 30))

    def rotate_tile(self):
        pass

    def do_next(self):
        pass

    def waiting_for_position(self):
        self.condition = True

    # def fill_cell(self, cell, screen):
    #     x, y = cell
    #     pygame.draw.rect(screen, (244, 196, 8), (10 + x * 30, 10 + y * 30, 30, 30))


class TilesSprites(pygame.sprite.Sprite):
    '''создаём спрайты для кнопок'''
    def __init__(self, tile, path):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(path).convert()
        self.image = player_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 85)
        self.tile = tile

    def update(self):
        pass


if __name__ == '__main__':
    pygame.init()
    size = width, height = 700, 600
    screen = pygame.display.set_mode(size)
    # создаём объект с лоскутным одеялом
    board = Board(9, 9, tiles_list)
    board.set_view(10, 10, 30)

    # Делаем кнопки
    all_sprites = pygame.sprite.Group()
    all_tiles = []
    for tile in tiles_list:
        all_sprites.add(TilesSprites(tile[0], tile[1]))
        all_tiles.append(TilesSprites(tile[0], tile[1]))
    index = 0

    running = True
    while running:
        screen.fill((0, 0, 0))
        board.render(screen)
        screen.blit(all_tiles[index % 10].image, all_tiles[index % 10].rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                f = board.get_click(event.pos, index, screen)
                if f:
                    index += 1

        # нужно отрисовывать один тайл, а не все сразу

        # all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()