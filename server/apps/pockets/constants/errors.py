from typing import Final


class TransactionErrors:
    NOT_USERS_CATEGORY: Final[str] = 'У пользователя нет такой категории'
    NEEDED_CATEGORY: Final['str'] = 'Требуется поле category'
    CATEGORY_NOT_ALLOWED: Final['str'] = 'Поле category запрещено'


class TransactionCategoryErrors:
    ALREADY_EXISTS: Final[str] = 'У пользоваетля уже существует категория с таким названием и типом'
