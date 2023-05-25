import csv


class Input(object):
    def __init__(self, aparato, item_escolhido, preco, pagador, acertado):
        self.aparato = aparato
        self.item_escolhido = item_escolhido
        self.preco = preco
        self.pagador = pagador
        self.acertado = acertado

    def __str__(self):
        return f"""
            Aparato: {self.aparato}
            Item Escolhido: {self.item_escolhido}
            Preco: {self.preco}
            Pagador: {self.pagador}
            Acertado: {self.acertado}
        """


class Sheets(object):
    def __init__(self):
        self.inputs = []

    def add_input(self, input):
        self.inputs.append(input)

    def __str__(self):
        inputs_str = []
        for input in self.inputs:
            inputs_str.append(str(input))

        return "\n".join(inputs_str)


def read_balanco_sheets(sheets, balanco_file):
    with open(balanco_file) as f:
        balanco = csv.reader(f)

        next(balanco)
        for row in balanco:
            new_input = Input(
                aparato=row[2],
                item_escolhido=row[4],
                preco=row[5],
                pagador=row[7],
                acertado=row[8]
            )

            if new_input.aparato:
                sheets.add_input(new_input)


def convert_brl_to_number(brl):
    """Convert from BRL to float.

    Example: given "R$ 505,10" in BRL, it should "505.10" in float.

    :argument brl a BRL in string
    :returns a float number
    """
    prepared_brl = brl.split("R$ ")[1].replace(".", "").replace(",", ".")  # NOTE(peterson.bem) disgusting
    number = float(prepared_brl)

    return number


def payment_per_person(sheets, only_not_settled=False):
    payments = {}
    for input in sheets.inputs:
        total = payments[input.pagador] if input.pagador in payments else 0
        if not only_not_settled or not input.acertado:
            total += convert_brl_to_number(input.preco)
        payments[input.pagador] = total

    return payments


def payments_correction(payments):
    not_official_pagadores = { "Ambos", "-" }  # TODO(peterson.bem) replace with an enum
    official_pagadores = { k : payments[k] for k in set(payments) - not_official_pagadores }

    total = sum(official_pagadores.values())
    payment_per_person = total / len(official_pagadores)

    for pagador, paid in official_pagadores.items():
        official_pagadores[pagador] = payment_per_person - paid

    return official_pagadores


m_sheets = Sheets()
read_balanco_sheets(m_sheets, "balanco.csv")
print(m_sheets)
payments = payment_per_person(m_sheets, True)
print(f"Pagamentos: {payments}")
print(f"Pagamentos corrigidos: {payments_correction(payments)}")
