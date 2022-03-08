import pygame
import numpy
import os
from random import choice

BOARD_HEIGHT = 9
BOARD_WIDTH = 9
CONFIG_NUM = 4

BLUE = (74, 172, 214)
GREEN = (94, 148, 118)
PURPLE = (74, 55, 97)
RED = (0, 0, 0)

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


class Tile:
    '''цена, время, базовые конфигурации'''

    def __init__(self, placing_price, placing_time, button_income, basic_configuration, images):
        self.basic_configuration = Shape(basic_configuration)
        self.images = images
        self.placing_time = placing_time
        self.placing_price = placing_price
        self.button_income = button_income


    @property
    def all_configurations(self):
        configurations = []
        configurations.append(self.basic_configuration.rotated_90(0))
        configurations.append(self.basic_configuration.rotated_90(1))
        configurations.append(self.basic_configuration.rotated_90(2))
        configurations.append(self.basic_configuration.rotated_90(3))
        # configurations.append(self.basic_configuration.mirrored)
        # configurations.append(self.basic_configuration.mirrored.rotated_90)
        # configurations.append(self.basic_configuration.mirrored.rotated_180)
        # configurations.append(self.basic_configuration.mirrored.rotated_90.rotated_180)
        return configurations


class Shape:
    '''Генератор всех возможных шейпов'''

    def __init__(self, tile):  # tile типа numpy.array
        self.shape = tile

    def mirrored(self):
        return numpy.flip(self.shape, axis=1)

    def rotated_90(self, n):
        return numpy.rot90(self.shape, n)

    @property
    def height(self):
        return len(self.shape)

    @property
    def width(self):
        if self.height == 0:
            return 0
        else:
            return len(self.shape[0])


class QuiltBoard:
    def __init__(self):
        self.board_list = numpy.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.is_bonus_7x7_received = False
        self.bonus_coords = None

    def check_7x7(self):
        for y in range(BOARD_HEIGHT - 7 + 1):
            for x in range(BOARD_WIDTH - 7 + 1):
                field_7x7 = numpy.ones((7, 7), dtype=int)
                if numpy.all(field_7x7 & self.board_list[y:y+7, x:x+7]):
                    self.bonus_coords = (x, y)
                    return True
        return False

    def check_tile(self, x, y, tiles):
        '''
        проверка, можно ли поставить тайл в координаты x, y,
        где x и y - координаты левого верхнего угла
        '''
        global image_configuration
        tile_height, tile_width = len(tiles[image_configuration]), len(tiles[image_configuration][0])
        if (tile_height + y > BOARD_HEIGHT) or (tile_width + x > BOARD_WIDTH):
            return False
        empty_field_with_tile = numpy.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        empty_field_with_tile[y:(y + tile_height), x:(x + tile_width)] = tiles[image_configuration]
        return numpy.all(empty_field_with_tile & self.board_list == 0)

    def place_tile(self, x, y, tiles):
        '''
        перед вызовом метода нужно проверить, можно ли вставить тайл
        x и y - координаты верхнего левого угла
        '''
        global image_configuration, qb_received_7x7
        for index_i, i in enumerate(tiles[image_configuration]):
            for index_j, j in enumerate(i):
                self.board_list[y + index_i][x + index_j] += j
        if not qb_received_7x7:
            if self.check_7x7():
                self.is_bonus_7x7_received = True
                qb_received_7x7 = self


    @property
    def empties_num(self):
        return BOARD_WIDTH*BOARD_HEIGHT - sum([sum(line) for line in self.board_list])


class TimeLine:
    def __init__(self, player1, player2):
        self.num_cells = 54
        self.button_income_coords = [5, 11, 17, 23, 29, 35, 41, 47, 53]
        self.special_patch_coords = [20, 26, 32, 44, 50]
        self.board = [] * 54
        self.player1 = player1
        self.player2 = player2

    def is_game_finished(self):
        if self.player1.timeline_position == 53 and self.player2.timeline_position == 53:
            return True
        return False

    def who_moves(self):
        if self.player1.timeline_position > self.player2.timeline_position:
            return self.player1
        if self.player1.timeline_position < self.player2.timeline_position:
            return self.player2
        else:
            # возвращает первого игрока, добавленного в список определенной клетки поля
            return self.board[self.player2.timeline_position][-1]



class Board:
    def __init__(self, width, height, tiles_list, qb1, qb2):
        self.width = width
        self.height = height
        self.left = 20
        self.top = 20
        self.cell_size = 50
        self.qb1 = qb1
        self.qb2 = qb2

        self.tiles_list = tiles_list  # список из объектов класса Tile
        self.condition = False  # отвечает за то, можно ли ставить тайл
        self.filled_cells = []
        # хотелось бы, чтобы после того, как мы ставим детальку, больше мы не могли её достать
        # для этого нужно удалить её из списка, но нам всё равно нужен индекс. Проблема: индекс
        # индекс лежит не в классе, менять
        self.dif_index = 0

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        x, y, s = self.left, self.top, self.cell_size
        # рисуем первый QuiltBoard
        for i in self.qb1.board_list:
            for _ in i:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, s, s), 1)
                x += s
            x = self.left
            y += s

        # рисуем второй QuiltBoard
        for i in self.qb2.board_list:
            for _ in i:
                pygame.draw.rect(screen, (255, 255, 255), (x, y + 30, s, s), 1)
                x += s
            x = self.left
            y += s

        # рисуем окошко, где будут показываться детальки
        pygame.draw.rect(screen, (255, 255, 255), (323, 8, 154, 154), 2)
        # к нему кнопку, которая должна пролистывать детальки, это спрайт
        # нет, блин, кола
        pygame.draw.rect(screen, PURPLE, (325, 170, 30, 30))
        # которая поворачивает детальку
        pygame.draw.rect(screen, BLUE, (370, 170, 30, 30))
        # кнопка, при нажатии на которую мы переходи в режим выставления детальки на поле
        pygame.draw.rect(screen, GREEN, (415, 170, 30, 30))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        elif self.check_button_rot(mouse_pos):
            self.rotate_tile()
            return 'rot'
        elif self.check_button_next(mouse_pos):
            self.do_next()
            return 'next'
        elif self.check_button_set(mouse_pos):
            self.waiting_for_position()

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or x > self.left + self.width * self.cell_size:
            # print(1)
            return None
        if y < self.top or y > self.top + self.height * self.cell_size:
            # print(2)
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

    def on_click(self, cell):
        global index, all_tiles
        print(cell)
        # если мы нажали на кнопку согласия на постановку тайла
        if self.condition:
            # если мы можем поставить тайл (проверяем при помощи метода класса квилтбоард)
            if self.qb1.check_tile(*cell, self.tiles_list[index].all_configurations):
                # закрашиваем
                self.qb1.place_tile(*cell, self.tiles_list[index].all_configurations)
                for y in range(len(self.qb1.board_list)):
                    for x in range(len(self.qb1.board_list[y])):
                        if self.qb1.board_list[y][x]:
                            self.add_filled_cell((x, y))
                self.condition = False
                self.tiles_list.pop(index)
                all_tiles.pop(index)
                index -= 1

    def rotate_tile(self):
        pass

    def do_next(self):
        pass

    def waiting_for_position(self):
        self.condition = True

    def add_filled_cell(self, cell):
        global filling_cells
        x, y = cell
        filled_cell = pygame.Rect(11 + x * 30, 11 + y * 30, 28, 28)
        self.filled_cells.append(filled_cell)
        filling_cells = True


class Player:
    def __init__(self, quiltboard):
        self.quiltboard = quiltboard
        self.bonus_7x7 = 0
        self.button_income = 0  # кол-во пуговиц на поле
        self.money = 5
        self.special_patches = 0 # кажется, их нужно сразу ставить
        self.timeline_position = 0

    def move(self, move_num):
        if self.timeline_position + move_num <= 53:
            self.timeline_position += move_num
        else:
            self.timeline_position = 53

    def has_new_buttons(self):
        pass

    def add_new_buttons(self):
        pass

    def has_new_special_patches(self):
        pass

    def add_new_special_patches(self):
        pass





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


tiles_list = [
    Tile(4, 2, 1, tile_1, ['tile_1.bmp', 'tile_1_rot90.bmp', 'tile_1_rot180.bmp', 'tile_1_rot270.bmp']),
    Tile(10, 3, 0, tile_2, ['tile_2.bmp', 'tile_2_rot90.bmp', 'tile_2_rot180.bmp', 'tile_2_rot270.bmp']),
    Tile(1, 3, 0, tile_3, ['tile_3.bmp', 'tile_3_rot90.bmp', 'tile_3_rot180.bmp', 'tile_3_rot270.bmp']),
    Tile(10, 5, 3, tile_4, ['tile_4.bmp', 'tile_4_rot90.bmp', 'tile_4_rot180.bmp', 'tile_4_rot270.bmp']),
    Tile(7, 1, 1, tile_5, ['tile_5.bmp', 'tile_5_rot90.bmp', 'tile_5_rot180.bmp', 'tile_5_rot270.bmp']),
    Tile(10, 3, 2, tile_6, ['tile_6.bmp', 'tile_6_rot90.bmp', 'tile_6_rot180.bmp', 'tile_6_rot270.bmp']),
    Tile(7, 2, 2, tile_7, ['tile_7.bmp', 'tile_7_rot90.bmp', 'tile_7_rot180.bmp', 'tile_7_rot270.bmp']),
    Tile(6, 5, 2, tile_8, ['tile_8.bmp', 'tile_8_rot90.bmp', 'tile_8_rot180.bmp', 'tile_8_rot270.bmp']),
    Tile(10, 4, 3, tile_9, ['tile_9.bmp', 'tile_9_rot90.bmp', 'tile_9_rot180.bmp', 'tile_9_rot270.bmp']),
    Tile(1, 4, 1, tile_10, ['tile_10.bmp', 'tile_10_rot90.bmp', 'tile_10_rot180.bmp', 'tile_10_rot270.bmp'])
]

if __name__ == '__main__':
    pygame.init()
    size = width, height = 700, 600
    screen = pygame.display.set_mode(size)

    qb1 = QuiltBoard()
    qb2 = QuiltBoard()

    player1 = Player(qb1)
    player2 = Player(qb2)

    qb_received_7x7 = None

    # создаём объект с лоскутным одеялом
    board = Board(BOARD_HEIGHT, BOARD_WIDTH, tiles_list, qb1, qb2)
    board.set_view(10, 10, 30)

    timeline = TimeLine(player1, player2)

    index = 0
    image_configuration = 0

    filling_cells = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                f = board.get_click(event.pos)
                if f == 'next':
                    index += 1
                if f == 'rot':
                    image_configuration += 1

        image_configuration %= CONFIG_NUM

        # Делаем кнопки
        all_sprites = pygame.sprite.Group()
        all_tiles = []
        for tile in tiles_list:
            # all_sprites.add(TilesSprites(tile.basic_configuration, tile.images[0]))
            all_tiles.append(
                TilesSprites(tile.all_configurations[image_configuration], tile.images[image_configuration]))

        if len(all_tiles) != 0:
            index %= len(all_tiles)

        screen.fill((0, 0, 0))
        board.render()
        if filling_cells:
            for cell in board.filled_cells:
                pygame.draw.rect(screen, GREEN, cell)
        if qb_received_7x7 is not None:
            bonus_x, bonus_y = qb_received_7x7.bonus_coords
            for y in range(7):
                for x in range(7):
                    pygame.draw.rect(screen, PURPLE,
                                     (11 + (x + bonus_x) * 30, 11 + (y + bonus_y) * 30, 28, 28))
        # нужно отрисовывать один тайл, а не все сразу
        screen.blit(all_tiles[index].image, all_tiles[index].rect)
        # all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()
