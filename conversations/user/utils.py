from aiogram.utils.helper import Helper, HelperMode, ListItem


class UserStates(Helper):
    mode = HelperMode.snake_case

    GET_RECIPIENT = ListItem()
    GET_MESSAGE = ListItem()


if __name__ == '__main__':
    print(f'GiveAdminStates list: {UserStates.all()}')