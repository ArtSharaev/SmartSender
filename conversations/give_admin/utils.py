from aiogram.utils.helper import Helper, HelperMode, ListItem


class GiveAdminStates(Helper):
    mode = HelperMode.snake_case

    GIVE_ADMIN = ListItem()


if __name__ == '__main__':
    print(f'GiveAdminStates list: {GiveAdminStates.all()}')