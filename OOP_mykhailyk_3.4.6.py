class Polynom:
    def __init__(self, coeffs=None):
        if coeffs is None:
            self.coeffs = {}
        else:
            self.coeffs = coeffs.copy()

    @classmethod
    def from_file(cls, filename):
        coeffs = {}
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    power = int(parts[0])
                    coef = float(parts[1])
                    coeffs[power] = coef
        return cls(coeffs)

    def __str__(self):
        terms = []
        for power in sorted(self.coeffs.keys(), reverse=True):
            coef = self.coeffs[power]
            if coef == 0:
                continue
            if power == 0:
                terms.append(f"{coef}")
            elif power == 1:
                terms.append(f"{coef}*x")
            else:
                terms.append(f"{coef}*x^{power}")
        return " + ".join(terms) if terms else "0"

    def __call__(self, x):
        result = 0
        for power, coef in self.coeffs.items():
            result += coef * (x ** power)
        return result

    def __add__(self, other):
        result = self.coeffs.copy()
        for power, coef in other.coeffs.items():
            result[power] = result.get(power, 0) + coef
        return Polynom(result)

    def __sub__(self, other):
        result = self.coeffs.copy()
        for power, coef in other.coeffs.items():
            result[power] = result.get(power, 0) - coef
        return Polynom(result)

    def __mul__(self, other):
        result = {}
        for p1, c1 in self.coeffs.items():
            for p2, c2 in other.coeffs.items():
                result[p1 + p2] = result.get(p1 + p2, 0) + c1 * c2
        return Polynom(result)


class DifferentiablePolynom(Polynom):
    def derivative(self):
        result = {}
        for power, coef in self.coeffs.items():
            if power > 0:
                result[power - 1] = coef * power
        return DifferentiablePolynom(result)

    def second_derivative(self):
        return self.derivative().derivative()

    def integral(self):
        result = {}
        for power, coef in self.coeffs.items():
            result[power + 1] = coef / (power + 1)
        return DifferentiablePolynom(result)

if __name__ == '__main__':
    P1 = DifferentiablePolynom.from_file('input01.txt')
    P2 = DifferentiablePolynom.from_file('input02.txt')
    P3 = DifferentiablePolynom.from_file('input03.txt')
    P4 = DifferentiablePolynom.from_file('input04.txt')
    P5 = DifferentiablePolynom.from_file('input05.txt')
    P6 = DifferentiablePolynom.from_file('input06.txt')

    integrated = (P1 + (P2 * P3)).integral()
    deriv_part = P4.derivative() + P5.second_derivative()
    final_poly = integrated + (deriv_part * P6)

    print("Поліном P(x):")
    print(final_poly)

    x_value = 2
    print(f"\nP({x_value}) = {final_poly(x_value)}")
