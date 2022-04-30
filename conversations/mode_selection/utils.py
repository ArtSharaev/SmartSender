from aiogram.utils.helper import Helper, HelperMode, ListItem


class ModeSelectionStates(Helper):
    mode = HelperMode.snake_case

    ASK_ADMIN = ListItem()
    GIVE_ADMIN = ListItem()


if __name__ == '__main__':
    print(f'ProfileStates list: {ModeSelectionStates.all()}')