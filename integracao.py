import requests
from utilitarios import validar_inteiro

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
        print('2. Consultar endereço via CEP (API pública)')
        print('0. Voltar ao menu principal')

        opcao = validar_inteiro('Escolha uma opção: ')

        if opcao == 1:
            cep = input('Digite o CEP (somente números): ')
            consultar_cep(cep)
        elif opcao == 0:
            break
        else:
            print('❌ Opção inválida.')