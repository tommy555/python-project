import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_EXIT, wrapper
from random import randint

# parameter
WIDTH = 35
HEIGHT = 20
MAX_X = WIDTH - 2
MAX_Y = HEIGHT - 2
SNAKE_LENGTH = 5
SNAKE_X = SNAKE_LENGTH + 1
SNAKE_Y = 3
TIMEOUT = 100

# key map
START_KEY = [83, 115] # 83 = S 115 = s
EXIT_KEY = 27
KEY_MAP = [KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_EXIT]
REV_KEY_MAP = {
    KEY_RIGHT: KEY_LEFT,
    KEY_LEFT: KEY_RIGHT,
    KEY_UP: KEY_DOWN,
    KEY_DOWN: KEY_UP
}

# Snake object
class Snake:

    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.window = window
        self.char = '0'
        self.point = 0
        self.direction = KEY_RIGHT
        self.body = []
        for i in range(1, SNAKE_LENGTH+1):
            self.body.append(Body(x-i, y))

        self.direction_map = {
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
        }
        

    def set_direct(self, direction):
        if direction != REV_KEY_MAP[self.direction]:
            self.direction = direction
    
    def update(self):
        last_body = self.body.pop()
        last_body.x = self.x
        last_body.y = self.y
        self.body.insert(0, last_body)
        self.direction_map[self.direction]()

    def render(self):
        self.window.addstr(self.y, self.x, self.char)
        for e in self.body:
            self.window.addstr(e.y, e.x, e.char)

    def update_stat(self):
        self.window.addstr(0, 2, "Points: {}".format(self.point)) # .addstr(y,x, items_to_print)
    
    def eat_food(self):
        self.point += 10
        self.body.append(Body(self.body[-1].x, self.body[-1].y))

    @property
    def is_collided(self):
        return any([(self.x, self.y)==(body.x, body.y ) for body in self.body])

    def move_left(self):
        self.x -= 1
        if self.x < 1:
            self.x = MAX_X

    def move_right(self):
        self.x += 1
        if self.x > MAX_X:
            self.x = 1

    def move_up(self):
        self.y -= 1
        if self.y < 1:
            self.y = MAX_Y

    def move_down(self):
        self.window.addstr(2,2, "Moving down")
        self.y += 1
        if self.y > MAX_Y:
            self.y = 1


class Body:

    def __init__(self, x, y, char='='):
        self.x = x
        self.y = y
        self.char = char

class Food:

    def __init__(self, window, char = '*'):
        self.window = window
        self.char = char
    
    def spawn(self):
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)
    
    def render(self):
        self.window.addstr(self.y, self.x, self.char, curses.A_BLINK)

# program start

# init curses object
curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

window = curses.newwin(HEIGHT, WIDTH, 0, 40)
window.keypad(True)
window.timeout(TIMEOUT)

snake = Snake(SNAKE_X, SNAKE_Y, window)

food = Food(window)
food.spawn()

def game():
    while True:
        window.clear() 
        window.border(0)
        snake.render()
        food.render()
        snake.update_stat()

        event = window.getch()

        if event == EXIT_KEY: # 27 = exit btn
            break
        
        if event in KEY_MAP:
            snake.set_direct(event)
        
        if (snake.x, snake.y) == (food.x, food.y): # eat the food if collided by head
            snake.eat_food()
            food.spawn()

        snake.update()
        if snake.is_collided:
            break

def print_info(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 0, "SNAKE GAME")
    stdscr.addstr(2, 0, "How to play:")
    stdscr.addstr(3, 0, "1) Eat all coins as you can")
    stdscr.addstr(4, 0, "2) Avoid eat yourself")
    stdscr.addstr(5, 0, "")
    stdscr.addstr(6, 0, "How to control:")
    stdscr.addstr(7, 0, "press 'Esc' to quit")
    stdscr.addstr(8, 0, "press arrow key to control snake")
    stdscr.addstr(9, 0, "")
    stdscr.addstr(10, 0, "")
    stdscr.addstr(11, 0, "press 'S' to start!!!")
    
    stdscr.refresh()
    
    key = 123
    while key not in START_KEY:
        key = stdscr.getch()
        if key == EXIT_KEY:
            exit()
    game()
    

if __name__ == "__main__":
    wrapper(print_info)

# end 
curses.endwin()    
if snake.is_collided: print("You lose")
print("Your point: {}".format(snake.point))
        

