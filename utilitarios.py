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

# --- Valida Números Inteiros ---
def validar_inteiro(entrada: str) -> int:
    """
    Solicita um valor e garante que é um número inteiro, repetindo até ser válido.
    """
    while True:
        try:
            # Solicita a entrada dentro do loop
            valor = int(input(entrada))
            return valor
        except ValueError:
            print(f"Entrada inválida. Por favor, digite um número inteiro.")


# --- Valida Data e Hora (a partir de hoje) ---
def validar_data(mensagem: str) -> datetime:
    """
    Solicita uma data/hora no formato 'DD/MM/AAAA HH:MM' e valida se é futura ou atual.
    Repete até receber uma data/hora válida.
    """
    formato = "%d/%m/%Y %H:%M"
    while True:
        entrada = input(mensagem) # Solicita a entrada dentro do loop
        try:
            data = datetime.strptime(entrada, formato)
            
            # Compara a data inserida (sem segundos/microssegundos) com a data/hora atual
            # para evitar problemas de comparação de milissegundos.
            if data < datetime.now().replace(microsecond=0):
                print("Operação cancelada. Inserir apenas uma data/hora válida a partir de agora.")
            else:
                return data 
            
        except ValueError:
            print(f"Operação cancelada. Inserir apenas no formato exato '{formato}'.")


# --- Valida Nome ---
def validar_nome(mensagem: str) -> str:
    """
    Solicita o nome do usuário, valida se contém apenas letras/espaços.
    Repete até ser válido.
    """
    while True:
        entrada = input(mensagem)
        nome_tratado = entrada.strip()

        # Padrão para letras, incluindo acentos e espaços (ajustado para melhor cobertura Unicode)
        padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$' 

        if nome_tratado and re.fullmatch(padrao, nome_tratado):
            return nome_tratado
        else:
            print("Operação cancelada. Inserir apenas letras válidas.")


# --- Valida E-mail ---
def validar_email(mensagem: str) -> str:
    """
    Solicita e valida um e-mail do usuário. Repete até ser válido.
    Retorna o e-mail limpo e em minúsculas.
    """
    # Padrão mais robusto, requer a biblioteca 'regex' para \p{L}
    # Se usar apenas 're', use: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    padrao = r'^[\p{L}0-9._%+-]+@[\p{L}0-9.-]+\.[\p{L}]{2,}$'

    while True:
        entrada = input(mensagem)
        email_tratado = entrada.strip().lower()

        # Usa regex.fullmatch, que é mais robusto para UNICODE. 
        # Se usar 're', remova o 'flags' ou use re.IGNORECASE.
        if regex.fullmatch(padrao, email_tratado, flags=regex.UNICODE | regex.IGNORECASE):
            return email_tratado
        else:
            print("Operação cancelada. Digite um e-mail válido (ex: nome@dominio.com).")


# --- Valida CEP ---
def validar_cep(mensagem: str) -> str:
    """
    Solicita e valida um CEP no formato 8 dígitos opcionalmente com hífen. Repete até ser válido.
    Retorna o CEP como string (sem higienização automática).
    """
    padrao = r'^\d{5}-?\d{3}$'
    
    while True:
        entrada = input(mensagem)
        # O código original usava 'regex.fullmatch', mantendo a compatibilidade com 'regex'
        if entrada and regex.fullmatch(padrao, entrada):
            return entrada
        else:
            print("Operação cancelada. Inserir um CEP válido (ex: 12345678 ou 12345-678).")


# --- Valida Telefone (11 dígitos, formato brasileiro) ---
def validar_telefone(mensagem: str) -> str:
    """
    Solicita e valida um número de telefone no formato brasileiro (11 dígitos).
    Retorna o telefone apenas com dígitos. Repete até ser válido.
    """
    # Padrão que aceita formatos comuns, mas a validação final será por comprimento
    # (Ex: (11) 98765-4321 ou 11987654321)
    
    while True:
        entrada = input(mensagem)

        # Remove todos os caracteres não numéricos: espaços, parênteses e hífens
        telefone_limpo = re.sub(r'[\s\(\)-]', '', entrada)
        
        # Valida se tem exatamente 11 dígitos e são todos numéricos
        if len(telefone_limpo) == 11 and telefone_limpo.isdigit():
            return telefone_limpo
        else:
            print("Operação cancelada. Inserir um telefone válido (ex: 11987654321 ou (11) 98765-4321).")
            
def validar_booleano(mensagem: str) -> bool:
    """
    Solicita uma entrada e força uma resposta booleana (True ou False).
    Aceita 's', 'n', 'sim', 'nao', 'true', 'false' (case-insensitive).
    Repete a solicitação até receber uma entrada válida.
    """
    while True:
        entrada = input(mensagem).strip().lower() # Limpa e converte para minúsculas

        # Define as respostas que significam True
        if entrada in ('s', 'sim', 'true', '1', 'ok', 'S', 'SIM'):
            return True
        
        # Define as respostas que significam False
        elif entrada in ('n', 'não', 'nao', 'false', '0', 'cancelar', 'NAO', 'NÃO'):
            return False
            
        # Se não for uma resposta válida, informa o erro e o loop repete
        else:
            print("Entrada inválida. Por favor, digite 'sim' ou 'não' (ou variações como 's'/'n').")

def validar_string(mensagem: str, minimo: int = 1, maximo: int = 100) -> str:
    """
    Solicita uma string ao usuário e garante que ela não está vazia e está dentro
    de um comprimento mínimo e máximo. Repete até ser válida.
    """
    while True:
        entrada = input(mensagem)
        # 1. Remove espaços em branco do início e fim
        string_tratada = entrada.strip()
        
        tamanho = len(string_tratada)

        # 2. Verifica se está vazia ou contém apenas espaços
        if not string_tratada:
            print("Entrada inválida. O campo não pode ficar vazio.")
            continue # Volta para o início do loop

        # 3. Verifica o comprimento
        if tamanho < minimo:
            print(f"Entrada inválida. O valor deve ter pelo menos {minimo} caracteres.")
        elif tamanho > maximo:
            print(f"Entrada inválida. O valor deve ter no máximo {maximo} caracteres.")
        
        # 4. Se passar por todas as verificações, retorna
        else:
            return string_tratada