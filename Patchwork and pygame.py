import numpy
import pygame

BOARD_HEIGHT = 9
BOARD_WIDTH = 9
CONFIG_NUM = 4

BLUE = (74, 172, 214)
GREEN = (94, 148, 118)
PURPLE = (74, 55, 97)
RED = (123, 69, 90)
WHITE = (255, 255, 255)
YELLOW = (211, 146, 52)

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
tile_11 = numpy.array([  # 5 4 2
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])
tile_12 = numpy.array([  # 2 1 0
    [1, 1]
])
tile_13 = numpy.array([  # 7 4 2
    [0, 1, 1, 0],
    [1, 1, 1, 1]
])
tile_14 = numpy.array([  # 1 5 1
    [1, 1],
    [1, 0],
    [1, 0],
    [1, 1]
])
tile_15 = numpy.array([  # 1 2 0
    [1, 1],
    [1, 0],
    [1, 1]
])


class Button:
    def __init__(self, screen, x, y, length, width, color, text):
        self.x = x
        self.y = y
        self.screen = screen
        self.length = length
        self.width = width
        self.text = text
        self.color = color
        self.rect = pygame.Rect(x, y, length, width)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.length, self.width))
        font_size = int(self.length// len(self.text))
        myFont = pygame.font.SysFont("Courier New", font_size)
        myText = myFont.render(self.text, True, RED)
        self.screen.blit(myText, ((self.x + self.length / 2) - myText.get_width() / 2, (self.y + self.width / 2) - myText.get_height() / 2))

    def is_pressed(self, mouse):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1]:
                        return True
        return False


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


class QuiltBoard():
    def __init__(self, player, width, height, left, top, dif, cell_size):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.dif = dif
        self.cell_size = cell_size
        self.filled_cells = []
        self.board_list = numpy.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.bonus_coords = None
        self.player = player

    def render(self):
        x, y, s = self.left, self.top + self.dif, self.cell_size
        for i in self.board_list:
            for _ in i:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, s, s), 1)
                x += s
            x = self.left
            y += s

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        is_board2 = False
        if x < self.left or x > self.left + self.width * self.cell_size:
            # print(1)
            return None
        if y < self.top + self.dif or y > self.top + self.height * self.cell_size + self.dif:
            # print(2)
            return None
        x_num = (x - self.left) // self.cell_size
        y_num = (y - self.top - self.dif) // self.cell_size
        return (x_num, y_num)


    def check_7x7(self):
        for y in range(BOARD_HEIGHT - 7 + 1):
            for x in range(BOARD_WIDTH - 7 + 1):
                field_7x7 = numpy.ones((7, 7), dtype=int)
                if numpy.all(field_7x7 & self.board_list[y:y + 7, x:x + 7]):
                    self.bonus_coords = (x, y)
                    return True
        return False

    def add_filled_cell(self, cell):
        global filling_cells
        x, y = cell
        filled_cell = pygame.Rect(11 + x * 30, 11 + y * 30 + self.dif, 28, 28)
        self.filled_cells.append(filled_cell)
        filling_cells = True

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

    def place_tile(self, x, y, tile):
        '''
        перед вызовом метода нужно проверить, можно ли вставить тайл
        x и y - координаты верхнего левого угла
        '''
        global image_configuration, player_received_7x7, move_number
        for index_i, i in enumerate(tile.all_configurations[image_configuration]):
            for index_j, j in enumerate(i):
                self.board_list[y + index_i][x + index_j] += j
        player_latest_position = self.player.timeline_position
        self.player.move(move_num=tile.placing_time)
        self.player.use_money(value=tile.placing_price)
        self.player.increase_income(tile.button_income)
        move_number += 1

        nearest_button_position = None
        nearest_patch_position = None

        for btn in timeline.button_income_coords:
            if btn > player_latest_position:
                nearest_button_position = btn
                break

        for patch in timeline.special_patch_coords:
            if patch > player_latest_position:
                nearest_button_position = patch
                break

        if nearest_button_position:
            if self.player.is_money_increased(nearest_btn=nearest_button_position):
                self.player.add_money()

        if nearest_patch_position:
            if self.player.has_new_special_patches(nearest_patch=nearest_patch_position):
                pass  # не придумала я еще, что делать в этом случае

        if not player_received_7x7:
            if self.check_7x7():
                self.player.bonus_7x7 = True
                player_received_7x7 = self.player

    @property
    def empties_num(self):
        return BOARD_WIDTH * BOARD_HEIGHT - sum([sum(line) for line in self.board_list])


class Player:
    def __init__(self, token):
        self.bonus_7x7 = False
        self.button_income = 0  # кол-во пуговиц на поле
        self.money = 5
        self.special_patches = 0  # кажется, их нужно сразу ставить
        self.timeline_position = 0
        self.token = token

    def __repr__(self):
        return f'Player {self.token.number}'

    def move(self, move_num):
        if self.timeline_position + move_num <= 53:
            self.timeline_position += move_num
        else:
            self.timeline_position = 53

    def use_money(self, value):
        self.money -= value

    def add_money(self, value):
        self.money += value

    def is_money_increased(self, nearest_btn):
        return nearest_btn <= self.timeline_position

    def increase_income(self, value):
        self.button_income += value

    def has_new_special_patches(self, nearest_patch):
        return nearest_patch <= self.timeline_position


class TimeLine:
    def __init__(self):
        self.num_cells = 54
        self.button_income_coords = [5, 11, 17, 23, 29, 35, 41, 47, 53]
        self.special_patch_coords = [20, 26, 32, 44, 50]
        self.board = [] * 54
        # self.player1 = player1
        # self.player2 = player2
        self.cells_centers = [
            (347, 235), (392, 235), (437, 235), (482, 235), (527, 235), (572, 235), (617, 235),
            (662, 235), (662, 280), (662, 325), (662, 370), (662, 415), (662, 460), (662, 505),
            (662, 550), (617, 325), (572, 325), (527, 325), (482, 325), (437, 325), (392, 325),
            (347, 370), (392, 370), (437, 370), (482, 370), (527, 370), (347, 415),
            (392, 415), (437, 415), (482, 415), (347, 460), (392, 460),
            (437, 460), (347, 505), (392, 505)
        ]
        # аааааа блин, ничего не получается, здесь должны быть координаты центров, но они
        # тут не все и не правильные, но предположим, что они тут есть, я устала искать ошибки
        # в циферках, вообще люблю эту жизнь и тех, кто ставит 8 за проекты. Мне вот ЕГЭ сдавать,
        # а, оказывается, золотую медаль мне портит не русский, не физика, а проект 💕💕💕

    def is_game_finished(self):
        global player1, player2
        if player1.timeline_position == 53 and player2.timeline_position == 53:
            return True
        return False

    @property
    def who_moves(self):
        global player1, player2
        if player1.timeline_position > player2.timeline_position:
            return 2
        if player1.timeline_position < player2.timeline_position:
            return 1
        else:
            # возвращает первого игрока, добавленного в список определенной клетки поля
            # return self.board[self.player2.timeline_position][-1]

            # но здесь какая-то ошибка, так что пусть будет первый игрок
            return 1


class Board:
    def __init__(self, width, height, tiles_list, qb, btn_A, btn_B, timeline):
        self.width = width
        self.height = height
        self.left = 20
        self.top = 20
        self.cell_size = 50
        self.quiltboards = qb

        self.tiles_list = tiles_list  # список из объектов класса Tile
        self.condition = False  # отвечает за то, можно ли ставить тайл
        self.btn_A = btn_A
        self.btn_B = btn_B
        # хотелось бы, чтобы после того, как мы ставим детальку, больше мы не могли её достать
        # для этого нужно удалить её из списка, но нам всё равно нужен индекс. Проблема: индекс
        # индекс лежит не в классе, менять
        self.dif_index = 0

    def render(self):
        global index, player1, player2
        for qb in self.quiltboards:
            qb.render()

        # рисуем окошко, где будут показываться детальки
        pygame.draw.rect(screen, (255, 255, 255), (323, 8, 154, 154), 2)
        # к нему кнопку, которая должна пролистывать детальки, это спрайт
        # нет, блин, кола
        pygame.draw.rect(screen, PURPLE, (325, 170, 30, 30))
        # которая поворачивает детальку
        pygame.draw.rect(screen, BLUE, (445, 170, 30, 30))
        # окно с данными лоскутка
        pygame.draw.rect(screen, WHITE, (360, 170, 80, 30), 2)
        myFont = pygame.font.SysFont("Courier New", 14, bold=True)
        myText = myFont.render(
            f'П:{self.tiles_list[index].placing_price} В:{self.tiles_list[index].placing_time}',
            True, WHITE)
        screen.blit(myText, (365, 175))
        # окошки для игроков, у кого сколько пуговиц
        pygame.draw.rect(screen, (255, 255, 255), (490, 10, 95, 100), 2)
        myText = myFont.render(f'{player1.money} пуговиц', True, WHITE)
        screen.blit(myText, (495, 15))
        pygame.draw.rect(screen, (255, 255, 255), (585, 10, 95, 100), 2)
        myText = myFont.render(f'{player2.money} пуговиц', True, WHITE)
        screen.blit(myText, (590, 15))

        myText = myFont.render(f'Ход {timeline.who_moves}го игрока', True, WHITE)
        screen.blit(myText, (490, 120))

    def get_click(self, mouse_pos):
        cell1 = self.quiltboards[0].get_cell(mouse_pos)
        cell2 = self.quiltboards[1].get_cell(mouse_pos)
        if cell1:
            self.on_click(cell1, 1)
        elif cell2:
            self.on_click(cell2, 2)
        elif self.check_button_rot(mouse_pos):
            self.rotate_tile()
            return 'rot'
        elif self.check_button_next(mouse_pos):
            self.do_next()
            return 'next'
        elif self.btn_A.is_pressed(mouse_pos):
            print('передвинуться по таймлайну и получить пуговицы')
        elif self.btn_B.is_pressed(mouse_pos):
            print('потратить пуговицы и расположить лоскут')
            player = timeline.who_moves
            if player == 1:
                player1.move(self.tiles_list[index].placing_time)
                player1.token.rect.center = timeline.cells_centers[player1.timeline_position]
            else:
                player2.move(self.tiles_list[index].placing_time)
                player2.token.rect.center = timeline.cells_centers[player2.timeline_position]
            self.waiting_for_position()

    def check_button_rot(self, mouse_pos):
        x, y = mouse_pos
        if 325 <= x <= 355 and 170 <= y <= 200:
            print('rot')
            return True
        return False

    def check_button_next(self, mouse_pos):
        x, y = mouse_pos
        if 445 <= x <= 475 and 170 <= y <= 200:
            print('next')
            return True
        return False

    # def check_button_set(self, mouse_pos):
    #     x, y = mouse_pos
    #     if 415 <= x <= 445 and 170 <= y <= 200:
    #         print('set')
    #         return True
    #     return False

    def on_click(self, cell, qb_number):
        global index, all_tiles
        print(cell)
        # если мы нажали на кнопку согласия на постановку тайла
        if self.condition:
            # если мы можем поставить тайл (проверяем при помощи метода класса квилтбоард)
            if self.quiltboards[qb_number-1].check_tile(*cell, self.tiles_list[index].all_configurations):
                # закрашиваем
                self.quiltboards[qb_number-1].place_tile(*cell, self.tiles_list[index])
                for y in range(len(self.quiltboards[qb_number-1].board_list)):
                    for x in range(len(self.quiltboards[qb_number-1].board_list[y])):
                        if self.quiltboards[qb_number-1].board_list[y][x]:
                            self.quiltboards[qb_number-1].add_filled_cell((x, y))
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


class TimelineSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load('TimeLine.bmp').convert()
        self.image = player_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (505, 405)
        self.pos = (347, 245)  # центр первой клетки таймлайна


class TimeToken(pygame.sprite.Sprite):
    '''создаём спрайты для жетонов'''
    def __init__(self, path, number):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(path).convert()
        self.image = player_img
        self.number = number
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (350, 235 + (number - 1) * 20)


# special_patch_code = numpy.array([1])
# special_patch = Tile(0, 0, 0, special_patch_code, #тут должна быть картинка)

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
    Tile(1, 4, 1, tile_10, ['tile_10.bmp', 'tile_10_rot90.bmp', 'tile_10_rot180.bmp', 'tile_10_rot270.bmp']),
    Tile(5, 4, 2, tile_11, ['tile_11.bmp', 'tile_11_rot90.bmp', 'tile_11_rot180.bmp', 'tile_11_rot270.bmp']),
    Tile(2, 1, 0, tile_12, ['tile_12.bmp', 'tile_12_rot90.bmp', 'tile_12_rot180.bmp', 'tile_12_rot270.bmp']),
    Tile(7, 4, 2, tile_13, ['tile_13.bmp', 'tile_13_rot90.bmp', 'tile_13_rot180.bmp', 'tile_13_rot270.bmp']),
    Tile(1, 5, 1, tile_14, ['tile_14.bmp', 'tile_14_rot90.bmp', 'tile_14_rot180.bmp', 'tile_14_rot270.bmp']),
    Tile(1, 2, 0, tile_15, ['tile_15.bmp', 'tile_15_rot90.bmp', 'tile_15_rot180.bmp', 'tile_15_rot270.bmp'])
]

if __name__ == '__main__':
    pygame.init()
    size = width, height = 700, 600
    screen = pygame.display.set_mode(size)

    token1 = TimeToken('жетон 1.bmp', 1)
    token2 = TimeToken('жетон 2.bmp', 2)
    tokens_sprites_list = pygame.sprite.Group()
    tokens_sprites_list.add(token1)
    tokens_sprites_list.add(token2)

    player1 = Player(token1)
    player2 = Player(token2)

    btn_A = Button(screen, 490, 170, 30, 30, YELLOW, 'A')
    btn_B = Button(screen, 530, 170, 30, 30, YELLOW, 'B')

    qb1 = QuiltBoard(player1, width=BOARD_WIDTH, height=BOARD_HEIGHT, left=10, top=10, cell_size=30, dif=0)
    qb2 = QuiltBoard(player2, width=BOARD_WIDTH, height=BOARD_HEIGHT, left=10, top=10, cell_size=30, dif=300)

    timeline = TimeLine()

    board = Board(BOARD_HEIGHT, BOARD_WIDTH, tiles_list, [qb1, qb2], btn_A, btn_B, timeline)

    player_received_7x7 = None
    move_number = 0

    # создаём объект с лоскутным одеялом
    # board_1 = Board(BOARD_HEIGHT, BOARD_WIDTH, tiles_list, qb1, 0)
    # board_1.set_view(10, 10, 30)
    # board_2 = Board(BOARD_HEIGHT, BOARD_WIDTH, tiles_list, qb2, 300)
    # board_2.set_view(10, 10, 30)

    index = 0
    image_configuration = 0

    filling_cells = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                f1 = board.get_click(event.pos)
                if f1 == 'next':
                    index += 1
                if f1 == 'rot':
                    image_configuration += 1

        image_configuration %= CONFIG_NUM

        # Делаем кнопки
        timeline_sprite = TimelineSprite()
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
        btn_A.draw()
        btn_B.draw()
        if filling_cells:
            for cell in qb1.filled_cells:
                pygame.draw.rect(screen, GREEN, cell)
            for cell in qb2.filled_cells:
                pygame.draw.rect(screen, GREEN, cell)
        if player_received_7x7 is not None:
            bonus_x, bonus_y = player_received_7x7.bonus_coords
            for y in range(7):
                for x in range(7):
                    pygame.draw.rect(screen, PURPLE,
                                     (11 + (x + bonus_x) * 30, 11 + (y + bonus_y) * 30, 28, 28))
        # нужно отрисовывать один тайл, а не все сразу
        screen.blit(all_tiles[index].image, all_tiles[index].rect)
        screen.blit(timeline_sprite.image, timeline_sprite.rect)
        # screen.blit(token2.image, timeline_sprite.rect)
        # screen.blit(token1.image, timeline_sprite.rect)
        tokens_sprites_list.draw(screen)

        # all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()
