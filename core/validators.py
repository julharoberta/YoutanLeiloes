
import re


def somente_digitos(documento):
    """Remove pontos, barras, traços e outros caracteres não numéricos."""
    return re.sub(r"\D", "", str(documento or ""))


def cpf_valido(documento):
    """Verifica os dígitos verificadores de um CPF."""
    cpf = somente_digitos(documento)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for tamanho in (9, 10):
        soma = sum(
            int(digito) * peso
            for digito, peso in zip(cpf[:tamanho], range(tamanho + 1, 1, -1))
        )
        resto = (soma * 10) % 11
        digito_calculado = 0 if resto == 10 else resto

        if digito_calculado != int(cpf[tamanho]):
            return False

    return True


def cnpj_valido(documento):
    """Verifica os dígitos verificadores de um CNPJ."""
    cnpj = somente_digitos(documento)

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    pesos = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)

    soma = sum(
        int(digito) * peso
        for digito, peso in zip(cnpj[:12], pesos)
    )
    resto = soma % 11
    primeiro = 0 if resto < 2 else 11 - resto

    if primeiro != int(cnpj[12]):
        return False

    pesos = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)

    soma = sum(
        int(digito) * peso
        for digito, peso in zip(cnpj[:13], pesos)
    )
    resto = soma % 11
    segundo = 0 if resto < 2 else 11 - resto

    return segundo == int(cnpj[13])
