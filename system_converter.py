from math import floor

class NumberSystemConverter:
    def make_translation(self, number, system, to_system):
        try:
            self.x = number
            self.s = int(system)
            self.t = int(to_system)
        except:
            return '[color=ff3333]Input Error[/color]'

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
                        return '[color=ff3333]Invalid number\n or system input[/color]'
            elif i in Alphabet:
                if Alphabet_dict[i] >= self.s:
                    return '[color=ff3333]Invalid number\n or system input[/color]'
            else:
                return '[color=ff3333]Invalid input[/color]'

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