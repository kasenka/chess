import os
import random
# король - king
# ферзь - queen
# ладья - rook
# слон - bishop
# конь - kNight
# пешка - pawn


green = '\033[42m'
bold = '\033[1m'
red = '\033[0;37;41m'
blue = "\033[0;34m"
purple = "\033[0;35m"
end = '\033[0m'
negative = '\033[7m'


class Board:
    step_counter = 0
    move = 'White'

    def __init__(self):

        self.board = {
            8: ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            7: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            6: ['.', '.', '.', '.', '.', '.', '.', '.'],
            5: ['.', '.', '.', '.', '.', '.', '.', '.'],
            4: ['.', '.', '.', '.', '.', '.', '.', '.'],
            3: ['.', '.', '.', '.', '.', '.', '.', '.'],
            2: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            1: ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        }

    def print_board(self):
        print(blue + '  A B C D E F G H ' + end)
        for i in self.board:
            print(purple + str(i) + end, *self.board[i], purple + str(i) + end)
        print(blue + '  A B C D E F G H ' + end)

    def update(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def change_player(self):
        self.move = 'Black' if self.move == 'White' else 'White'

    move_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    low_upp = {'White': 'W', 'Black': 'b'}

    def take_move(self):
        check = input(Board.move + "'s turn ")

        while len(check) != 2 or (check[0] not in 'ABCDEFGH') or (check[1] not in '12345678'):
            print('Некорректный ввод координат')
            check = input('Введите координаты хода вида[A-H][1-8] ')

        point = self.board[int(check[1])][self.move_dict[check[0]]]
        while point == '.' or point.isupper() != self.low_upp[self.move].isupper():
            check = input('Выберите для хода клетку со своей фигурой ')
            while len(check) != 2 or (check[0] not in 'ABCDEFGH') or (check[1] not in '12345678'):
                print('Некорректный ввод координат')
                check = input('Введите координаты хода вида[A-H][1-8] ')
            break

        move = check

        self.y = self.move_dict[move[0]]  # int
        self.x = int(move[1])  # int
        self.figure = self.board[self.x][self.y]
        self.board[self.x][self.y] = negative + self.board[self.x][self.y] + end

        Board.update()
        Board.print_board()

        return self.x, self.y, self.figure

    def make_move(self, name, sp, x, y):
        coords = input('Your move ? ')

        self.x = int(coords[1])
        self.y = self.move_dict[coords[0]]

        while [self.x, self.y] not in sp:
            coords = input('Выберите 1 из возможных ходов ')
            self.x = int(coords[1])
            self.y = self.move_dict[coords[0]]

        self.board[self.x][self.y] = name
        self.board[x][y] = '.'

        Figure.uncolor_steps()
        Board.update()
        Board.print_board()


class Figure:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def stat_steps(self, sp):
        pos = [i for i in sp if str(i[0]) in '12345678' and str(i[1]) in '01234567' and
               (Board.board[i[0]][i[1]].isupper() != self.name.isupper() or not Board.board[i[0]][i[1]].isalpha())]
        return pos

    def moving_steps(self, sp):
        pos = []
        for j in sp:
            for i in j:
                if len(str(i[0])) == 1 and len(str(i[1])) == 1 and str(i[0]) in '12345678' and str(i[1]) in '01234567':
                    if not Board.board[i[0]][i[1]].isalpha():
                        pos.append(i)
                    else:
                        pos.append(i)
                        break
        pos = [i for i in pos if
               Board.board[i[0]][i[1]].isupper() != self.name.isupper() or not Board.board[i[0]][i[1]].isalpha()]
        return pos

    @staticmethod
    def danger_figures(figures):
        d = {(int(8 - i), j): val[j] for i, val in enumerate(Board.board.values())
             for j in range(len(val)) if val[j].isalpha() and Board.low_upp[Board.move].isupper() != val[j].isupper()}
        sp = []
        for key in d.keys():

            if d[key] in 'pP':
                Board.change_player()
                coords = figures[d[key].lower()](d[key], key[0], key[1]).possible_kill_st()
                Board.change_player()
            else:
                coords = figures[d[key].lower()](d[key], key[0], key[1]).possible_st()

            if coords:
                for i in coords:
                    if negative in Board.board[i[0]][i[1]]:
                        Board.board[i[0]][i[1]] = Board.board[i[0]][i[1]].replace(negative, '').replace(end, '')
                    if Board.board[i[0]][i[1]].isalpha():
                        sp.append(i)

        return sp

    @staticmethod
    def color_danger_figures(sp):
        f = 0
        for i in sp:
            Board.board[i[0]][i[1]] = Board.board[i[0]][i[1]].replace(negative, '').replace(end, '')
            if Board.board[i[0]][i[1]] in 'kK':
                f += 1
            Board.board[i[0]][i[1]] = red + Board.board[i[0]][i[1]] + end
        Board.update()
        Board.print_board()
        return f

    def color_steps(self, sp):
        for i in sp:
            Board.board[i[0]][i[1]] = green + Board.board[i[0]][i[1]] + end
        Board.update()
        Board.print_board()

    @staticmethod
    def uncolor_steps():
        for line in Board.board.keys():
            for i in range(len(Board.board[line])):
                Board.board[line][i] = Board.board[line][i].replace(green, '').replace(red, '').replace(end, '')
        Board.update()
        Board.print_board()


class Pawn(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.p_s = {'White': [[self.x + 1, self.y], [self.x + 2, self.y]] if self.x == 2 else [[self.x + 1, self.y]],
                    'Black': [[self.x - 1, self.y], [self.x - 2, self.y]] if self.x == 7 else [[self.x - 1, self.y]]}

        self.p_w_kill = [i for i in [[self.x + 1, self.y + 1], [self.x + 1, self.y - 1]] if str(i[1]) in '01234567']
        self.p_b_kill = [i for i in [[self.x - 1, self.y + 1], [self.x - 1, self.y - 1]] if str(i[1]) in '01234567']

        self.p_w_kill = [i for i in self.p_w_kill if
                         (Board.board.get(i[0]) is not None and Board.board.get(i[0])[i[1]] != '.'
                          and Board.board.get(i[0])[i[1]].isupper() != self.name.isupper())]
        self.p_b_kill = [i for i in self.p_b_kill if
                         (Board.board.get(i[0]) is not None and Board.board.get(i[0])[i[1]] != '.'
                          and Board.board.get(i[0])[i[1]].isupper() != self.name.isupper())]
        self.p_kill = {'White': self.p_w_kill, 'Black': self.p_b_kill}

    def color(self):
        Figure.color_steps(self, self.p_s[Board.move] + self.p_kill[Board.move])

    def possible_st(self):
        return self.p_s[Board.move] + self.p_kill[Board.move]

    def possible_kill_st(self):
        return self.p_kill[Board.move]


class King(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.k_s = [[self.x + 1, self.y], [self.x + 1, self.y + 1], [self.x + 1, self.y - 1], [self.x - 1, self.y],
                    [self.x - 1, self.y + 1], [self.x - 1, self.y - 1], [self.x, self.y + 1], [self.x, self.y - 1]]

    def color(self):
        Figure.color_steps(self, Figure.stat_steps(self, self.k_s))

    def possible_st(self):
        return Figure.stat_steps(self, self.k_s)


class Queen(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

        self.q_s = [
            [[self.x + i, self.y] for i in range(1, 8)],
            [[self.x - i, self.y] for i in range(1, 8)],
            [[self.x, self.y + i] for i in range(1, 8)],
            [[self.x, self.y - i] for i in range(1, 8)],
            [[self.x + i, self.y + i] for i in range(1, 8)],
            [[self.x + i, self.y - i] for i in range(1, 8)],
            [[self.x - i, self.y + i] for i in range(1, 8)],
            [[self.x - i, self.y - i] for i in range(1, 8)]]

    def color(self):
        Figure.color_steps(self, Figure.moving_steps(self, self.q_s))

    def possible_st(self):
        return Figure.moving_steps(self, self.q_s)


class Knight(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

        self.n_s = [
            [self.x + 1, self.y + 2],
            [self.x + 2, self.y + 1],
            [self.x + 2, self.y - 1],
            [self.x + 1, self.y - 2],
            [self.x - 1, self.y - 2],
            [self.x - 2, self.y - 1],
            [self.x - 2, self.y + 1],
            [self.x - 1, self.y + 2]]

    def color(self):
        Figure.color_steps(self, Figure.stat_steps(self, self.n_s))

    def possible_st(self):
        return Figure.stat_steps(self, self.n_s)


class Rook(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

        self.r_s = [
            [[self.x + i, self.y] for i in range(1, 8)],
            [[self.x - i, self.y] for i in range(1, 8)],
            [[self.x, self.y + i] for i in range(1, 8)],
            [[self.x, self.y - i] for i in range(1, 8)]]

    def color(self):
        Figure.color_steps(self, Figure.moving_steps(self, self.r_s))

    def possible_st(self):
        return Figure.moving_steps(self, self.r_s)


class Bishop(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

        self.b_s = [
            [[self.x + i, self.y + i] for i in range(1, 8)],
            [[self.x + i, self.y - i] for i in range(1, 8)],
            [[self.x - i, self.y + i] for i in range(1, 8)],
            [[self.x - i, self.y - i] for i in range(1, 8)]]

    def color(self):
        Figure.color_steps(self, Figure.moving_steps(self, self.b_s))

    def possible_st(self):
        return Figure.moving_steps(self, self.b_s)



figures = {'p': Pawn, 'r': Rook, 'n': Knight, 'b': Bishop, 'q': Queen, 'k': King}
Board = Board()

while True:
    Board.update()
    Board.print_board()

    x, y, figure = Board.take_move()
    step = figures[figure.lower()](figure, x, y)  # вызываем нужный класс фигуры

    step.color()

    sp = Figure.danger_figures(figures)
    f = Figure.color_danger_figures(sp)

    if f:
        print(red + '__CHECKMATE__' + end)

    Board.make_move(figure, step.possible_st(), x, y)

    Board.change_player()
