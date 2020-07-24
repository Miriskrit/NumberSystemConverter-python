from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivymd.uix.card import MDCard
from kivy.core.clipboard import Clipboard

from translate import NumberSystemTranslation
Config.set('kivy', 'keyboard_mode', 'systemanddock')


class Container(BoxLayout):
    translator_translator_main_input = ObjectProperty()
    translator_from_numeral_system_input = ObjectProperty()
    translator_to_numeral_system_input = ObjectProperty()
    translator_translator_result_label_label = ObjectProperty()

    calc_left_input = ObjectProperty()
    calc_left_system_input = ObjectProperty()
    calc_right_input = ObjectProperty()
    calc_right_system_input = ObjectProperty()
    calc_before_translator_result_label_label = ObjectProperty()
    calc_result_label_label = ObjectProperty()
    calc_result_system_input = ObjectProperty()

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
            i_left = int(self.translator_from_numeral_system_input.text)
        except:
            i_left = 8

        try:
            i_right = int(self.translator_to_numeral_system_input.text)
        except:
            i_right = 8

        if side == 'left':
            if value == 'up' and i_left < 24:
                self.translator_from_numeral_system_input.text = str(i_left+1)
            elif value == 'down' and i_left > 2:
                self.translator_from_numeral_system_input.text = str(i_left-1)
        else:
            if value == 'up' and i_right < 24:
                self.translator_to_numeral_system_input.text = str(i_right+1)
            elif value == 'down' and i_right > 2:
                self.translator_to_numeral_system_input.text = str(i_right-1)

    #

    def switch(self):
        self.translator_from_numeral_system_input.text, self.translator_to_numeral_system_input.text = self.translator_to_numeral_system_input.text, self.translator_from_numeral_system_input.text

    #

    def clean(self):
        self.translator_from_numeral_system_input.text = ''
        self.translator_to_numeral_system_input.text = ''
        self.translator_main_input.text = ''
        self.translator_result_label.text = ''

    #

    def calculate(self):

        def is_correct_input(t, s):
            try:
                t = int(t)
                s = int(s)
                if (int(t) < 2 or int(t) > 24) or (int(s) < 2 or int(s) > 24):
                    self.translator_result_label.text = '[color=ff3333]Доступные системы счиления\nот 2 до 24[/color]'
                if int(t) < 2:
                    self.translator_to_numeral_system_input.text = '2'
                elif int(t) > 24:
                    self.translator_to_numeral_system_input.text = '24'

                if int(s) < 2:
                    self.translator_from_numeral_system_input.text = '2'
                elif int(s) > 24:
                    self.translator_from_numeral_system_input.text = '24'
                return True
            except:
                return False

        def make_mathematic():
            user_number = self.translator_main_input.text.upper()
            from_system = self.translator_from_numeral_system_input.text
            to_system = self.translator_to_numeral_system_input.text
            if is_correct_input(to_system, from_system):
                try:
                    text = NumberSystemTranslation().make_translation(
                        user_number, from_system, to_system)
                    if text.isdigit():
                        text = self.format_text(
                            text, to_system) + '[sub]({})[/sub]'.format(to_system)
                    self.translator_result_label.text = text
                except:
                    self.translator_result_label.text = '[color=ff3333]Ошибка[/color]'
            else:
                self.translator_result_label.text = '[color=ff3333]Вы не ввели число[/color]'
        make_mathematic()

    def to_count(self, mode):

        def calc_is_correct_input():
            for txtinput in (self.calc_left_system_input, self.calc_right_system_input, self.calc_result_system_input):
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
            c = NumberSystemTranslation()
            return c.make_translation(self.calc_left_input.text.upper(), int(self.calc_left_system_input.text), 10), \
                c.make_translation(self.calc_right_input.text.upper(), int(
                    self.calc_right_system_input.text), 10)

        def make_mathematic():

            def mathematical_operation(name, isfloat, first_num, second_num):
                if name == 'min':
                    res = float(first_num)-float(second_num)

                elif name == 'pls':
                    res = float(first_num)+float(second_num)

                elif name == 'mlt':
                    res = float(first_num)*float(second_num)

                else:
                    res = round(float(first_num)/float(second_num), 5)
                    if res == int(res):
                        res = int(res)

                self.last_do = name

                if not isfloat:
                    return int(res)
                else:
                    return res

            number_is_null = False
            final_syst = self.calc_result_system_input.text
            first_num, second_num = convert_both_to_ten()
            c = NumberSystemTranslation()
            try:
                first_num = c.make_translation(self.calc_left_input.text.upper(),
                                               int(self.calc_left_system_input.text), 10)
                second_num = c.make_translation(self.calc_right_input.text.upper(),
                                                int(self.calc_right_system_input.text), 10)

                if '.' in first_num or '.' in second_num:
                    isfloat = True
                else:
                    isfloat = False

                ten_system_res = mathematical_operation(
                    mode, isfloat, first_num, second_num)
                if ten_system_res == 0:
                    number_is_null = True

                modes = {'min': '-', 'pls': '+', 'mlt': '*', 'del': '/'}
                self.calc_before_result_label.text = f'{first_num}[sub](10)[/sub] {modes.get(mode)} {second_num}[sub](10)[/sub] = {ten_system_res}[sub](10)[/sub]'

                if not number_is_null:
                    final_res = str(c.make_translation(
                        str(ten_system_res), 10, int(final_syst)))
                    if isfloat:
                        final_res = float(final_res)
                    else:
                        final_res = int(final_res)

                    if str(final_res).find('[') == -1:
                        self.calc_result_label.text = self.format_text(
                            str(final_res), int(final_syst)) + '[sub]({})[/sub]'.format(final_syst)
                    else:
                        # если обнаружена ошибка
                        self.calc_result_label.text = final_res
                else:
                    self.calc_result_label.text = '0'
            except Exception as exc:
                print(exc)
                self.calc_result_label.text = '[color=ff3333]Ошибка[/color]'

        calc_is_correct_input()
        make_mathematic()

    #

    def calc_repeat(self):
        self.to_count(self.last_do)

    #

    def calc_change_value(self, value):
        try:
            i = int(self.calc_result_system_input.text)
        except:
            i = 8

        if i > 1 and value > 0:
            self.calc_result_system_input.text = str(i + 1)
            self.calc_repeat()
        elif i < 25 and value < 0:
            self.calc_result_system_input.text = str(i - 1)
            self.calc_repeat()

    #

    def calc_clean(self):
        self.calc_result_system_input.text = ''
        self.calc_left_input.text = ''
        self.calc_right_input.text = ''
        self.calc_left_system_input.text = ''
        self.calc_right_system_input.text = ''
        self.calc_before_result_label.text = ''
        self.calc_result_label.text = ''


class MyApp(MDApp):

    def build(self):
        self.icon = 'myicon.png'
        self.theme_cls.theme_style = "Dark"
        return Container()


if __name__ == '__main__':
    MyApp().run()
