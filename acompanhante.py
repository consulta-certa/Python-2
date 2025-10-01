import oracledb
from utilitarios import getConnection,validar_inteiro,validar_string,validar_nome,validar_email,validar_telefone


'''
1.2. Cada ACOMPANHANTE deve ser representado com as chaves: id_acompanhante,
email, telefone, parentesco e nome e id_paciente?
'''
#Operações CRUD
def create_acompanhante(id_acompanhante, email, telefone, parentesco, id_paciente, nome):
    print('*** Inserindo um novo acompanhante na tabela acompanhante ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO acompanhantes (id_acompanhante, email, telefone, parentesco, id_paciente, nome)
            VALUES (:id_acompanhante, :email, :telefone, :parentesco, :id_paciente, :nome)
        """
        cursor.execute(sql, {
            'id_acompanhante' : id_acompanhante,
            'email' : email,
            'telefone' : telefone,
            'parentesco' : parentesco,
            'id_paciente' : id_paciente,
            'nome' : nome
        })
        conn.commit()
        print(f' O acompanhante de ID: {id_acompanhante}, nome: {nome} email: {email}, telefone: {telefone}, grau de parentesco: {parentesco} do paciente de id{id_paciente}foi adicionado com sucesso!')
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
            SELECT id_acompanhante, email , telefone, parentesco, id_paciente, nome
            FROM acompanhantes ORDER BY id_acompanhante
        """
        cursor.execute(sql)
        print("\n --- Lista de acompanhantes ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID acompanhante: {row[0]}, email: {row[1]}, telefone: {row[2]}, grau de parentesco: {row[3]}, ID do paciente: {row[4]} e nome: {row[5]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler acompanhantes: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um acompanhante
def update_acompanhante(id_acompanhante, novo_email, novo_telefone, novo_parentesco, novo_id_paciente, novo_nome):
    print(f'Atualizando os dados do acompanhante pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE acompanhantes
        SET email = :novo_email, telefone = :novo_telefone, parentesco = :novo_parentesco, id_paciente = :novo_id_paciente, nome = :novo_nome WHERE id_acompanhante = :id_acompanhante
        
        """
        cursor.execute(sql, {'novo_email' : novo_email, 'novo_telefone' : novo_telefone, 'novo_parentesco' :novo_parentesco, 'novo_id_paciente' : novo_id_paciente,'novo_nome' : novo_nome, 'id_acompanhante': id_acompanhante})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O novo email: {novo_email}, telefone: {novo_telefone} e grau parentesco: {novo_parentesco}, relacionado com o paciente ID: {novo_id_paciente} e nome: {novo_nome} do acompanhante de ID:{id_acompanhante} foram atualizados!')
        else:
            print(f'Nenhum acompanhante com ID {id_acompanhante} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um acompanhante pelo Id

def delete_acompanhante(id_acompanhante):
    print(f' Excluindo o acompanhante com id: {id_acompanhante}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM acompanhantes WHERE 
        id_acompanhante=  :id_acompanhante
        """
        cursor.execute(sql, {'id_acompanhante' : id_acompanhante})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O acompanhante de ID: {id_acompanhante} foi excluido com sucesso!')
        else:
            print(f'Nenhum acompanhante com ID {id_acompanhante} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir acompanhante: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_acompanhante():

    while True:

        print('**Menu - acompanhante**')
        print('1. Inserir um novo acompanhante')
        print('2. Listar todos os acompanhantes')
        print('3. Atualizar os dados de um acompanhante')
        print('4. Excluir um acompanhante')
        print('5. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id_acompanhante = validar_inteiro('Digite o ID do acompanhante: ')
            email = validar_email('Digite o email do acompanhante: ')
            telefone = validar_telefone('Digite o telefone do acompanhante: ')
            parentesco = validar_string('Digite o grau de parentesco do acompanhante: ')
            id_paciente = validar_inteiro('Digite o ID do paciente relacionado: ')
            nome = validar_nome('Digite o nome do acompanhante: ')
            create_acompanhante(id_acompanhante,email,telefone,parentesco,id_paciente,nome)
    
        elif opcao==2:
            read_acompanhante()

        elif opcao==3:
            id_acompanhante = validar_inteiro('Digite o Id do acompanhante: ')
            novo_email = validar_email('Digite o novo email do acompanhante: ')
            novo_telefone = validar_telefone('Digite o novo telefone do acompanhante: ')
            novo_parentesco = validar_string('Digite o novo grau de parentesco do acompanhante: ')
            novo_id_paciente = validar_inteiro('Digite o novo ID do paciente relacionado: ')
            novo_nome = validar_nome('Digite o novo nome do acompanhante: ')
            update_acompanhante(id_acompanhante,novo_email,novo_telefone,novo_parentesco,novo_id_paciente,novo_nome)

        elif opcao==4:
            id_acompanhante = validar_inteiro('Digite o Id do acompanhante: ')
            delete_acompanhante(id_acompanhante)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 1 e 5.")
            
main_acompanhante