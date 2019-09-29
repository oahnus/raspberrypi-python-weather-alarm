#!/usr/bin/python3
# -*- coding:utf-8 -*-
import math

class Num2Word:
    words = {
        0: '零',
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六',
        7: '七',
        8: '八',
        9: '九',
        10: '十',
        100: '百',
        1000: '千',
        10000: '万',
    }

    # TODO 1024 -> 一千二十四  ==> 1024 -> 一千零二十四
    # TODO 1004 -> 一千四  ==> 1024 -> 一千零四
    # TODO 1024.2 小数点
    @staticmethod
    def to_word(num):
        if isinstance(num, int):
            pass
        elif isinstance(num, str):
            num = int(num)
        else:
            raise TypeError('num must be int or str')
        if num < 0:
            return '负' + Num2Word.to_word(-num)
        else:
            quotient = num
            remainder = 0
            s = ""
            ten_num = 0
            while quotient > 0:
                quotient = int(num / 10)
                remainder = num % 10
                if remainder > 0:
                    if ten_num > 0:
                        s = Num2Word.words[remainder] + Num2Word.words[int(math.pow(10, ten_num))] + s
                    else:
                        s = Num2Word.words[remainder] + s
                num = int(num / 10)
                ten_num += 1
            return s

if __name__ == '__main__':
    print(Num2Word.to_word(int(18)))
    print(type("se") == str)