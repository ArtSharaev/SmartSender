"""Словарик сообщений для пользователя"""

get_reason = " Вы отклонили анкету. Введите причину вашего решения:"
no_forms = "Сейчас нет анкет на модерации."
rejected_message = "ℹ️ Ваша анкета была отклонена.\n  Предлагаем Вам запол" \
               "нить новую.\n  Причина отклонения: "

enter_start = "\n  Чтобы снова заполнить анкету, введите команду /start"
accepted_message = "ℹ Поздравляем, ваша анкета была подтверждена!"
was_rejected = "Пользователь получил уведомление об отклонении анкеты."
was_accepted = "Пользователь получил уведомление о подтверждении анкеты."

MESSAGES = {
    "get_reason": get_reason,
    "rejected_message": rejected_message,
    "enter_start": enter_start,
    "no_forms": no_forms,
    "accepted_message": accepted_message,
    "was_rejected": was_rejected,
    "was_accepted": was_accepted,
}