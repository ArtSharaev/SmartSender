"""Словарик сообщений для пользователя"""

greeting = "Привет от разработчиков!\n\nЗаполните анкету, " \
           "чтобы получить доступ к функционалу."
askname = "Введите своё настоящее имя:"
asksurname = "Введите свою настоящую фамилию:"
askgender = "Выберите ваш пол:"
askposition = "Кто вы по отношению к школе? Выберите из предложенного:"
inputerror = "Ошибка ввода. Попробуйте еще раз."
stop = "Успех! А тут пока заглушка)"

MESSAGES = {
    "greeting": greeting,
    "askname": askname,
    "asksurname": asksurname,
    "askgender": askgender,
    "askposition": askposition,
    "pass": stop,
    "inputerror": inputerror,
}