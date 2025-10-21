import json
import requests
from utilitarios import validar_inteiro
from utilitarios import getConnection

def exportar_pacientes_json():
    '''
    Exporta todos os pacientes cadastrados no banco Oracle
    para um arquivo local 'pacientes.json'.
    '''
    print('\n📤 Exportando dados dos pacientes para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_paciente, nome , email, senha, telefone, acompanhante
            FROM pacientes ORDER BY id_paciente
        """)
        rows = cursor.fetchall()

        pacientes = [
            {'id_paciente': r[0], 'nome': r[1], 'email': r[2], 'telefone': r[3]}
            for r in rows
        ]

        with open('pacientes.json', 'w', encoding='utf-8') as f:
            json.dump(pacientes, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para pacientes.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()


def consultar_cep(cep):
    '''
    Consome a API pública ViaCEP e retorna os dados do endereço.
    Exemplo de CEP: 01001000
    '''
    print(f'\n🔎 Consultando informações do CEP {cep}...')
    url = f'https://viacep.com.br/ws/{cep}/json/'
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        if 'erro' in dados:
            print('CEP não encontrado.')
        else:
            print(f'CEP: {dados["cep"]}')
            print(f'Logradouro: {dados["logradouro"]}')
            print(f'Bairro: {dados["bairro"]}')
            print(f'Cidade: {dados["localidade"]}')
            print(f'UF: {dados["uf"]}')
    else:
        print('Erro ao consultar o CEP. Verifique sua conexão.')

def menu_integracoes():
    'Submenu para integração com JSON e API.'
    while True:
        print('\n--- Integrações ---')
        print('1. Exportar pacientes para JSON')
        print('2. Consultar endereço via CEP (API pública)')
        print('0. Voltar ao menu principal')

        opcao = validar_inteiro('Escolha uma opção: ')

        if opcao == 1:
            exportar_pacientes_json()
        elif opcao == 2:
            cep = input('Digite o CEP (somente números): ')
            consultar_cep(cep)
        elif opcao == 0:
            break
        else:
            print('❌ Opção inválida.')