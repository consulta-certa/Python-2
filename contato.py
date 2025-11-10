import oracledb
import json
from utilitarios import getConnection, validar_inteiro, validar_string, validar_nome, validar_email, validar_telefone, validar_cep, validar_id

def create_contato(id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem):
    """Cria um novo contato e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_contatos_hc (id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem)
                    VALUES (:id, :nome, :telefone, :email, :numero, :rua, :bairro, :cidade, :cep, :imagem)
                """
                cursor.execute(sql, {
                    'id': id, 'nome': nome, 'telefone': telefone, 'email': email, 'numero': numero,
                    'rua': rua, 'bairro': bairro, 'cidade': cidade, 'cep': cep, 'imagem': imagem
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao criar contato: {e}')
        return False

def read_contato():
    """Lê e retorna uma lista de todos os contatos."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem FROM cc_contatos_hc ORDER BY nome"
                cursor.execute(sql)
                contatos = []
                for row in cursor.fetchall():
                    contatos.append({
                        'id': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3], 'numero': row[4],
                        'rua': row[5], 'bairro': row[6], 'cidade': row[7], 'cep': row[8], 'imagem': row[9]
                    })
                return contatos
    except oracledb.Error as e:
        print(f'\n Erro ao ler contatos: {e}')
        return None

def update_contato(id, novo_nome, novo_telefone, novo_email, novo_numero, nova_rua, novo_bairro, nova_cidade, novo_cep, nova_imagem):
    """Atualiza um contato e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_contatos_hc
                    SET nome = :novo_nome, telefone = :novo_telefone, email = :novo_email, numero = :novo_numero,
                        rua = :nova_rua, bairro = :novo_bairro, cidade = :nova_cidade, cep = :novo_cep, imagem = :nova_imagem
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'novo_nome': novo_nome, 'novo_telefone': novo_telefone, 'novo_email': novo_email,
                    'novo_numero': novo_numero, 'nova_rua': nova_rua, 'novo_bairro': novo_bairro,
                    'nova_cidade': nova_cidade, 'novo_cep': novo_cep, 'nova_imagem': nova_imagem, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar contato: {e}')
        return False

def delete_contato(id):
    """Exclui um contato e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_contatos_hc WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir contato: {e}')
        return False

def exportar_contatos_json():
    """Exporta os contatos para JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados dos contatos para JSON...')
    contatos = read_contato()
    if contatos is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not contatos:
        print(" Nenhum contato encontrado para exportar.")
        return True

    try:
        with open('contatos.json', 'w', encoding='utf-8') as f:
            json.dump(contatos, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para contatos.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_contato():
    while True:
        print('\n**Menu - Contato HC**')
        print('1. Inserir um novo contato')
        print('2. Listar todos os contatos')
        print('3. Atualizar os dados de um contato')
        print('4. Excluir um contato')
        print('5. Exportar Contatos para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo contato ***')
            id = validar_id()
            nome = validar_nome('Digite o nome do contato: ')
            telefone = validar_telefone('Digite o telefone do contato: ')
            email = validar_email('Digite o email do contato: ')
            numero = validar_string('Digite o número da residência: ')
            rua = validar_string('Digite a rua: ')
            bairro = validar_string('Digite o bairro: ')
            cidade = validar_string('Digite a cidade: ')
            cep = validar_cep('Digite o CEP (8 dígitos): ')
            imagem = validar_string('Digite a URL da imagem: ')
            if create_contato(id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem):
                print(f'\n O contato {nome} (ID: {id}) foi adicionado com sucesso!')
            else:
                print('\n Falha ao adicionar o contato.')

        elif opcao == 2:
            print('\n*** Listando todos os contatos ***')
            contatos = read_contato()
            if contatos is not None:
                if contatos:
                    print("\n--- Lista de Contatos ---")
                    for c in contatos:
                        print(f"ID: {c['id']}, Nome: {c['nome']}, Telefone: {c['telefone']}, Email: {c['email']}")
                        print(f"Endereço: {c['rua']}, {c['numero']} - {c['bairro']}, {c['cidade']} - CEP: {c['cep']}")
                        print(f"Imagem: {c['imagem']}")
                        print('----------------------------------')
                else:
                    print(" Nenhum contato encontrado.")
            else:
                print(" Erro ao listar os contatos.")

        elif opcao == 3:
            print('\n*** Atualizando um contato ***')
            id = validar_string('Digite o Id do contato que deseja atualizar: ')
            novo_nome = validar_nome('Digite o novo nome: ')
            novo_telefone = validar_telefone('Digite o novo telefone: ')
            novo_email = validar_email('Digite o novo email: ')
            novo_numero = validar_string('Digite o novo número da residência: ')
            nova_rua = validar_string('Digite a nova rua: ')
            novo_bairro = validar_string('Digite o novo bairro: ')
            nova_cidade = validar_string('Digite a nova cidade: ')
            novo_cep = validar_cep('Digite o novo CEP (8 dígitos): ')
            nova_imagem = validar_string('Digite a nova URL da imagem: ')

            if update_contato(id, novo_nome, novo_telefone, novo_email, novo_numero, nova_rua, novo_bairro, nova_cidade, novo_cep, nova_imagem):
                print(f'\n Os dados do contato {id} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum contato com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um contato ***')
            id = validar_string('Digite o Id do contato que deseja excluir: ')
            if delete_contato(id):
                print(f'\n O contato {id} foi excluído com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum contato com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 5:
            exportar_contatos_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_contato()