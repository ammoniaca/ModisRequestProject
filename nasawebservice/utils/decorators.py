from enum import Enum, unique


def iter2list(func):
    """Decorator method to convert a generator in a list.

        via https://stackoverflow.com/questions/48594971/yield-then-convert-to-a-list-or-returning-a-list-directly

    Parameters
    ----------
    func
        Generator to convert in list.

    Returns
    -------
    list

    Examples
    --------
    >>> def get_sequence():
    ...     num = [1, 2, 3, 4, 5, 6]
    ...     for n in num:
    ...         yield n
    >>> gen = get_sequence()
    >>> print(next(gen))
    1
    >>> print(next(gen))
    2
    >>> @iter2list
    ... def get_sequence():
    ...     num = [1, 2, 3, 4, 5, 6]
    ...     for n in num:
    ...         yield n
    >>> gen = get_sequence()
    >>> print(gen)
    [1, 2, 3, 4, 5, 6]

    """
    def wrapped(*args):
        return list(func(*args))

    return wrapped


def stringformat(cls_enum: Enum) -> Enum:
    """Class decorator for enumerations in order to overload the the special
    method __str__(). Using the decorator @stringformat it is possible to obtain directly,
    as string (str), the constant value contained in the appropriate attribute of
    the enumerations.

        via https://pencilprogrammer.com/decorate-python-class/

    Parameters
    ----------
    cls_enum:
        Enumerations

    Returns
    -------
    Enumerations

    Raises
    ------
    TypeError
        If cls_enum is not an enumerations a TypeError is raises.

    Examples
    --------
    >>> from enum import Enum, unique
    >>> @unique
    >>> @stringformat
    >>> class Numbers(Enum):
    ...         ONE = 'one'
    ...         TWO = 'two'
    ...         THREE = 'three'
    >>> one = str(Numbers.ONE)
    >>> type(one)
    <class 'str'>
    >>> two = Numbers.TWO
    >>> type(two)
    <enum 'Numbers'>
    >>> type(two.value)
    <class 'str'>
    """
    if not issubclass(cls_enum, Enum):
        raise TypeError(f' Class: {cls_enum.__name__}, is not an enumerations.')

    # define a new special method for __str__()
    def new__str__(self):
        return str(self.value)

    # replace the new special method __str__() with old method __str__()
    cls_enum.__str__ = new__str__

    # return the modified enumerations
    return cls_enum
