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

from system_converter import NumberSystemConverter
Config.set('kivy', 'keyboard_mode', 'systemanddock')
MAX_SYSTEM = 36


class Container(BoxLayout):
    converter_main_input = ObjectProperty()
    converter_from_numeral_system_input = ObjectProperty()
    converter_to_numeral_system_input = ObjectProperty()
    converter_converter_result_label_label = ObjectProperty()

    calc_left_input = ObjectProperty()
    calc_left_system_input = ObjectProperty()
    calc_right_input = ObjectProperty()
    calc_right_system_input = ObjectProperty()
    calc_before_converter_result_label_label = ObjectProperty()
    calc_result_label_label = ObjectProperty()
    calc_result_system_input = ObjectProperty()

    def _format_number(self, text_number, to_system):
        '''converting the program's operation to a clear number'''

        def check_minus(text_number):
            '''checks whether the number is negative'''
            if text_number[0] == '-':
                return True
            else:
                return False

        def definition_of_the_step(system):
            '''specifies how many characters will be separated by commas'''
            if system == 10:
                return 3
            else:
                return 4

        def complete_formating(text_number, isminus, step):
            '''placement of commas and minus sign'''
            if isminus:
                text_number = text_number[1:]
            res = ''
            if len(text_number) > step+2 and text_number.find('.') == -1:
                text_number = text_number[::-1]
                formatingtext = ''
                for i in range(len(text_number)):
                    if i % step == 0:
                        formatingtext += ','
                    formatingtext += text_number[i]
                res = formatingtext[::-1][:-1]
            elif text_number.find('.') != -1:
                # floating point numbers do not contain commas
                if text_number[0] == '.':
                    text_number = '0' + text_number
                invert_number = text_number[::-1]
                split_nulls = 0
                for s in invert_number:
                    if s == '0':
                        split_nulls += 1
                    else:
                        break
                res = invert_number[split_nulls:][::-1]
            else:
                res = text_number

            if res[-1] == '.':
                res = res[:-1]
            if isminus:
                return '-' + res
            else:
                return res

        return complete_formating(text_number, check_minus(text_number), definition_of_the_step(int(to_system)))

    #----------------------#
    #-screen1 "converter'-#
    #----------------------#

    def converter_system_input_change_value(self, side, value):
        '''increase or decrease the system input value'''

        # if fields is empty
        try:
            value_left_input = int(
                self.converter_from_numeral_system_input.text)
        except:
            value_left_input = 8
        try:
            value_right_input = int(
                self.converter_to_numeral_system_input.text)
        except:
            value_right_input = 8

        if side == 'left':
            if value == 'up' and value_left_input < MAX_SYSTEM:
                self.converter_from_numeral_system_input.text = str(
                    value_left_input+1)
            elif value == 'down' and value_left_input > 2:
                self.converter_from_numeral_system_input.text = str(
                    value_left_input-1)
        else:
            if value == 'up' and value_right_input < MAX_SYSTEM:
                self.converter_to_numeral_system_input.text = str(
                    value_right_input+1)
            elif value == 'down' and value_right_input > 2:
                self.converter_to_numeral_system_input.text = str(
                    value_right_input-1)

    def converter_button_switch_values(self):
        '''swaps input values'''
        self.converter_from_numeral_system_input.text, self.converter_to_numeral_system_input.text = self.converter_to_numeral_system_input.text, self.converter_from_numeral_system_input.text

    def converter_clean(self):
        self.converter_from_numeral_system_input.text = ''
        self.converter_to_numeral_system_input.text = ''
        self.converter_main_input.text = ''
        self.converter_result_label.text = ''

    def converter_calculate(self):
        '''transfer to another number system'''

        def is_correct_input(t, s):
            '''error output for incorrect input'''
            try:
                t = int(t)
                s = int(s)
                if (int(t) < 2 or int(t) > MAX_SYSTEM) or (int(s) < 2 or int(s) > MAX_SYSTEM):
                    self.converter_result_label.text = f'[color=ff3333]Доступные системы счиления\nот 2 до {MAX_SYSTEM }[/color]'
                if int(t) < 2:
                    self.converter_to_numeral_system_input.text = '2'
                elif int(t) > MAX_SYSTEM:
                    self.converter_to_numeral_system_input.text = str(
                        MAX_SYSTEM)

                if int(s) < 2:
                    self.converter_from_numeral_system_input.text = '2'
                elif int(s) > MAX_SYSTEM:
                    self.converter_from_numeral_system_input.text = str(
                        MAX_SYSTEM)
                return True
            except:
                return False

        def make_mathematic():
            user_number = self.converter_main_input.text.upper()
            from_system = self.converter_from_numeral_system_input.text
            to_system = self.converter_to_numeral_system_input.text
            if is_correct_input(to_system, from_system):
                try:
                    res = NumberSystemConverter().make_translation(
                        user_number, from_system, to_system)
                    if res.find('[') == -1:
                        self.converter_result_label.text = self._format_number(
                            res, to_system) + '[sub]({})[/sub]'.format(to_system)
                    else:
                        self.converter_result_label.text = res
                except Exception as exc:
                    print(exc)
                    self.converter_result_label.text = '[color=ff3333]Ошибка[/color]'
            else:
                self.converter_result_label.text = '[color=ff3333]Вы не ввели число[/color]'

        make_mathematic()

    #----------------------#
    #-screen2 "calculator'-#
    #----------------------#
    last_do = 'pls'

    def calc_calculate(self, mode):

        def is_correct_input():
            '''substitution of base values for incorrect input'''
            for txtinput in (self.calc_left_system_input, self.calc_right_system_input, self.calc_result_system_input):
                try:
                    i = int(txtinput.text)
                    if i < 2:
                        txtinput.text = '2'
                    if i > MAX_SYSTEM:
                        txtinput.text = str(MAX_SYSTEM)
                except:
                    txtinput.text = '10'
                if self.calc_left_input.text == '':
                    self.calc_left_input.text = '1'
                if self.calc_right_input.text == '':
                    self.calc_right_input.text = '1'

        def make_mathematic(mode):
            # if the response is 0, it will not be convert to another system
            number_is_null = False
            result_system = self.calc_result_system_input.text
            converter = NumberSystemConverter()

            def do_mathematical_operation(name, isfloat, first_num, second_num):
                self.last_do = name
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
                if not isfloat:
                    return int(res)
                else:
                    return res

            def count_decimal_result(mode):
                '''converting both values to the 10'system and count'''
                first_decimal_num = converter.make_translation(self.calc_left_input.text.upper(),
                                                                int(self.calc_left_system_input.text), 10)
                second_decimal_num = converter.make_translation(self.calc_right_input.text.upper(),
                                                                 int(self.calc_right_system_input.text), 10)

                if '.' in first_decimal_num or '.' in second_decimal_num:
                    isfloat = True
                else:
                    isfloat = False

                return (do_mathematical_operation(
                    mode, isfloat, first_decimal_num, second_decimal_num),
                    first_decimal_num,
                    second_decimal_num)

            def calc_before_result_text(modes, num1, num2, system):
                self.calc_before_result_label.text = f'{num1}[sub](10)[/sub] {modes.get(mode)} {num2}[sub](10)[/sub] = {system}[sub](10)[/sub]'

            try:
                ten_system_res, first_decimal_num, second_decimal_num = count_decimal_result(
                    mode)
                if ten_system_res == 0:
                    number_is_null = True

                # filling out the label before_result
                calc_before_result_text({'min': '-', 'pls': '+', 'mlt': '*', 'del': '/'},
                                        first_decimal_num, second_decimal_num, ten_system_res)

                if not number_is_null:
                    final_res = converter.make_translation(
                        str(ten_system_res), 10, int(result_system))

                    if str(final_res).find('[') == -1:
                        # if not error block, which started with [
                        final_res = self._format_number(
                            final_res, int(self.calc_result_system_input.text))
                        self.calc_result_label.text = self._format_number(
                            str(final_res), int(result_system)) + '[sub]({})[/sub]'.format(result_system)
                    else:
                        # print error
                        self.calc_result_label.text = final_res
                else:
                    # if 0
                    self.calc_result_label.text = '0'
            except Exception as exc:
                print(exc)
                self.calc_result_label.text = '[color=ff3333]Ошибка[/color]'

        is_correct_input()
        make_mathematic(mode)

    def calc_repeat(self):
        '''repeat the last action on the "equals" button'''
        self.calc_calculate(self.last_do)

    def calc_result_system_input_change_value(self, value):
        '''increase or decrease the system input value'''
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
        self.theme_cls.primary_hue = "A100"
        self.theme_cls.primary_palette = "LightBlue"
        return Container()


if __name__ == '__main__':
    MyApp().run()
