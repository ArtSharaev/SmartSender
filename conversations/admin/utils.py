from aiogram.utils.helper import Helper, HelperMode, ListItem


class AdminStates(Helper):
    mode = HelperMode.snake_case

    SEND_REJECTED = ListItem()


if __name__ == '__main__':
    print(f'GiveAdminStates list: {AdminStates.all()}')