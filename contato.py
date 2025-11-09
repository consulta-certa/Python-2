import oracledb
import json
from utilitarios import getConnection,validar_inteiro,validar_string,validar_nome,validar_email,validar_telefone,validar_cep, validar_id


#Operações CRUD
def create_contato(id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem):
    print('*** Inserindo um novo contato na tabela cc_contatos_hc ***')
    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO cc_contatos_hc (id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem)
            VALUES (:id, :nome, :telefone, :email, :numero, :rua, :bairro, :cidade, :cep, :imagem)
        """
        cursor.execute(sql, {
            'id' : id,
            'nome' : nome,
            'telefone' : telefone,
            'email' : email,
            'numero' : numero,
            'rua' : rua,
            'bairro' : bairro,
            'cidade' : cidade,
            'cep' : cep,
            'imagem' : imagem
        })
        conn.commit()
        print(f' O contato de ID: {id}, nome: {nome} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir contato: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os contatos
def read_contato():
    print('*** Lê e exibe todos os contatos da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, nome , telefone, email, numero, rua, bairro, cidade, cep, imagem
            FROM cc_contatos_hc ORDER BY nome
        """
        cursor.execute(sql)
        print("\n --- Lista de contatos ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Nome: {row[1]}, Telefone: {row[2]}, Email: {row[3]}, Endereço: {row[5]}, {row[4]} - {row[6]}, {row[7]} - CEP: {row[8]}, Imagem: {row[9]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler contatos: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um contato
def update_contato(id, novo_nome, novo_telefone, novo_email, novo_numero, nova_rua, novo_bairro, nova_cidade, novo_cep, nova_imagem):
    print(f'Atualizando os dados do contato pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE cc_contatos_hc
        SET nome = :novo_nome, telefone = :novo_telefone, email = :novo_email, numero = :novo_numero, rua = :nova_rua, bairro = :novo_bairro, cidade = :nova_cidade, cep = :novo_cep, imagem = :nova_imagem WHERE id = :id
        """
        cursor.execute(sql, {'novo_nome' : novo_nome, 'novo_telefone' : novo_telefone, 'novo_email' :novo_email, 'novo_numero' : novo_numero, 'nova_rua' : nova_rua, 'novo_bairro' : novo_bairro, 'nova_cidade' : nova_cidade, 'novo_cep' : novo_cep, 'nova_imagem': nova_imagem, 'id': id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'Os dados do contato de ID {id} foram atualizados!')
        else:
            print(f'Nenhum contato com ID {id} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um contato pelo Id
def delete_contato(id):
    print(f' Excluindo o contato com id: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """DELETE FROM cc_contatos_hc WHERE id = :id"""
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'O contato de ID: {id} foi excluido com sucesso!')
        else:
            print(f'Nenhum contato com ID {id} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir contato: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

def exportar_contatos_json():
    '''
    Exporta todos os contatos cadastrados no banco Oracle
    para um arquivo local 'contatos.json'.
    '''
    print('\n📤 Exportando dados dos contatos para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem
            FROM cc_contatos_hc ORDER BY nome
        """)
        rows = cursor.fetchall()

        contatos = [
            {'id': row[0], 'nome': row[1],'telefone': row[2],'email': row[3], 'numero': row[4], 'rua': row[5], 'bairro': row[6], 'cidade': row[7], 'cep': row[8], 'imagem': row[9]}
            for row in rows
        ]

        with open('contatos.json', 'w', encoding='utf-8') as f:
            json.dump(contatos, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para contatos.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()

#Programa Principal
def main_contato():

    while True:

        print('\n**Menu - Contato HC**')
        print('1. Inserir um novo contato')
        print('2. Listar todos os contatos')
        print('3. Atualizar os dados de um contato')
        print('4. Excluir um contato')
        print('5. Exportar Contatos para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao ==1:
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
            create_contato(id, nome, telefone, email, numero, rua, bairro, cidade, cep, imagem)
    
        elif opcao==2:
            read_contato()

        elif opcao==3:
            id = validar_string('Digite o Id do contato que deseja atualizar: ')
            novo_nome = validar_nome('Digite o novo nome do contato: ')
            novo_telefone = validar_telefone('Digite o novo telefone do contato: ')
            novo_email = validar_email('Digite o novo email do contato: ')
            novo_numero = validar_string('Digite o novo número da residência: ')
            nova_rua = validar_string('Digite a nova rua: ')
            novo_bairro = validar_string('Digite o novo bairro: ')
            nova_cidade = validar_string('Digite a nova cidade: ')
            novo_cep = validar_cep('Digite o novo CEP (8 dígitos): ')
            nova_imagem = validar_string('Digite a nova URL da imagem: ')
            update_contato(id, novo_nome, novo_telefone, novo_email, novo_numero, nova_rua, novo_bairro, nova_cidade, novo_cep, nova_imagem)

        elif opcao==4:
            id = validar_string('Digite o Id do contato que deseja excluir: ')
            delete_contato(id)

        elif opcao == 5:
            exportar_contatos_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_contato()