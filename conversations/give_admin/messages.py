"""Словарик сообщений для пользователя"""

ask_admin = "Вам было предложено стать админом!\nСогласны?"
ask_user = "Какому пользователю предложить право админа?"
admin_greeting = "Поздравляем, теперь Вы админ!\n" \
                 "Вы получили новые возможности."
admin_negate = "Вы отклонили предложение."
negate_notify = "Предложение стать админом было отклонено пользователем"
greeting_notify = "Предложение стать админом было принято пользователем"


MESSAGES = {
    "give_admin": ask_admin,
    "ask_user": ask_user,
    "admin_greeting": admin_greeting,
    "admin_negate": admin_negate,
    "negate_notify": negate_notify,
    "greeting_notify": greeting_notify,
}
