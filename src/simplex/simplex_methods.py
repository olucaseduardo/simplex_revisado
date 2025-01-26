from src.simplex.reviewed_simplex import ReviewedSimplex
from src.utils.matrix_util import remove_last_columns, get_two_phase_c, get_big_m_c
import numpy as np

PPL_ILIMITADO = 1
PPL_INVIAVEL = -1


class SimplexMethods:

    def __init__(self, standard_form):
        self.artificial_count = standard_form["D"].count(">=") + standard_form["D"].count("=")
        self.standard_form = standard_form

    def execute(self):

        if self.artificial_count == 0:
            return self._generalize()
        else:
            if self.standard_form["method"] == "Duas Fases":
                return self._two_phases()
            return self._big_m()

    def _generalize(self):
        reviewed_simplex = ReviewedSimplex(self.standard_form)
        return reviewed_simplex.execute()

    def _big_m(self):
        c_original = self.standard_form["c"]
        self.standard_form["c"] = get_big_m_c(c_original, self.artificial_count)
        reviewed_simplex = ReviewedSimplex(self.standard_form)
        result = reviewed_simplex.execute()
        if result[3]:
            return PPL_ILIMITADO

        artificial_indexes = np.array(list(range(len(c_original) - self.artificial_count, len(c_original))))
        artificial_tests = np.isin(artificial_indexes, result[1])
        exists = np.any(artificial_tests)

        if exists:
            return PPL_INVIAVEL
        return result

    def _two_phases(self):
        # FASE 1
        c_original = self.standard_form["c"]

        self.standard_form["c"] = get_two_phase_c(self.standard_form["A"], self.artificial_count)

        # Fase 1
        one_phase_reviewed_simplex = ReviewedSimplex(self.standard_form)
        self.standard_form["r_index"], self.standard_form[
            "b_index"], better, ilim, solve = one_phase_reviewed_simplex.execute()
        if ilim:
            return PPL_ILIMITADO
        fo, b = solve()
        if fo != 0:
            return PPL_INVIAVEL
        # FASE 2
        A_new, c_new, r_new = remove_last_columns(self.standard_form["A"], c_original, self.standard_form["r_index"],
                                                  self.artificial_count)
        self.standard_form["r_index"] = r_new
        self.standard_form["A"] = A_new
        self.standard_form["c"] = c_new
        #
        two_phase_reviewed_simplex = ReviewedSimplex(self.standard_form)
        #
        result = two_phase_reviewed_simplex.execute()
        if result[3]:
            return PPL_ILIMITADO
        fo, _ = result[4]()
        return result
