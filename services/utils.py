import numpy as np


def create_new_board(dim: int) -> np.ndarray:
    """
    :param dim: dimension of the grid
    :return: a zero-matrix composed by numpy 2d array
    """
    # create a clear board
    if not dim:
        raise TypeError("Dimension is necessary")
    board = np.zeros((dim, dim), dtype=int)
    return board


def select_empty_position(board):
    """
    Select an empty postion to put entity on
    :param board: board instance
    :return: list of available choices
    """
    result = np.where(board == 0)
    list_of_coordinate = list(zip(result[0], result[1]))
    numpyint64_to_int = [(row.item(), col.item()) for row, col in list_of_coordinate]
    return numpyint64_to_int