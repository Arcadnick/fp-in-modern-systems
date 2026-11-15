"""История изменений каталога для отмены: кортеж прошлых версий, последняя — в конце.

Каталог неизменяемый, поэтому хранить старые версии безопасно.
"""


def remember(history, old, new):
    """История после действия меню: старая версия запоминается, только если каталог изменился."""
    return history if new is old else history + (old,)


def can_undo(history):
    return len(history) > 0


def undone(history):
    """(предыдущая версия каталога, история без неё)."""
    return history[-1], history[:-1]
