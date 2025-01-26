import numpy as np

type StandardFormProps = {
    "A": [],
    "b":[],
    "c":[],
    "D":[],
    "objective":[]
}
class StandardForm:

    @staticmethod
    def execute(props:StandardFormProps) -> StandardFormProps:

        A = props["A"]
        b = props["b"]
        c = props["c"]
        D = props["D"]
        objective = props["objective"]

        for index,inequality in enumerate(D):
            if inequality == "=":
                continue
            if inequality == "<=":
                A[index].append(1)
            if inequality == ">=":
                A[index].append(-1)
            for zeros,element in enumerate(A):
                if zeros != index:
                    element.append(0)
            c.append(0)

        for index,inequality in enumerate(D):
            if inequality == ">=" or inequality == "=":
                A[index].append(1)
                c.append(0)
                for zeros, element in enumerate(A):
                    if zeros != index:
                        element.append(0)

        if objective == "Maximizar":
            props['c'] = [element * -1 for element in c]

        return {
            "A": np.array(A),
            "b": np.array(b),
            "c": np.array(props['c']),
            "D": D,
            "objective": objective,
            "method": props["method"]
        }
