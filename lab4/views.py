def convert(v, b1=10, b2=16):
    try:
        num = int(v, b1)
    except ValueError:
        return "Неверное число"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return '0'
    res = []
    while num > 0:
        num, mod = divmod(num, b2)
        res.append(digits[mod])
    res = ''.join(reversed(res))
    return f'{v}, (base: {b1}) => {res} (base: {b2})'


def calc_diffs(word): # расчёт разниц между соседними буквами слова
    lst = []
    for i in range(1, len(word)):
        lst.append((ord(word[i]) - ord(word[i-1])) % 26)
    return lst

def decrypt(strs):
    book_words = list(strs[0].split())
    inp_words = list(strs[2:])
    answer = ""

    book_words.sort(key=len) # Сортировка списка по возрастанию длины слов
    words_lengths = {} # Создание словаря, где ключи - длины слов, а значения - первый индекс, в к-ром расположено слово этой длины
    for index, word in enumerate(book_words):
        word_length = len(word)
        if word_length not in words_lengths: # Если длина слова еще не добавлена в словарь, добавляем
            words_lengths[word_length] = index

    # предварительная подготовка списков разниц между соседними буквами
    book_diffs = []
    for book_w in book_words:
        book_diffs.append(calc_diffs(book_w))

    for word in inp_words:
        length = len(word)
        diffs = []
        for i in range(words_lengths.get(length), len(book_words)):
            book_w = book_words[i]
            if length == 1 or i == len(book_words)-1 or len(book_w) != len(book_words[i+1]):
                answer += book_w + "<br>" # <br> - переход на новую строку в HTML
                break

            if diffs == []:
                diffs = calc_diffs(word)
            if diffs == book_diffs[i]: # если списки разниц слов совпадают - зашифрованное слово найдено
                answer += book_w + "<br>"
                break
    return answer


from django.shortcuts import render, HttpResponse

def mainPage(_request):
    return HttpResponse('<h1>Стародубцев Андрей Александрович, гр. 44-24-208, Практическая работа №4</h1><h2><a href="/game/">Игра "5x5"</a></h2><h3>Калькулятор из десятичного числа в шестнадцатиричную: <a href="/calc/55">/calc/[десятичное_число]</a></h3><h3>Решение <a href="https://coderun.yandex.ru/selections/backend/problems/decrypt-message">олимпиадной задачи</a>: <a href="/task/a%20abb%20bab%20abc%7C6%7Cq%7Cbcc%7Caza%7Cabc%7Cz%7Cdef">/task/[входные_строки,разделённые_знаком"|"]</a></h3>')

def gameFunc(request):
    return render(request, "game/index.html")

def calc(_request, val):
    return HttpResponse(convert(val))

def solveTask(_request, val):
    strings = list(val.split("|"))
    # print("INPUT", strings)
    return HttpResponse(decrypt(strings))

def customNotFoundHandler(_request, _exception):
    return HttpResponse('<h1>Что-то пошло не так...</h1>')

# Задача https://coderun.yandex.ru/selections/backend/problems/decrypt-message
# Запрос http://127.0.0.1:8000/task/a%20abb%20bab%20abc%7C6%7Cq%7Cbcc%7Caza%7Cabc%7Cz%7Cdef
