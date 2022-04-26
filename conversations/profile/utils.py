from aiogram.utils.helper import Helper, HelperMode, ListItem


class ProfileStates(Helper):
    mode = HelperMode.snake_case

    GET_NAME = ListItem()
    GET_SURNAME = ListItem()
    GET_GENDER = ListItem()
    GET_AGE = ListItem()
    GET_POSITION = ListItem()
    GET_POSITION2 = ListItem()


if __name__ == '__main__':
    print(f'ProfileStates list: {ProfileStates.all()}')