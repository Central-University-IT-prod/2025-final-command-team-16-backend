from enum import Enum


class BookStateType(Enum):
    NEW = "Новая"
    GOOD = "Хорошая"
    MINOR_DAMAGE = "С небольшими повреждениями"
    MAJOR_DAMAGE = "С большими повреждениями"
