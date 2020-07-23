from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from math import floor
from kivy.config import Config
from kivymd.uix.card import MDCard
from kivy.core.clipboard import Clipboard
Config.set('kivy', 'keyboard_mode', 'systemanddock')


class Counter:
    def main(self, number, system, to_system):
        try:
            self.x = number
            self.s = int(system)
            self.t = int(to_system)
        except:
            return '[color=ff3333]Ошибка при вводе[/color]'

        Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Numbers = '0123456789.'
        Alphabet_dict = {chr(int(a)+55): a for a in range(10, 36)}
        Alphabet_dict_to_ten = {a: chr(int(a)+55) for a in range(10, 36)}
        main_int = []
        minus = False

        if self.x[0:1] == '-':
            minus = True
            self.x = self.x[1:]

        for i in self.x:
            if i in Numbers:
                if i != '.':
                    if int(i) >= self.s:
                        return '[color=ff3333]Вы ввели неверное число\n или систему счисления[/color]'
            elif i in Alphabet:
                if Alphabet_dict[i] >= self.s:
                    return '[color=ff3333]Вы ввели неверное число\n или систему счисления[/color]'
            else:
                return '[color=ff3333]Некорректный ввод[/color]'

        def convert():
            new_x = 0
            for i in range(len(self.x)):
                if self.x[i] in Numbers:
                    if self.x[i] == '.':
                        main_int.append(self.x[i])
                    else:
                        main_int.append(int(self.x[i]))
                else:
                    for j in Alphabet:
                        if self.x[i] == j:
                            new_x = Alphabet_dict[j]
                            main_int.append(new_x)
                            break

        def other_to_ten():
            cout = 0
            cout2 = 0
            degree = -1
            new_main_int = []

            for length in range(len(main_int)):
                if main_int[length] != '.':
                    new_main_int.append(main_int[length])
                    point_pos = len(main_int)
                else:
                    point_pos = length
                    break
            new_main_int.reverse()
            for i in range(len(new_main_int)):
                cout = cout + new_main_int[i]*(self.s**i)
            for i in range(point_pos + 1, len(main_int)):
                cout2 = cout2 + main_int[i]*(self.s**degree)
                degree -= 1

            summ = cout + cout2
            return (str(summ))

        def ten_to_other(x_ten):
            rezult = ''
            rezult2 = ''
            if '.' in x_ten:
                x_ten = x_ten.split('.')
                x = int(x_ten[0])
                x_afterpoint = float('0.' + x_ten[1])
                for _ in range(11):
                    x_afterpoint *= self.t
                    if x_afterpoint*self.t < self.t:
                        if self.t >= 10 and floor(x_afterpoint) >= 10:
                            rezult2 += str(
                                Alphabet_dict_to_ten[floor(x_afterpoint)])
                        else:
                            rezult2 += str(floor(x_afterpoint))
                    else:
                        if self.t >= 10 and floor(x_afterpoint) >= 10:
                            rezult2 += str(
                                Alphabet_dict_to_ten[floor(x_afterpoint)])
                        else:
                            rezult2 += str(floor(x_afterpoint))
                        x_afterpoint = x_afterpoint % 1
            else:
                x = int(x_ten)
            while x >= 1:
                if x % self.t <= 9:
                    rezult += str(x % self.t)
                else:
                    rezult += str(Alphabet_dict_to_ten[x % self.t])
                x = x//self.t
            rezult = rezult[::-1]
            rezult_final = rezult + '.' + rezult2
            if rezult_final[-1] == '.':
                rezult_final = rezult_final[:-1]
            if minus == True:
                rezult_final = '-' + rezult_final
            return rezult_final

        convert()
        if self.s == 10:
            rez = ten_to_other(self.x)
        else:
            ten = other_to_ten()
            rez = ten_to_other(ten)
        return rez


class Container(BoxLayout):
    main_input = ObjectProperty()
    from_system_input = ObjectProperty()
    to_system_input = ObjectProperty()
    result = ObjectProperty()
    calc_left_input = ObjectProperty()
    calc_left_s = ObjectProperty()
    calc_right_input = ObjectProperty()
    calc_right_s = ObjectProperty()
    calc_decision = ObjectProperty()
    calc_result = ObjectProperty()
    calc_result_input = ObjectProperty()
    last_do = 'pls'

    def format_text(self, text, t):
        if text[0] == '-':
            text = text[1:]
            isminus = True
        else:
            isminus = False
        if int(t) == 10:
            step = 3
        else:
            step = 4
        if len(text) > step and text.find('.') == -1:
            text = text[::-1]
            formatingtext = ''
            for i in range(len(text)):
                if i % step == 0:
                    formatingtext += ','
                formatingtext += text[i]
            if isminus:
                return '-' + formatingtext[::-1][:-1]
            return formatingtext[::-1][:-1]
        else:
            if text[0] == '.':
                text = '0' + text
            if isminus:
                return '-' + text
            return text

    def change_value(self, side, value):
        try:
            i_left = int(self.from_system_input.text)
        except:
            i_left = 8

        try:
            i_right = int(self.to_system_input.text)
        except:
            i_right = 8

        if side == 'left':
            if value == 'up' and i_left < 24:
                self.from_system_input.text = str(i_left+1)
            elif value == 'down' and i_left > 2:
                self.from_system_input.text = str(i_left-1)
        else:
            if value == 'up' and i_right < 24:
                self.to_system_input.text = str(i_right+1)
            elif value == 'down' and i_right > 2:
                self.to_system_input.text = str(i_right-1)

    #

    def switch(self):
        self.from_system_input.text, self.to_system_input.text = self.to_system_input.text, self.from_system_input.text

    #

    def clean(self):
        self.from_system_input.text = ''
        self.to_system_input.text = ''
        self.main_input.text = ''
        self.result.text = ''

    #

    def calculate(self):

        def is_correct_input(t, s):
            try:
                t = int(t)
                s = int(s)
                if (int(t) < 2 or int(t) > 24) or (int(s) < 2 or int(s) > 24):
                    self.result.text = '[color=ff3333]Доступные системы счиления\nот 2 до 24[/color]'
                if int(t) < 2:
                    self.to_system_input.text = '2'
                elif int(t) > 24:
                    self.to_system_input.text = '24'

                if int(s) < 2:
                    self.from_system_input.text = '2'
                elif int(s) > 24:
                    self.from_system_input.text = '24'
                return True
            except:
                return False

        def make_mathematic():
            user_number = self.main_input.text.upper()
            from_system = self.from_system_input.text
            to_system = self.to_system_input.text
            if is_correct_input(to_system, from_system):
                c = Counter()
                try:
                    text = c.main(user_number, from_system, to_system)
                    if text.isdigit():
                        text = self.format_text(
                            text, to_system) + '[sub]({})[/sub]'.format(to_system)
                    self.result.text = text
                except:
                    self.result.text = '[color=ff3333]Ошибка[/color]'
            else:
                self.result.text = '[color=ff3333]Вы не ввели число[/color]'
        make_mathematic()


    def to_count(self, mode):

        def calc_is_correct_input():
            for txtinput in (self.calc_left_s, self.calc_right_s, self.calc_result_input):
                try:
                    i = int(txtinput.text)
                    if i < 2:
                        txtinput.text = '2'
                    if i > 24:
                        txtinput.text = '24'
                except:
                    txtinput.text = '10'
                if self.calc_left_input.text == '':
                    self.calc_left_input.text = '1'
                if self.calc_right_input.text == '':
                    self.calc_right_input.text = '1'

        def convert_both_to_ten():
            c = Counter()
            return c.main(self.calc_left_input.text.upper(), int(self.calc_left_s.text), 10), c.main(self.calc_right_input.text.upper(), int(self.calc_right_s.text), 10)

        def make_mathematic():
            number_is_null = False
            final_syst = self.calc_result_input.text
            first_num, second_num = convert_both_to_ten()
            c = Counter()
            try:
                first_num = c.main(self.calc_left_input.text.upper(),
                                   int(self.calc_left_s.text), 10)
                second_num = c.main(self.calc_right_input.text.upper(),
                                    int(self.calc_right_s.text), 10)
                if mode == 'min':
                    self.last_do = 'min'
                    res = int(first_num)-int(second_num)
                    if res == 0:
                        number_is_null = True

                elif mode == 'pls':
                    self.last_do = 'pls'
                    res = int(first_num)+int(second_num)

                elif mode == 'mlt':
                    self.last_do = 'mlt'
                    res = int(first_num)*int(second_num)

                else:
                    self.last_do = 'del'
                    res = round(int(first_num)/int(second_num), 5)
                    if res == int(res):
                        res = int(res)

                modes = {'min': '-', 'pls': '+', 'mlt': '*', 'del': '/'}
                self.calc_decision.text = f'{first_num}[sub](10)[/sub] {modes.get(mode)} {second_num}[sub](10)[/sub] = {res}[sub](10)[/sub]'

                if not number_is_null:
                    t = str(c.main(str(res), 10, int(final_syst)))
                    if t.find('[') == -1:
                        self.calc_result.text = self.format_text(
                            t, int(final_syst)) + '[sub]({})[/sub]'.format(final_syst)
                    else:
                        self.calc_result.text = t
                else:
                    self.calc_result.text = '0'
            except:
                self.calc_result.text = '[color=ff3333]Ошибка[/color]'

        calc_is_correct_input()
        make_mathematic()

    #

    def calc_repeat(self):
        self.to_count(self.last_do)

    #

    def calc_change_value(self, value):
        try:
            i = int(self.calc_result_input.text)
        except:
            i = 8

        if i > 1 and value > 0:
            self.calc_result_input.text = str(i + 1)
            self.calc_repeat()
        elif i < 25 and value < 0:
            self.calc_result_input.text = str(i - 1)
            self.calc_repeat()

    #

    def calc_clean(self):
        self.calc_result_input.text = ''
        self.calc_left_input.text = ''
        self.calc_right_input.text = ''
        self.calc_left_s.text = ''
        self.calc_right_s.text = ''
        self.calc_decision.text = ''
        self.calc_result.text = ''




class MyApp(MDApp):

    def build(self):
        self.icon = 'myicon.png'
        self.theme_cls.theme_style = "Dark"
        return Container()


if __name__ == '__main__':
    MyApp().run()
