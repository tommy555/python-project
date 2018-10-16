import curses
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from random import randint


# parameter

HEIGHT = 4 # game height
WIDTH = 4 # game width
GAME_FIELD = None
KEY_END = 27 # Esc
KEY_START = 265 # f1
KEY_RESTART = 266 # f2

# define object

class Block:

    def __init__(self, x, y, number = 0):
        self.x  = x
        self.y = y
        self.number = number

    def is_left_available(self, left):
        pass
    
    def is_right_available(self, right):
        pass
    
    def is_top_available(self, top):
        pass
    
    def is_btm_available(self, btm):
        pass

    @property
    def get_coor(self):
        return (self.x, self.y)

class BlockField:

    def __init__(self, screen):
        self.block_field = []
        self.screen = screen
    
    def add_block(self, block):
        self.block_field.append(block)
    
    def get_block(self, x, y):
        for e in self.block_field:
            if e.x == x and e.y == y:
                return e

    def is_available(self, x, y):
        block = self.get_block(x, y)
        if block.number == 0:
            return True

        return False
    
    def update_block(self, x, y, number):
        block = self.get_block(x, y)
        block.number = number
    
    def print_blocks(self):
        #self.screen.clear()
        text = ""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                block = self.get_block(x, y)
                if block.number == 0:
                    text += "_\t"
                else:
                    text += str(block.number) + "\t"
            text += "\n"
        
        self.screen.addstr(text)
        self.screen.refresh()

    @property
    def size(self):
        return len(self.block_field)
    
    @property
    def is_empty(self):
        return (self.size == 0)
    
    def make_movement(self, event):
        able_to_move = False
        target = []

        def merge_block(list):
            result = False

            def reset_block(): # r stand for result
                list[0].number = 0
                return True

            # function start here    
            while len(list) > 1:
                e = list.pop(0)
                if e.number == list[0].number: 
                    e.number = e.number * 2
                    result = reset_block()
                elif e.number == 0: 
                    e.number = list[0].number
                    result = reset_block()
                    

            return result

        if event == KEY_LEFT or event == KEY_RIGHT:
            for y in range (HEIGHT):
                for x in range (WIDTH):
                    target.append(self.get_block(x, y))
                
                if event == KEY_RIGHT:
                    target.reverse()
                
                if merge_block(target):
                    able_to_move = True
                
                target = []

        elif event == KEY_UP or event == KEY_DOWN:
            for x in range (WIDTH):
                for y in range (HEIGHT):
                    target.append(self.get_block(x, y))
                
                if event == KEY_DOWN:  
                    target.reverse() # reverse col for moving block
                if merge_block(target):
                    able_to_move = True
                
                target = []
        


        return able_to_move

# function

def init_game(field):
    # init the game
    for y in range(HEIGHT):
        for x in range(WIDTH):
            field.add_block(Block(x, y))
    
    # spawn 2 block: 2, and 4
    spawn_block(field, 2)
    spawn_block(field, 4)



def spawn_block(field, number, x = None, y = None):
    if x == None and y == None:
        done = False
        while not done:
            x = randint(0, WIDTH-1)
            y = randint(0, HEIGHT-1)
            done = field.is_available(x, y)
    
    field.update_block(x, y, number)


def restart_game(field):
    pass

# setup key map

KEY_STR = {
    KEY_UP: "move_up",
    KEY_DOWN: "move_down",
    KEY_LEFT: "move_left",
    KEY_RIGHT: "move_right",
    KEY_RESTART: "restart_game"
}

# setup curses
curses.initscr()
curses.curs_set(0)

def main(screen):
    fail_counter = 0
    last_field_mov = 0
    event = screen.getch()
    while event != KEY_START:
            event = screen.getch() # wait for user to press enter
            if event == KEY_END:
                return

    GAME_FIELD = BlockField(screen)
    init_game(GAME_FIELD)
    GAME_FIELD.print_blocks()
    screen.refresh()

    # start game
    while event != KEY_END:
        event = screen.getch() # wait for user input
        if event in KEY_STR:
            screen.clear()
            success = GAME_FIELD.make_movement (event)
            if success: # run function based on user key, refer to <KEY_MAP dict> -> line 138
                spawn_block(GAME_FIELD, 2)
                fail_counter = 0
            else:
                if last_field_mov != event:
                    fail_counter += 1
                last_field_mov = event
            GAME_FIELD.print_blocks()
            #screen.addstr("success: {}, movement make: {}\n".format(success,event))
        if fail_counter >= 4:
            break
    
    
# add main function to screen
curses.wrapper(main)