import oracledb
import json
from utilitarios import getConnection,validar_inteiro,validar_string,validar_nome,validar_email,validar_telefone, validar_id


#Operações CRUD
def create_acompanhante(id, nome, email, telefone, parentesco, id_paciente):
    print('*** Inserindo um novo acompanhante na tabela cc_acompanhantes ***')
    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO cc_acompanhantes (id, nome, email, telefone, parentesco, id_paciente)
            VALUES (:id, :nome, :email, :telefone, :parentesco, :id_paciente)
        """
        cursor.execute(sql, {
            'id' : id,
            'nome' : nome,
            'email' : email,
            'telefone' : telefone,
            'parentesco' : parentesco,
            'id_paciente' : id_paciente
        })
        conn.commit()
        print(f' O acompanhante de ID: {id}, nome: {nome}, email: {email}, telefone: {telefone}, grau de parentesco: {parentesco} do paciente de id {id_paciente} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir acompanhante: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os acompanhantes
def read_acompanhante():
    print('*** Lê e exibe todos os acompanhantes da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, nome, email , telefone, parentesco, id_paciente
            FROM cc_acompanhantes ORDER BY nome
        """
        cursor.execute(sql)
        print("\n --- Lista de acompanhantes ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Nome: {row[1]}, Email: {row[2]}, Telefone: {row[3]}, Parentesco: {row[4]}, ID do Paciente: {row[5]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler acompanhantes: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um acompanhante
def update_acompanhante(id, novo_nome, novo_email, novo_telefone, novo_parentesco, novo_id_paciente):
    print(f'Atualizando os dados do acompanhante pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE cc_acompanhantes
        SET nome = :novo_nome, email = :novo_email, telefone = :novo_telefone, parentesco = :novo_parentesco, id_paciente = :novo_id_paciente WHERE id = :id
        """
        cursor.execute(sql, {'novo_nome' : novo_nome, 'novo_email' : novo_email, 'novo_telefone' : novo_telefone, 'novo_parentesco' :novo_parentesco, 'novo_id_paciente' : novo_id_paciente, 'id': id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'Os dados do acompanhante de ID {id} foram atualizados!')
        else:
            print(f'Nenhum acompanhante com ID {id} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um acompanhante pelo Id
def delete_acompanhante(id):
    print(f' Excluindo o acompanhante com id: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """DELETE FROM cc_acompanhantes WHERE id = :id"""
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'O acompanhante de ID: {id} foi excluido com sucesso!')
        else:
            print(f'Nenhum acompanhante com ID {id} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir acompanhante: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()


def exportar_acompanhantes_json():
    '''
    Exporta todos os acompanhantes cadastrados no banco Oracle
    para um arquivo local 'acompanhantes.json'.
    '''
    print('\n📤 Exportando dados dos acompanhantes para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, email , telefone, parentesco, id_paciente
            FROM cc_acompanhantes ORDER BY nome
        """)
        rows = cursor.fetchall()

        acompanhantes = [
            {'id': row[0], 'nome': row[1], 'email': row[2],'telefone': row[3],'parentesco': row[4], 'id_paciente': row[5]}
            for row in rows
        ]

        with open('acompanhantes.json', 'w', encoding='utf-8') as f:
            json.dump(acompanhantes, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para acompanhantes.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()

#Programa Principal
def main_acompanhante():

    while True:

        print('\n**Menu - Acompanhante**')
        print('1. Inserir um novo acompanhante')
        print('2. Listar todos os acompanhantes')
        print('3. Atualizar os dados de um acompanhante')
        print('4. Excluir um acompanhante')
        print('5. Exportar Acompanhantes para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao ==1:
            id = validar_id()
            nome = validar_nome('Digite o nome do acompanhante: ')
            email = validar_email('Digite o email do acompanhante: ')
            telefone = validar_telefone('Digite o telefone do acompanhante: ')
            parentesco = validar_string('Digite o grau de parentesco do acompanhante: ')
            id_paciente = validar_string('Digite o ID do paciente relacionado: ')
            create_acompanhante(id, nome, email, telefone, parentesco, id_paciente)
    
        elif opcao==2:
            read_acompanhante()

        elif opcao==3:
            id = validar_string('Digite o Id do acompanhante que deseja atualizar: ')
            novo_nome = validar_nome('Digite o novo nome do acompanhante: ')
            novo_email = validar_email('Digite o novo email do acompanhante: ')
            novo_telefone = validar_telefone('Digite o novo telefone do acompanhante: ')
            novo_parentesco = validar_string('Digite o novo grau de parentesco do acompanhante: ')
            novo_id_paciente = validar_string('Digite o novo ID do paciente relacionado: ')
            update_acompanhante(id, novo_nome, novo_email, novo_telefone, novo_parentesco, novo_id_paciente)

        elif opcao==4:
            id = validar_string('Digite o Id do acompanhante que deseja excluir: ')
            delete_acompanhante(id)
    
        elif opcao == 5:
            exportar_acompanhantes_json()

        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_acompanhante()