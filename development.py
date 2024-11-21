import easygui
import src.Globals as Globals
import src.hash_func as hf
import keyboard
import pygame
import random
import src.show_func as shf
import src.stat_func as stf
import src.supp_func as sf
import time


def choose_level_num(chosen_list):
    """Gives user ability to choose level and start game"""
    sf.fill_gradient()
    while 1:
        shf.esc_to_end_show()
        shf.level_num_show()
        pygame.time.wait(200)
        rk = keyboard.read_key()
        if rk.isnumeric() and Globals.Globals.THE_FIRST_LEVEL <= int(rk) <= Globals.Globals.THE_LAST_LEVEL:
            Globals.Globals.screen.blit(Globals.Globals.img, (0, 0))
            pygame.display.update()
            random_list = random.choices(chosen_list[int(rk)], k=Globals.Globals.LEN_STRING)
            random_string = "".join(random_list)
            start_game(random_string)
            break
        elif rk == "esc":
            break
        else:
            sf.no_option()


def level_type(rktype):
    """Returns chosen level_type"""
    if rktype == "f":
        return Globals.Globals.Junior_levels
    elif rktype == "s":
        return Globals.Globals.Middle_levels
    elif rktype == "t":
        return Globals.Globals.Senior_levels
    elif rktype == "d":
        return Globals.Globals.Developer_levels
    else:
        return 0


def choose_level_type():
    """Gives User to choose difficulty and call choose_level_num()"""
    sf.fill_gradient()
    while 1:
        shf.esc_to_end_show()
        shf.type_level_show()
        pygame.time.wait(400)
        rktype = keyboard.read_key()
        chosen_list = level_type(rktype)
        if chosen_list != 0:
            choose_level_num(chosen_list)
            break
        elif rktype == "esc":
            break
        else:
            sf.no_option()

def update_next_iter(start_time, lci, mistakes, correct_string):
    Globals.Globals.screen.blit(Globals.Globals.img, (0, 0))
    shf.correct_string_show(correct_string, lci)
    shf.online_stat_show(start_time, lci, mistakes)
    pygame.time.wait(150)


def show_end_stat(start_time, lci, mistakes):
    Globals.Globals.screen.blit(Globals.Globals.img, (0, 0))
    pygame.display.update()
    shf.online_stat_show(start_time, lci, mistakes)
    pygame.time.wait(500)


def process_update_stat(start_time, lci, mistakes):
    online_delta = time.time() - start_time
    speed = sf.to_fixed(lci * 60 / online_delta, 1)
    stf.stat_append(speed, mistakes)


def process_else_variant(mistakes, lci, correct_string ):
    mistakes += 1
    shf.cat_show()
    pygame.time.wait(100)
    cs = correct_string[lci]
    if cs == " " or cs == "_":
        cs = "space"
    hf.hash_append(cs)
    return mistakes, lci-1

def update_show_end_stat(start_time, lci, mistakes):
    process_update_stat(start_time, lci, mistakes)
    show_end_stat(start_time, lci, mistakes)


def start_game(correct_string):
    """Starts game with correct_string"""
    mistakes, lci, start_time = 0, 0, time.time() # len_correct_input
    shf.esc_to_end_show()
    shf.correct_string_show(correct_string, lci)
    while lci < len(correct_string):
        update_next_iter(start_time, lci, mistakes, correct_string)
        rk = keyboard.read_key()
        if rk == correct_string[lci]:
            shf.correct_string_show(correct_string, lci)
        elif rk == "shift":
            continue
        elif rk == "space" and correct_string[lci] == "_":
            sf.space_underline(correct_string, lci)
        elif rk == "esc":
            return 1
        else:
            mistakes, lci = process_else_variant(mistakes, lci, correct_string )
        lci += 1
    update_show_end_stat(start_time, lci, mistakes)





def load_file():
    """Loading file from openbox"""
    count_read_in_file = 30
    input_file = easygui.fileopenbox(filetypes=["*.docx"])
    if not input_file:
        return 0
    file = open(input_file, 'r')
    res = 0
    while 1:
        line = file.read(count_read_in_file)
        if not line or res:
            break
        new_line = sf.change_space_on_underline(line)
        res = start_game(new_line)
        cover_rect = (Globals.Globals.COORD_OF_STRING[0],
                      Globals.Globals.COORD_OF_STRING[1], count_read_in_file * 50, 80)
        pygame.draw.rect(Globals.Globals.screen, Globals.Globals.COLOUR_SCREEN_FILL, cover_rect)
        pygame.display.update()


class Menu:
    """Menu """
    def __init__(self):
        """Initializes Menu options, callbacks, current_option"""
        self._options = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        """Appends option"""
        self._options.append(Globals.Globals.ARIAL_90.render(option, True, Globals.Globals.COLOUR_OF_MENU_TEXT))
        self._callbacks.append(callback)

    def switch(self, direction):
        """Chooses option which is available"""
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        """Select current option"""
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        """Draws options of Menu starting from point with x and y coordinates"""
        for i, option in enumerate(self._options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, Globals.Globals.COLOUR_OF_MENU_RECTANGLE, option_rect, 3)
            surf.blit(option, option_rect)


# RUNNING = True
def quit_game():
    """Quite game"""
    Globals.Globals.RUNNING = False


def menu_create():
    """Creates menu"""
    menu = Menu()
    menu.append_option("Choose_Level", choose_level_type)
    menu.append_option('Load_File', load_file)
    menu.append_option('Statistics', shf.stat_show)
    menu.append_option('Hash', shf.hash_show)
    menu.append_option('Help', shf.help_show)
    menu.append_option('Quit', quit_game)
    return menu


def processing_keydown(e, menu):
    """Processing keydown"""
    if e.key == pygame.K_UP:
        menu.switch(-1)
    elif e.key == pygame.K_DOWN:
        menu.switch(1)
    elif e.key == pygame.K_RETURN:
        menu.select()


def main():
    """Processing Keyboard"""
    menu = menu_create()
    FPS = 100
    clock = pygame.time.Clock()
    while Globals.Globals.RUNNING:
        menu_x = Globals.Globals.size[0] // 2 - 200
        menu_y = 50
        len_between_options = 125
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                processing_keydown(e, menu)

        clock.tick(FPS)
        Globals.Globals.screen.blit(Globals.Globals.img, (0, 0))
        menu.draw(Globals.Globals.screen, menu_x, menu_y, len_between_options)
        pygame.display.flip()


main()
