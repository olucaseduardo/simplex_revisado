from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QLabel, QScrollArea, QFileDialog
)
import sys
from fractions import Fraction

from src.simplex.simplex_methods import PPL_INVIAVEL, PPL_ILIMITADO, SimplexMethods
from src.simplex.standard_form import StandardForm


class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.result_window = None
        self.final_values = None
        self.inequalities = None
        self.objective_values = None
        self.matrix_values = None
        self.setWindowTitle("Gerador de Matriz")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.main_layout.addWidget(self.scroll_area)

        self.config_layout = QHBoxLayout()

        self.objective_label = QLabel("Objetivo da Função:")
        self.config_layout.addWidget(self.objective_label)

        self.objective_box = QComboBox()
        self.objective_box.addItems(["Maximizar", "Minimizar"])
        self.config_layout.addWidget(self.objective_box)

        self.rows_label = QLabel("Restrições:")
        self.rows_input = QLineEdit()
        self.rows_input.setPlaceholderText("Número de Restrições")
        self.config_layout.addWidget(self.rows_label)
        self.config_layout.addWidget(self.rows_input)

        self.cols_label = QLabel("Variáveis:")
        self.cols_input = QLineEdit()
        self.cols_input.setPlaceholderText("Número de Variáveis")
        self.config_layout.addWidget(self.cols_label)
        self.config_layout.addWidget(self.cols_input)

        self.scroll_layout.addLayout(self.config_layout)

        self.second_row_layout = QHBoxLayout()

        self.initial_solution_label = QLabel("Solução Inicial:")
        self.second_row_layout.addWidget(self.initial_solution_label)

        self.initial_solution_box = QComboBox()
        self.initial_solution_box.addItems(["Duas Fases", "Big M"])
        self.second_row_layout.addWidget(self.initial_solution_box)

        self.import_button = QPushButton("Importar Arquivo")
        self.import_button.clicked.connect(self.load_file)
        self.second_row_layout.addWidget(self.import_button)

        self.scroll_layout.addLayout(self.second_row_layout)

        self.generate_button = QPushButton("Gerar Tableau")
        self.generate_button.clicked.connect(self.generate_matrix)
        self.scroll_layout.addWidget(self.generate_button)

        self.matrix_layout = QVBoxLayout()
        self.scroll_layout.addLayout(self.matrix_layout)

        self.central_widget.setLayout(self.main_layout)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Text Files (*.txt)")

        if file_path:
            try:
                with open(file_path, "r") as file:
                    lines = file.readlines()

                objective_values, matrix_values, inequalities, final_values, objective_type = self.generate_matrix_from_lines(
                    lines)

                self.rows_input.setText(str(len(matrix_values)))
                self.cols_input.setText(str(len(matrix_values[0])))
                self.generate_matrix()
                self.objective_box.setCurrentText(objective_type)

                for idx, field in enumerate(self.objective_values):
                    field.setText(str(objective_values[idx]))

                for row_idx, row_layout in enumerate(self.matrix_values):
                    for col_idx, field in enumerate(row_layout):
                        field.setText(str(matrix_values[row_idx][col_idx]))

                    self.inequalities[row_idx].setCurrentText(inequalities[row_idx])

                    self.final_values[row_idx].setText(str(final_values[row_idx]))

            except Exception as e:
                QMessageBox.critical(self, "Erro de Leitura", f"Ocorreu um erro ao ler o arquivo: {str(e)}")

    def generate_matrix_from_lines(self, lines):
        first_word = lines[0].split()[0]
        if first_word == 'Max':
            objective_type = 'Maximizar'
        elif first_word == 'Min':
            objective_type = 'Minimizar'
        else:
            objective_type = first_word
        objective_values = list(map(Fraction, lines[0].split()[1:]))

        inequalities = []
        matrix_values = []
        final_values = []

        for line in lines[2:]:
            if line.strip() == '':
                continue

            parts = line.split()
            row_values = list(map(Fraction, parts[:-2]))
            inequality = parts[-2]
            final_value = Fraction(parts[-1])

            matrix_values.append(row_values)
            inequalities.append(inequality)
            final_values.append(final_value)

        return objective_values, matrix_values, inequalities, final_values, objective_type

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def generate_matrix(self):
        self.clear_layout(self.matrix_layout)
        self.objective_values = []
        self.matrix_values = []
        self.inequalities = []
        self.final_values = []

        try:
            rows = int(self.rows_input.text())
            cols = int(self.cols_input.text())

            if rows <= 0 or cols <= 0:
                raise ValueError("O tamanho da matriz deve ser maior que 0.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro de Entrada", f"Entrada inválida: {str(e)}")
            return

        objective_layout = QHBoxLayout()
        objective_label = QLabel("Função Objetivo:")
        objective_layout.addWidget(objective_label)

        for col in range(cols):
            objective_field = QLineEdit()
            objective_field.setPlaceholderText(f"C{col + 1}")
            objective_layout.addWidget(objective_field)
            self.objective_values.append(objective_field)

        self.matrix_layout.addLayout(objective_layout)

        for row in range(rows):
            row_layout = QHBoxLayout()
            row_values = []

            for col in range(cols):
                matrix_field = QLineEdit()
                matrix_field.setPlaceholderText(f"({row + 1}, {col + 1})")
                row_layout.addWidget(matrix_field)
                row_values.append(matrix_field)

            self.matrix_values.append(row_values)

            inequality_box = QComboBox()
            inequality_box.addItems(["<=", ">=", "="])
            row_layout.addWidget(inequality_box)
            self.inequalities.append(inequality_box)

            value_field = QLineEdit()
            value_field.setPlaceholderText("Valor")
            row_layout.addWidget(value_field)
            self.final_values.append(value_field)

            self.matrix_layout.addLayout(row_layout)

        solve_tableau = QPushButton("Resolver Tableau")
        solve_tableau.clicked.connect(self.resolve_tableau)
        self.matrix_layout.addWidget(solve_tableau)

    def resolve_tableau(self):
        try:
            objective = self.objective_box.currentText()
            preferred_method = self.initial_solution_box.currentText()
            c = [Fraction(field.text()) for field in self.objective_values]
            A = [[Fraction(field.text()) for field in row] for row in self.matrix_values]
            D = [box.currentText() for box in self.inequalities]
            b = [Fraction(field.text()) for field in self.final_values]

            standard_form = StandardForm.execute({
                "A": A,
                "b": b,
                "D": D,
                "c": c,
                "objective": objective,
                "method": preferred_method
            })

            simplex_methods = SimplexMethods(standard_form)

            result = simplex_methods.execute()

            if result == PPL_INVIAVEL:
                self.show_results_window("PPL_INVIÁVEL", [], [], [])
            elif result == PPL_ILIMITADO:
                self.show_results_window("PPL_ILIMITADO", [], [], [])
            else:
                base_indices = result[1]
                optimal_value, base_values = result[4]()

                variable_names = [f"x{i + 1}" for i in range(len(c))]
                base_variable_names = [variable_names[i] for i in base_indices]

                self.show_results_window(
                    "Solução Ótima",
                    variable_names,
                    base_variable_names,
                    base_values,
                    optimal_value
                )

        except ValueError:
            QMessageBox.warning(
                self, "Erro",
                "Certifique-se de preencher todos os campos corretamente com valores numéricos ou frações válidas."
            )
        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico", f"Ocorreu um erro inesperado: {str(e)}")

    def show_results_window(self, status, variable_names=None, base_variable_names=None, base_values=None,
                            optimal_value=None):
        variable_names = variable_names
        base_variable_names = base_variable_names
        base_values = base_values
        optimal_value = optimal_value

        message = f"Status do Problema: {status}\n\n"

        if status == "Solução Ótima":
            message += f"Valor Ótimo da Função Objetivo: {format(abs(optimal_value), ".2f")}\n\n"
            message += "Variáveis Básicas:\n"
            for name, value in zip(base_variable_names, base_values):
                message += f"  {name} = {format(value, ".2f")}\n"
            message += "\nVariáveis Não-Básicas (Zeradas):\n"
            for name in set(variable_names) - set(base_variable_names):
                message += f"  {name} = 0\n"
        elif status == "PPL_INVIÁVEL":
            message += "O problema é inviável. Não existem soluções que atendam às restrições dadas."
        elif status == "PPL_ILIMITADO":
            message += "O problema é ilimitado. A função objetivo não possui um valor ótimo finito."

        QMessageBox.information(self, "Resultado", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainUi()
    main_window.show()
    sys.exit(app.exec())
