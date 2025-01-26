import numpy as np
from copy import deepcopy

from src.utils.matrix_util import matrix_extracted, vector_extracted, get_index_br_matrix

type ReviewedSimplexProps = {
    "A": [],
    "b": [],
    "c": [],
    "r_index": [],
    "b_index": []
}


class ReviewedSimplex:

    def __init__(self, props: ReviewedSimplexProps):
        props["r_index"] = props.get("r_index", [])
        props["b_index"] = props.get("b_index", [])
        self.props = {
            "A": props["A"],
            "b": props["b"],
            "c": props["c"],
        }
        self.artificial_count = props["D"].count(">=") + props["D"].count("=")
        self.tableau = deepcopy(self.props)

        if ("r_index" not in props or len(props.get("r_index", [])) == 0 or
                "b_index" not in props or len(props.get("b_index", [])) == 0):
            self.b_index, self.r_index = get_index_br_matrix(self.tableau["A"])
        else:
            self.b_index, self.r_index = props["b_index"], props["r_index"]

        self.vector_cr = vector_extracted(self.tableau["c"], self.r_index)
        self.matrix_r = matrix_extracted(self.tableau["A"], self.r_index)
        self.vector_cb = vector_extracted(self.tableau["c"], self.b_index)
        self.matrix_b = matrix_extracted(self.tableau["A"], self.b_index)
        self.vector_b = self.tableau['b']
        self.inv_matrix_b = np.linalg.inv(self.matrix_b)

    def execute(self):

        self.matrix_r = self.inv_matrix_b @ self.matrix_r
        self.vector_b = self.inv_matrix_b @ self.vector_b
        self.vector_cr = self.vector_cr - (self.vector_cb @ (self.inv_matrix_b @ self.matrix_r))

        while True:
            better, ilimitado = self.pivoting(self.r_index, self.b_index)
            if better:
                return self.r_index, self.b_index, better, ilimitado, self._solve
            if ilimitado:
                return None, None, None, ilimitado, [None, None]

            self.vector_cr = vector_extracted(self.tableau["c"], self.r_index)
            self.matrix_r = matrix_extracted(self.tableau["A"], self.r_index)
            self.vector_cb = vector_extracted(self.tableau["c"], self.b_index)
            self.matrix_b = matrix_extracted(self.tableau["A"], self.b_index)

            self.inv_matrix_b = np.linalg.inv(self.matrix_b)

            self.vector_b = (self.inv_matrix_b @ self.tableau['b'])
            self.vector_cr = self.vector_cr - (self.vector_cb @ (self.inv_matrix_b @ self.matrix_r))
            self.matrix_r = self.inv_matrix_b @ self.matrix_r

    def _solve(self):
        col_b = self.props["b"][:, np.newaxis]
        fo = self.vector_cb @ self.inv_matrix_b @ col_b
        vector_b = self.inv_matrix_b @ col_b
        return fo[0], vector_b[:, 0]

    def pivoting(self, r_index: [], b_index: []):

        min_cr = self.vector_cr.min()
        if min_cr >= 0:
            return True, False

        index_min_cr = np.where(self.vector_cr == min_cr)[0][0]

        col_min_matrix_r = self.matrix_r[:, index_min_cr]
        col_min_matrix_r[col_min_matrix_r == 0] = -1
        self.vector_b[col_min_matrix_r == 0] = 1

        reason_test = np.divide(self.vector_b, col_min_matrix_r)
        reason_test_valid = reason_test[reason_test >= 0]

        if len(reason_test_valid) == 0:
            return False, True

        value_min_reason_test = np.min(reason_test_valid)
        index_min_reason_test = np.where(reason_test == value_min_reason_test)[0][0]

        b_index[index_min_reason_test], r_index[index_min_cr] = r_index[index_min_cr], b_index[
            index_min_reason_test]

        return False, False
