from aiogram.utils.helper import Helper, HelperMode, ListItem


class TakeAwayAdminStates(Helper):
    mode = HelperMode.snake_case

    ASK_REASON = ListItem()
    NOTIFY_USER = ListItem()


if __name__ == '__main__':
    print(f'TakeAwayAdminStates list: {TakeAwayAdminStates.all()}')