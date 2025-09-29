import oracledb
from utilitarios import getConnection

'''
1.2. Cada ACOMPANHANTE deve ser representado com as chaves: id_acompanhante,
email, telefone, parentesco e nome.
'''
#Operações CRUD
def create_acompanhante(id_acompanhante, email, telefone, parentesco, nome):
    print('*** Inserindo um novo acompanhante na tabela acompanhante ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO acompanhantes (id_acompanhante, email, telefone, parentesco, nome)
            VALUES (:id_acompanhante, :email, :telefone, :parentesco, :nome)
        """
        cursor.execute(sql, {
            'id_acompanhante' : id_acompanhante,
            'nome' : nome,
            'email' : email,
            'telefone' : telefone,
            'parentesco' : parentesco
        })
        conn.commit()
        print(f' O acompanhante de ID: {id_acompanhante}, nome: {nome} email: {email}, telefone: {telefone} e grau de parentesco: {parentesco} foi adicionado com sucesso!')
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
            SELECT id_acompanhante, nome, email , telefone, parentesco,
            FROM acompanhantes ORDER BY id_acompanhante
        """
        cursor.execute(sql)
        print("\n --- Lista de acompanhantes ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'id: {row[0]}, nome: {row[1]}, email: {row[2]}, telefone: {row[3]} e grau de parentesco: {row[4]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler acompanhantes: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um acompanhante
def update_acompanhante(id_acompanhante, novo_email, novo_telefone, novo_parentesco, novo_nome):
    print(f'Atualizando os dados do acompanhante pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE acompanhantes
        set nome = :novo_nome, email = :novo_email, telefone = :novo_telefone, parentesco = :novo_parentesco WHERE id_acompanhante = :id_acompanhante
        
        """
        cursor.execute(sql, { 'novo_nome' : novo_nome, 'novo_email' : novo_email, 'novo_telefone' : novo_telefone, 'novo_parentesco' :novo_parentesco,'id_acompanhante': id_acompanhante})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O novo nome: {novo_nome}, novo email: {novo_email}, telefone: {novo_telefone} e grau parentesco: {novo_parentesco} do acompanhante de ID:{id_acompanhante} foram atualizados!')
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
        print('5. Encerrar o Programa')

        opcao=int(input('Digite uma opção: '))
        if opcao ==1:
            id_acompanhante = int(input('ID: '))
            nome=(input('nome: '))
            email = (input('email: '))
            telefone = (input('telefone: '))
            parentesco= (input('parentesco: '))
            create_acompanhante(id_acompanhante,nome,email,telefone,parentesco)
    
        elif opcao==2:
            read_acompanhante()

        elif opcao==3:
            id_acompanhante = int(input('Digite o Id do acompanhante: '))
            novo_nome = int(input('Digite o novo nome do acompanhante: '))
            novo_email = (input('Digite o novo email do acompanhante: '))
            novo_telefone = (input('Digite o novo telefone do acompanhante: '))
            novo_parentesco = (input('Digite o novo grau de parentesco: '))
            update_acompanhante(id_acompanhante,novo_nome,novo_email,novo_telefone,novo_parentesco,)

        elif opcao==4:
            id_acompanhante = int(input('Digite o Id do acompanhante: '))
            delete_acompanhante(id_acompanhante)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break

main_acompanhante