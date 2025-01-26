import numpy as np


def matrix_extracted(old_matrix: np.array, array: []):
    rows_old, _ = old_matrix.shape
    extracted_matrix = np.zeros(shape=(rows_old, len(array)))
    for index, element in enumerate(array):
        extracted_matrix[:, index] = old_matrix[:, element]
    return extracted_matrix


def vector_extracted(old_vector: [], array: []):
    extracted_matrix = np.zeros(shape=len(array))
    for index, element in enumerate(array):
        extracted_matrix[index] = old_vector[element]
    return extracted_matrix


def get_index_br_matrix(A: np.array):
    base_indices = []

    for row_index in range(A.shape[0]):
        for col_index in range(A.shape[1]):
            if A[row_index, col_index] == 1 and (A[:, col_index] == np.eye(A.shape[0])[:, row_index]).all():
                base_indices.append(col_index)
                break
    all_indices = np.arange(A.shape[1])
    non_base_indices = np.setdiff1d(all_indices, base_indices)
    return np.array(base_indices), non_base_indices


def remove_last_columns(A, c, r, num_cols_to_remove):
    if num_cols_to_remove > A.shape[1]:
        raise ValueError("O número de colunas a remover é maior que o total de colunas em A.")

    new_column_count = A.shape[1] - num_cols_to_remove
    removed_indices = np.array(range(new_column_count, A.shape[1]))
    # np.delete(r,removed_indices)
    r_removed = r[~np.isin(r, removed_indices)]
    A_new = A[:, :new_column_count]
    c_new = c[:new_column_count]

    return A_new, c_new, r_removed


def get_two_phase_c(A, artificial_count):
    _, cols = A.shape
    c_artificial_start = cols - artificial_count
    c_new = np.zeros(cols)
    c_new[c_artificial_start:] = 1

    return c_new


def get_big_m_c(c, artificial_count):
    cols = c.shape[0]
    c_artificial_start = cols - artificial_count
    c[c_artificial_start:] = 100

    return c
