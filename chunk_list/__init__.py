import math


def chunks(array: list, n_elements: int) -> list[list]:
    """
    Chunk 'array' into 'n_elements' sized list

    :arg array: List to chunk
    :arg n_elements: size of chunks
    :return: list
    """
    chunks = math.floor(len(array) / n_elements)
    residue = len(array) % n_elements
    main_list = []
    sub_list = []

    # max_index = n_elements * chunks
    start = 0
    end = 0
    for i in range(1, chunks + 1):
        end = i * n_elements

        sub_list = array[start:end]
        main_list.append(sub_list)
        start = end
    if (chunks * n_elements) < len(array):
        sub_list = array[end:end+residue]
        main_list.append(sub_list)
    return main_list