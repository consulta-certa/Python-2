import oracledb
from datetime import datetime
import regex
import re



'''
Lembrar de pip install regex
pip install oracledb
'''

#dominio = "oracle.fiap.com.br:1521/orcl"
""
#criar (obter) uma conexão com o banco de dados Oracle (FIAP)
def getConnection():
    try:
        conn = oracledb.connect(
            user = "RM566315",
            password = "050304",
            host = "oracle.fiap.com.br",
            port = "1521",
            service_name = "orcl"
            #dominio = dominio
        )
        print('Conexão com Oracle DB realizada!')
    except Exception as e:
        print(f'Erro ao obter a conexão: {e}')
    return conn

#valida numeros inteiros
def validar_inteiro(entrada: str) -> int:
    while True:
        try:
            valor = int(input(entrada))
            return valor
        except ValueError:
            print(f"Entrada inválida. Por favor, digite um número inteiro.")
 
# Importante: O oracledb espera o objeto datetime do Python

def validar_data(entrada: str): # Removi a dica de tipo -> bool, pois o retorno pode ser datetime ou False
    try:
        # 1. Tenta converter a string para um objeto datetime
        data = datetime.strptime(entrada, "%d/%m/%Y %H:%M") 
        
        # 2. Verifica se a data não está no passado (usando a data/hora atual)
        if data < datetime.now(): 
            print("Operação cancelada. Inserir apenas uma data válida a partir de hoje.")
            return False # Se for inválida (passado), retorna False
            
        # 3. Se tudo estiver OK (válida e futura), RETORNA O OBJETO DATETIME
        return data 
        
    except ValueError:
        # 4. Se o formato da string estiver errado
        print("Operação cancelada. Inserir apenas no formato exato 'DD/MM/AAAA HH:MM'.")
        return False


import re


def validar_nome(mensagem: str) -> str:
    """
    Solicita o nome do usuário, valida se contém apenas letras/espaços.
    Retorna o nome limpo (sem espaços extras) ou uma string vazia se for inválido.
    """
    while True:
        entrada = input(mensagem)

        # 1. Limpeza: Remove espaços no início e fim
        nome_tratado = entrada.strip()

        padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'

        if nome_tratado and re.fullmatch(padrao, nome_tratado):
            # 2. Retorna o nome limpo e validado
            return nome_tratado
        else:
            print("Operação cancelada. Inserir apenas letras válidas.")
            # O usuário deve tentar novamente no loop 'while True'

#valida email
def validar_email(mensagem: str) -> str:
    """
    Solicita e valida um e-mail do usuário, limpando-o e forçando minúsculas.
    Retorna o e-mail limpo ou uma string vazia/None se for inválido/cancelado.
    """
    padrao = r'^[\p{L}0-9._%+-]+@[\p{L}0-9.-]+\.[\p{L}]{2,}$'

    # 1. Solicita a entrada usando a mensagem (Se ela não estiver usando input)
    entrada = input(mensagem)

    # 2. LIMPEZA DOS DADOS: Remove espaços e força minúsculas
    email_tratado = entrada.strip().lower()

    if regex.fullmatch(padrao, email_tratado, flags=regex.UNICODE | regex.IGNORECASE):
        # 3. Retorna o e-mail TRATADO (limpo e em minúsculas)
        return email_tratado
    else:
        print("Operação cancelada. Digite um e-mail válido (ex: nome@dominio.com).")
        # Retorna uma string vazia ou levanta uma exceção para indicar falha
        return ""  # Melhor do que retornar um booleano aqui

#valida cep
def validar_cep(entrada: str) -> bool:
    padrao = r'^\d{5}-?\d{3}$'  # Aceita "12345678" ou "12345-678"
    
    if entrada and regex.fullmatch(padrao, entrada):
        return True
    else:
        print("Operação cancelada. Inserir um CEP válido (ex: 12345678 ou 12345-678).")
        return False


def validar_telefone(mensagem: str) -> str:
    """
    Solicita e valida um número de telefone no formato brasileiro.
    Retorna o telefone como string ou uma string vazia se inválido.
    """
    padrao = r'^(\(?\d{2}\)?[\s-]?)?(9\d{4}[\s-]?\d{4})$'

    while True:
        entrada = input(mensagem)

        # Limpa espaços e formatação para validação e armazenamento
        telefone_limpo = re.sub(r'[\s\(\)-]', '', entrada)

        # Usando o padrão modificado para verificar se o telefone limpo é válido
        # Se você quer validar o formato com os caracteres:
        # padrao = r'^(\(?\d{2}\)?[\s-]?)?(9\d{4}[\s-]?\d{4})$'
        # if regex.fullmatch(padrao, entrada):

        # Se preferir validar o número puro (11 dígitos):
        if len(telefone_limpo) == 11 and telefone_limpo.isdigit():
            return telefone_limpo  # Retorna o número puro (só dígitos)
        else:
            print("Operação cancelada. Inserir um telefone válido (ex: 11987654321 ou (11) 98765-4321).")
            # Se fosse para sair do loop em vez de tentar novamente:
            # return ""