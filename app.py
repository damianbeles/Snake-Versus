import json
import PIL.Image
import pygame
import os
import threading

from datetime import datetime
from PIL import ImageTk
from tkinter import *
from tkinter.colorchooser import *
from tkinter.font import *

from player import Player
from utils import *

import algorithms


class App(Tk):

    WIDTH = 300
    HEIGHT = 450

    def __init__(self):
        super().__init__()
        self.withdraw()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.title('Snake Versus')
        self.iconbitmap(r'./resources/snake.ico')
        self.geometry(f'{App.WIDTH}x{App.HEIGHT}+{int(screen_width / 2 - App.WIDTH / 2)}+{int(screen_height / 2 - App.HEIGHT / 2)}')
        self.resizable(False, False)

        self.display_image = ImageTk.PhotoImage(file=r"./resources/display_settings.png")
        self.display_settings_button = Button(self, image=self.display_image, command=self.on_display_settings_click)
        self.display_settings_button.pack()
        self.display_settings_button.place(x=App.WIDTH - 42, y=App.HEIGHT - 42)

        self.user_image = ImageTk.PhotoImage(file=r"./resources/user_settings.png")
        self.user_settings_button = Button(self, image=self.user_image, command=self.on_user_settings_click)
        self.user_settings_button.pack()
        self.user_settings_button.place(x=4, y=App.HEIGHT - 42)

        self.play_button = Button(self, text="PLAY", font=Font(family="Georgia", size=14), command=self.on_play_click)
        self.play_button.pack()
        off_x = self.play_button.winfo_reqwidth() / 2
        off_y = self.play_button.winfo_reqheight() / 2
        self.play_button.place(relx=0.5, x=-int(off_x), rely=0.5, y=-int(off_y))

        self.deiconify()

    def hide(self):
        self.update()
        self.withdraw()

    def show_at_position(self, x, y):
        self.geometry(f'+{x}+{y}')
        self.update()
        self.deiconify()

    def on_display_settings_click(self):
        self.hide()
        settings = DisplaySettings(self, self.winfo_x(), self.winfo_y())
        settings.wait_window()
        self.show_at_position(DisplaySettings.LAST_X, DisplaySettings.LAST_Y)

    def on_user_settings_click(self):
        self.hide()
        settings = UserSettings(self, self.winfo_x(), self.winfo_y())
        settings.wait_window()
        self.show_at_position(UserSettings.LAST_X, UserSettings.LAST_Y)

    def on_play_click(self):
        self.hide()
        game = Game(self)
        game.wait_window()
        self.deiconify()


class Game(Toplevel):

    def init_game_window(self):
        game_window = pygame.display.set_mode([Dimension.SCREEN_WIDTH,
                                            Dimension.SCREEN_HEIGHT])
        game_window.fill(pygame.Color('white'))

        pygame.draw.rect(game_window,
                        pygame.Color('black'),
                        [Dimension.FIRST_BOARD_TOP_LEFT_X - 2,
                        Dimension.FIRST_BOARD_TOP_LEFT_Y - 2,
                        Dimension.BOARD_WIDTH + 1,
                        Dimension.BOARD_HEIGHT + 1],
                        True)

        pygame.draw.rect(game_window,
                        pygame.Color('black'),
                        [Dimension.SECOND_BOARD_TOP_LEFT_X - 2,
                        Dimension.SECOND_BOARD_TOP_LEFT_Y - 2,
                        Dimension.BOARD_WIDTH + 1,
                        Dimension.BOARD_HEIGHT + 1],
                        True)

        return game_window

    def play_new_game(self, players):
        players[0].play()
        players[1].play()

        players[0].set_enemy(players[1])
        players[1].set_enemy(players[0])

    def generate_report_entry(self, players):
        with open(self.REPORT_FILE_NAME, 'a') as fout:
            if players[0].get_score() > players[1].get_score():
                winner = "first"
            elif players[0].get_score() == players[1].get_score():
                winner = "tie"
            else:
                winner = "second"
            fout.write(f"\n{players[0].get_score()},{players[1].get_score()},{winner}")

    def __init__(self, parent):
        super().__init__(parent)
        self.withdraw()

        algorithmsMap = {'Human': algorithms.Human,
                         'Greedy Choosing': algorithms.GreedyChoosing,
                         'Lee\'s Algorithm': algorithms.Lee,
                         'Deep Q Learning': algorithms.DQN}

        FIRST_PLAYER_ALGORITHM = algorithmsMap[settings_json["first_player"]["algorithm"]]
        SECOND_PLAYER_ALGORITHM = algorithmsMap[settings_json["second_player"]["algorithm"]]

        self.REPORT_FILE_NAME = f"reports/{datetime.now():%d_%m_%Y___%H_%M_%S}.csv"
        first = FIRST_PLAYER_ALGORITHM.__name__
        second = SECOND_PLAYER_ALGORITHM.__name__
        if first == 'Human':
            first = settings_json["first_player"]["name"]
        if second == 'Human':
            second = settings_json["second_player"]["name"]
        with open(self.REPORT_FILE_NAME, 'w') as fout:
            fout.write(f"{first},{second},Winner")

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_icon(pygame.image.load(r'./resources/snake.ico'))
        pygame.display.set_caption('Snake Versus')

        players = [Player(Dimension.FIRST_BOARD_TOP_LEFT_X,
                          Dimension.FIRST_BOARD_TOP_LEFT_Y,
                          FIRST_PLAYER_ALGORITHM(), 0),
                   Player(Dimension.SECOND_BOARD_TOP_LEFT_X,
                          Dimension.SECOND_BOARD_TOP_LEFT_Y,
                          SECOND_PLAYER_ALGORITHM(), 1)]

        self.play_new_game(players)

        game_window = self.init_game_window()

        pygame.time.set_timer(CustomEvent.FIRST_PLAYER_MOVE_EVENT,
                              CustomEvent.FIRST_PLAYER_MOVE_EVENT_TIMER)
        pygame.time.set_timer(CustomEvent.SECOND_PLAYER_MOVE_EVENT,
                              CustomEvent.SECOND_PLAYER_MOVE_EVENT_TIMER)

        running = True
        while running:
            for player in players:
                player.draw_on_display(game_window)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.play_new_game(players)

                    if event.key in Player.KEYS.keys():
                        if Player.KEYS[event.key] in settings_json["first_player"]["controls"]:
                            CustomEvent.FIRST_PLAYER_LAST_PRESSED_KEY = event.key

                        if Player.KEYS[event.key] in settings_json["second_player"]["controls"]:
                            CustomEvent.SECOND_PLAYER_LAST_PRESSED_KEY = event.key

                if event.type == CustomEvent.FIRST_PLAYER_MOVE_EVENT:
                    players[0].move()

                if event.type == CustomEvent.SECOND_PLAYER_MOVE_EVENT:
                    players[1].move()

            if players[0].is_dead() and\
               players[1].is_dead():
                self.generate_report_entry(players)

                self.play_new_game(players)

        players[0].save()
        players[1].save()
        pygame.quit()

        threading.Thread(target=self.close, args=[]).start()

    def close(self):
        self.destroy()


class FOptionMenu(OptionMenu):
    def __init__(self, tk, text, font, *options):
        self.var = StringVar()
        self.var.set(text)
        OptionMenu.__init__(self, tk, self.var, *options)
        self.config(font=font)
        self.config(width=1)
        self['menu'].config(font=font)

class UserSettings(Toplevel):

    LAST_X = 0
    LAST_Y = 0
    POSSIBLE_KEYS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '→', '←', '↑', '↓']

    AVAILABLE_ALGORITHMS = ["Greedy Choosing", "Lee's Algorithm", "Deep Q Learning", "Human"]

    def __init__(self, parent, x, y):
        super().__init__(parent)
        self.withdraw()

        self.title('User Settings')
        self.iconbitmap('./resources/snake.ico')
        self.geometry(f'{App.WIDTH}x{App.HEIGHT}+{x}+{y}')
        self.resizable(False, False)
        self.canvas = Canvas(self)

        self.first_player_name_label = Label(self, text="First Player Name", font=Font(family="Georgia", size=14))
        self.first_player_name_label.pack()
        off_x = self.first_player_name_label.winfo_reqwidth() / 2
        off_y = self.first_player_name_label.winfo_reqheight()
        self.first_player_name_label.place(relx=0.5, x=-int(off_x), y=5)

        self.fpn_text = StringVar()
        self.fpn_entry = Entry(self, textvariable=self.fpn_text, font=Font(family="Georgia", size=14), width=24, justify='center')
        self.fpn_entry.pack()
        self.fpn_text.set(f'{settings_json["first_player"]["name"]}')
        off_x = self.fpn_entry.winfo_reqwidth() / 2
        self.fpn_entry.place(relx=0.5, x=-int(off_x), y=1 * int(off_y) + 2 * 5)

        self.second_player_name_label = Label(self, text="Second Player Name", font=Font(family="Georgia", size=14))
        self.second_player_name_label.pack()
        off_x = self.second_player_name_label.winfo_reqwidth() / 2
        off_y = self.second_player_name_label.winfo_reqheight()
        self.second_player_name_label.place(relx=0.5, x=-int(off_x), y=2 * int(off_y) + 3 * 5)

        self.spn_text = StringVar()
        self.spn_entry = Entry(self, textvariable=self.spn_text, font=Font(family="Georgia", size=14), width=24, justify='center')
        self.spn_entry.pack()
        self.spn_text.set(f'{settings_json["second_player"]["name"]}')
        off_x = self.spn_entry.winfo_reqwidth() / 2
        self.spn_entry.place(relx=0.5, x=-int(off_x), y=3 * int(off_y) + 4 * 5)

        self.first_player_controls_label = Label(self, text="First Player Controls", font=Font(family="Georgia", size=14))
        self.first_player_controls_label.pack()
        off_x = self.first_player_controls_label.winfo_reqwidth() / 2
        self.first_player_controls_label.place(relx=0.5, x=-int(off_x), y=4 * int(off_y) + 5 * 5)

        self.fp_n = FOptionMenu(self, settings_json["first_player"]["controls"][3], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.fp_n.pack()
        off_x = self.fp_n.winfo_reqwidth() / 2
        self.fp_n.place(relx=0.20, x=-int(off_x), y=5 * int(off_y) + 6 * 5)

        self.fp_w = FOptionMenu(self, settings_json["first_player"]["controls"][0], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.fp_w.pack()
        off_x = self.fp_w.winfo_reqwidth() / 2
        self.fp_w.place(relx=0.40, x=-int(off_x), y=5 * int(off_y) + 6 * 5)

        self.fp_s = FOptionMenu(self, settings_json["first_player"]["controls"][1], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.fp_s.pack()
        off_x = self.fp_s.winfo_reqwidth() / 2
        self.fp_s.place(relx=0.60, x=-int(off_x), y=5 * int(off_y) + 6 * 5)

        self.fp_e = FOptionMenu(self, settings_json["first_player"]["controls"][2], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.fp_e.pack()
        off_x = self.fp_e.winfo_reqwidth() / 2
        self.fp_e.place(relx=0.80, x=-int(off_x), y=5 * int(off_y) + 6 * 5)

        self.first_player_controls_label = Label(self, text="Second Player Controls", font=Font(family="Georgia", size=14))
        self.first_player_controls_label.pack()
        off_x = self.first_player_controls_label.winfo_reqwidth() / 2
        self.first_player_controls_label.place(relx=0.5, x=-int(off_x), y=6 * int(off_y) + 8 * 5)

        self.sp_n = FOptionMenu(self, settings_json["second_player"]["controls"][3], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.sp_n.pack()
        off_x = self.sp_n.winfo_reqwidth() / 2
        self.sp_n.place(relx=0.20, x=-int(off_x), y=7 * int(off_y) + 9 * 5)

        self.sp_w = FOptionMenu(self, settings_json["second_player"]["controls"][0], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.sp_w.pack()
        off_x = self.sp_w.winfo_reqwidth() / 2
        self.sp_w.place(relx=0.40, x=-int(off_x), y=7 * int(off_y) + 9 * 5)

        self.sp_s = FOptionMenu(self, settings_json["second_player"]["controls"][1], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.sp_s.pack()
        off_x = self.sp_s.winfo_reqwidth() / 2
        self.sp_s.place(relx=0.60, x=-int(off_x), y=7 * int(off_y) + 9 * 5)

        self.sp_e = FOptionMenu(self, settings_json["second_player"]["controls"][2], Font(family="Georgia", size=14), *UserSettings.POSSIBLE_KEYS)
        self.sp_e.pack()
        off_x = self.sp_e.winfo_reqwidth() / 2
        self.sp_e.place(relx=0.80, x=-int(off_x), y=7 * int(off_y) + 9 * 5)

        self.algo_label = Label(self, text="Algorithms", font=Font(family="Georgia", size=14))
        self.algo_label.pack()
        off_x = self.algo_label.winfo_reqwidth() / 2
        self.algo_label.place(relx=0.5, x=-int(off_x), y=8 * int(off_y) + 11 * 5)

        self.fa = FOptionMenu(self, settings_json["first_player"]["algorithm"], Font(family="Georgia", size=14), *UserSettings.AVAILABLE_ALGORITHMS)
        self.fa.config(width=20)
        self.fa.pack()
        off_x = self.fa.winfo_reqwidth() / 2
        self.fa.place(relx=0.50, x=-int(off_x), y=9 * int(off_y) + 12 * 5)

        self.sa = FOptionMenu(self, settings_json["second_player"]["algorithm"], Font(family="Georgia", size=14), *UserSettings.AVAILABLE_ALGORITHMS)
        self.sa.config(width=20)
        self.sa.pack()
        off_x = self.sa.winfo_reqwidth() / 2
        self.sa.place(relx=0.50, x=-int(off_x), y=10 * int(off_y) + 14 * 5)

        self.save_button = Button(self, text="SAVE", command=self._on_save_click, font=Font(family="Georgia", size=14))
        self.save_button.pack()
        off_x = self.save_button.winfo_reqwidth() / 2
        self.save_button.place(relx=0.5, x=-int(off_x), y=11 * int(off_y) + 17 * 5)

        self.protocol('WM_DELETE_WINDOW', self.close)
        self.deiconify()

    def _on_save_click(self):
        settings_json["first_player"]["name"] = self.fpn_text.get()
        settings_json["first_player"]["controls"][3] = self.fp_n.var.get()
        settings_json["first_player"]["controls"][0] = self.fp_w.var.get()
        settings_json["first_player"]["controls"][1] = self.fp_s.var.get()
        settings_json["first_player"]["controls"][2] = self.fp_e.var.get()
        settings_json["first_player"]["algorithm"] = self.fa.var.get()

        settings_json["second_player"]["name"] = self.spn_text.get()
        settings_json["second_player"]["controls"][3] = self.sp_n.var.get()
        settings_json["second_player"]["controls"][0] = self.sp_w.var.get()
        settings_json["second_player"]["controls"][1] = self.sp_s.var.get()
        settings_json["second_player"]["controls"][2] = self.sp_e.var.get()
        settings_json["second_player"]["algorithm"] = self.sa.var.get()

        with open('settings.json', 'w') as outfile:
            json.dump(settings_json, outfile, indent=4)

        self.close()

    def close(self):
        UserSettings.LAST_X = self.winfo_x()
        UserSettings.LAST_Y = self.winfo_y()
        self.destroy()


class DisplaySettings(Toplevel):

    LAST_X = 0
    LAST_Y = 0

    def __init__(self, parent, x, y):
        super().__init__(parent)
        self.withdraw()

        self.title('Display Settings')
        self.iconbitmap('./resources/snake.ico')
        self.geometry(f'{App.WIDTH}x{App.HEIGHT}+{x}+{y}')
        self.resizable(False, False)
        self.canvas = Canvas(self)

        self.first_player_color_label = Label(self, text="First Player Skin", font=Font(family="Georgia", size=14))
        self.first_player_color_label.pack()
        off_x = self.first_player_color_label.winfo_reqwidth() / 2
        off_y = self.first_player_color_label.winfo_reqheight()
        self.first_player_color_label.place(relx=0.5, x=-int(off_x), y=5)

        fp_wr_x = 56
        fp_wr_y = 10 + int(off_y)
        self.fp_wr = self.canvas.create_rectangle(fp_wr_x, fp_wr_y, fp_wr_x + 36, fp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["first_player"]["skin"]["WALL"]),
                                     tags="fp_wr")
        self.canvas.tag_bind("fp_wr",
                             "<Button-1>",
                             lambda event, item=self.fp_wr: self._on_color_clicked(item))
        self.fp_hr = self.canvas.create_rectangle(fp_wr_x + 35 * 1 + 16 * 1, fp_wr_y, fp_wr_x + 36 + 35 * 1 + 16 * 1, fp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["first_player"]["skin"]["HEAD"]),
                                     tags="fp_hr")
        self.canvas.tag_bind("fp_hr",
                             "<Button-1>",
                             lambda event, item=self.fp_hr: self._on_color_clicked(item))
        self.fp_tr = self.canvas.create_rectangle(fp_wr_x + 35 * 2 + 16 * 2, fp_wr_y, fp_wr_x + 36 + 35 * 2 + 16 * 2, fp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["first_player"]["skin"]["TAIL"]),
                                     tags="fp_tr")
        self.canvas.tag_bind("fp_tr",
                             "<Button-1>",
                             lambda event, item=self.fp_tr: self._on_color_clicked(item))
        self.fp_fr = self.canvas.create_rectangle(fp_wr_x + 35 * 3 + 16 * 3, fp_wr_y, fp_wr_x + 36 + 35 * 3 + 16 * 3, fp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["first_player"]["skin"]["FOOD"]),
                                     tags="fp_fr")
        self.canvas.tag_bind("fp_fr",
                             "<Button-1>",
                             lambda event, item=self.fp_fr: self._on_color_clicked(item))

        self.second_player_color_label = Label(self, text="Second Player Skin", font=Font(family="Georgia", size=14))
        self.second_player_color_label.pack()
        off_x = self.second_player_color_label.winfo_reqwidth() / 2
        self.second_player_color_label.place(relx=0.5, x=-int(off_x), y=int(off_y) + 50)

        sp_wr_x = 56
        sp_wr_y = 55 + int(off_y) * 2
        self.sp_wr = self.canvas.create_rectangle(sp_wr_x, sp_wr_y, sp_wr_x + 36, sp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["second_player"]["skin"]["WALL"]),
                                     tags="sp_wr")
        self.canvas.tag_bind("sp_wr",
                             "<Button-1>",
                             lambda event, item=self.sp_wr: self._on_color_clicked(item))
        self.sp_hr = self.canvas.create_rectangle(sp_wr_x + 35 * 1 + 16 * 1, sp_wr_y, sp_wr_x + 36 + 35 * 1 + 16 * 1, sp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["second_player"]["skin"]["HEAD"]),
                                     tags="sp_hr")
        self.canvas.tag_bind("sp_hr",
                             "<Button-1>",
                             lambda event, item=self.sp_hr: self._on_color_clicked(item))
        self.sp_tr = self.canvas.create_rectangle(sp_wr_x + 35 * 2 + 16 * 2, sp_wr_y, sp_wr_x + 36 + 35 * 2 + 16 * 2, sp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["second_player"]["skin"]["TAIL"]),
                                     tags="sp_tr")
        self.canvas.tag_bind("sp_tr",
                             "<Button-1>",
                             lambda event, item=self.sp_tr: self._on_color_clicked(item))
        self.sp_fr = self.canvas.create_rectangle(sp_wr_x + 35 * 3 + 16 * 3, sp_wr_y, sp_wr_x + 36 + 35 * 3 + 16 * 3, sp_wr_y + 36,
                                     fill=rgb_to_hex_color(settings_json["second_player"]["skin"]["FOOD"]),
                                     tags="sp_fr")
        self.canvas.tag_bind("sp_fr",
                             "<Button-1>",
                             lambda event, item=self.sp_fr: self._on_color_clicked(item))

        self.entity_label = Label(self, text="Entity", font=Font(family="Georgia", size=14))
        self.entity_label.pack()
        off_x = self.entity_label.winfo_reqwidth() / 2
        self.entity_label.place(relx=0.5, x=-int(off_x), y=2 * int(off_y) + 100)

        self.entity_width_label = Label(self, text="Width", font=Font(family="Georgia", size=14))
        self.entity_width_label.pack()
        off_x = self.entity_width_label.winfo_reqwidth() / 2
        self.entity_width_label.place(relx=0.25, x=-int(off_x), y=3 * int(off_y) + 105)

        self.ewe_text = StringVar()
        self.entity_width_entry = Entry(self, textvariable=self.ewe_text, font=Font(family="Georgia", size=14), width=2)
        self.entity_width_entry.pack()
        self.ewe_text.set(f'{settings_json["entity"]["width"]}')
        off_x = self.entity_width_entry.winfo_reqwidth() / 2
        self.entity_width_entry.place(relx=0.25, x=-int(off_x), y=4 * int(off_y) + 110)

        self.entity_height_label = Label(self, text="Height", font=Font(family="Georgia", size=14))
        self.entity_height_label.pack()
        off_x = self.entity_height_label.winfo_reqwidth() / 2
        self.entity_height_label.place(relx=0.75, x=-int(off_x), y=3 * int(off_y) + 105)

        self.ehe_text = StringVar()
        self.entity_height_entry = Entry(self, textvariable=self.ehe_text, font=Font(family="Georgia", size=14), width=2)
        self.entity_height_entry.pack()
        self.ehe_text.set(f'{settings_json["entity"]["height"]}')
        off_x = self.entity_height_entry.winfo_reqwidth() / 2
        self.entity_height_entry.place(relx=0.75, x=-int(off_x), y=4 * int(off_y) + 110)

        self.entity_nox_label = Label(self, text="On X-Axis", font=Font(family="Georgia", size=14))
        self.entity_nox_label.pack()
        off_x = self.entity_nox_label.winfo_reqwidth() / 2
        self.entity_nox_label.place(relx=0.25, x=-int(off_x), y=5 * int(off_y) + 115)

        self.enoxe_text = StringVar()
        self.entity_nox_entry = Entry(self, textvariable=self.enoxe_text, font=Font(family="Georgia", size=14), width=2)
        self.entity_nox_entry.pack()
        self.enoxe_text.set(f'{settings_json["entity"]["nof_x"]}')
        off_x = self.entity_nox_entry.winfo_reqwidth() / 2
        self.entity_nox_entry.place(relx=0.25, x=-int(off_x), y=6 * int(off_y) + 120)

        self.entity_noy_label = Label(self, text="On Y-Axis", font=Font(family="Georgia", size=14))
        self.entity_noy_label.pack()
        off_x = self.entity_noy_label.winfo_reqwidth() / 2
        self.entity_noy_label.place(relx=0.75, x=-int(off_x), y=5 * int(off_y) + 115)

        self.enoye_text = StringVar()
        self.entity_noy_entry = Entry(self, textvariable=self.enoye_text, font=Font(family="Georgia", size=14), width=2)
        self.entity_noy_entry.pack()
        self.enoye_text.set(f'{settings_json["entity"]["nof_y"]}')
        off_x = self.entity_noy_entry.winfo_reqwidth() / 2
        self.entity_noy_entry.place(relx=0.75, x=-int(off_x), y=6 * int(off_y) + 120)

        self.entity_speed_label = Label(self, text="Speed", font=Font(family="Georgia", size=14))
        self.entity_speed_label.pack()
        off_x = self.entity_speed_label.winfo_reqwidth() / 2
        self.entity_speed_label.place(relx=0.5, x=-int(off_x), y=7 * int(off_y) + 125)

        self.espeede_text = StringVar()
        self.entity_speed_entry = Entry(self, textvariable=self.espeede_text, font=Font(family="Georgia", size=14), width=4)
        self.entity_speed_entry.pack()
        self.espeede_text.set(f'{settings_json["speed"]}')
        off_x = self.entity_speed_entry.winfo_reqwidth() / 2
        self.entity_speed_entry.place(relx=0.5, x=-int(off_x), y=8 * int(off_y) + 130)

        self.save_button = Button(self, text="SAVE", command=self._on_save_click, font=Font(family="Georgia", size=14))
        self.save_button.pack()
        off_x = self.save_button.winfo_reqwidth() / 2
        self.save_button.place(relx=0.5, x=-int(off_x), y=9 * int(off_y) + 135)

        self.canvas.pack()

        self.protocol('WM_DELETE_WINDOW', self.close)
        self.deiconify()

    def _on_color_clicked(self, item):
        color = askcolor()
        self.canvas.itemconfig(item, fill=color[1])

    def _on_save_click(self):
        colors = {self.fp_wr: settings_json["first_player"]["skin"]["WALL"],
                  self.fp_hr: settings_json["first_player"]["skin"]["HEAD"],
                  self.fp_tr: settings_json["first_player"]["skin"]["TAIL"],
                  self.fp_fr: settings_json["first_player"]["skin"]["FOOD"],
                  self.sp_wr: settings_json["second_player"]["skin"]["WALL"],
                  self.sp_hr: settings_json["second_player"]["skin"]["HEAD"],
                  self.sp_tr: settings_json["second_player"]["skin"]["TAIL"],
                  self.sp_fr: settings_json["second_player"]["skin"]["FOOD"],}

        for color in colors:
            color_tuple = hex_to_rgb_color(self.canvas.itemcget(color, 'fill'))
            colors[color][0] = color_tuple[0]
            colors[color][1] = color_tuple[1]
            colors[color][2] = color_tuple[2]

        Entity.PygameColor = [[pygame.Color('white'),
                               pygame_color_from_setting(settings_json["first_player"]["skin"]["WALL"]),
                               pygame_color_from_setting(settings_json["first_player"]["skin"]["HEAD"]),
                               pygame_color_from_setting(settings_json["first_player"]["skin"]["TAIL"]),
                               pygame_color_from_setting(settings_json["first_player"]["skin"]["FOOD"])],
                              [pygame.Color('white'),
                               pygame_color_from_setting(settings_json["second_player"]["skin"]["WALL"]),
                               pygame_color_from_setting(settings_json["second_player"]["skin"]["HEAD"]),
                               pygame_color_from_setting(settings_json["second_player"]["skin"]["TAIL"]),
                               pygame_color_from_setting(settings_json["second_player"]["skin"]["FOOD"])]]

        try:
            entity_height = int(self.entity_height_entry.get())
            settings_json["entity"]["height"] = entity_height
            Entity.HEIGHT = entity_height
        except:
            pass
        try:
            entity_width = int(self.entity_width_entry.get())
            settings_json["entity"]["width"] = entity_width
            Entity.WIDTH = entity_width
        except:
            pass
        try:
            entities_on_x = int(self.entity_nox_entry.get())
            settings_json["entity"]["nof_x"] = entities_on_x
            Dimension.NUMBER_OF_ENTITIES_X = entities_on_x
        except:
            pass
        try:
            entities_on_y = int(self.entity_noy_entry.get())
            settings_json["entity"]["nof_y"] = entities_on_y
            Dimension.NUMBER_OF_ENTITIES_Y = entities_on_y
        except:
            pass
        try:
            speed = int(self.entity_speed_entry.get())
            settings_json["speed"] = speed
            CustomEvent.FIRST_PLAYER_MOVE_EVENT_TIMER = speed
            CustomEvent.SECOND_PLAYER_MOVE_EVENT_TIMER = speed
        except:
            pass

        Dimension.BOARD_WIDTH = Dimension.NUMBER_OF_ENTITIES_X * Entity.WIDTH
        Dimension.BOARD_HEIGHT = Dimension.NUMBER_OF_ENTITIES_Y * Entity.HEIGHT

        Dimension.WIDTH_ALIGNMENT = 2 * Entity.WIDTH
        Dimension.HEIGHT_ALIGNMENT = 2 * Entity.HEIGHT

        Dimension.SCREEN_WIDTH = 3 * Dimension.WIDTH_ALIGNMENT + 2 * Dimension.BOARD_WIDTH
        Dimension.SCREEN_HEIGHT = 2 * Dimension.HEIGHT_ALIGNMENT + Dimension.BOARD_HEIGHT

        Dimension.FIRST_BOARD_TOP_LEFT_X = Dimension.WIDTH_ALIGNMENT
        Dimension.FIRST_BOARD_TOP_LEFT_Y = Dimension.HEIGHT_ALIGNMENT

        Dimension.SECOND_BOARD_TOP_LEFT_X = 2 * Dimension.WIDTH_ALIGNMENT + Dimension.BOARD_WIDTH
        Dimension.SECOND_BOARD_TOP_LEFT_Y = Dimension.HEIGHT_ALIGNMENT

        Dimension.BOARD_SIZE = [int(Dimension.BOARD_WIDTH / Entity.WIDTH),
                                int(Dimension.BOARD_HEIGHT / Entity.HEIGHT)]

        with open('settings.json', 'w') as outfile:
            json.dump(settings_json, outfile, indent=4)

        self.close()

    def close(self):
        DisplaySettings.LAST_X = self.winfo_x()
        DisplaySettings.LAST_Y = self.winfo_y()
        self.destroy()
