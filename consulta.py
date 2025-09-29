'''

1.3. CONSULTAS devem ser representadas com as chaves: id_consulta, especialidade,
data_consulta Localdatetime, status e id_paciente.

'''

import oracledb
from utilitarios import getConnection

#Operações CRUD
def create_consulta(id_consulta, especialidade, data_consulta, status, id_paciente):
    print('*** Inserindo uma nova Consulta na tabela Consultas ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO consultas (id_consulta, especialidade, data_consulta, status, id_paciente)
            VALUES (:id_consulta, :especialidade, :data_consulta, :status, :id_paciente)
        """
        cursor.execute(sql, {
            'id_consulta' : id_consulta,
            'especialidade' : especialidade,
            'data_consulta' : data_consulta,
            'status' : status,
            'id_paciente' : id_paciente
        })
        conn.commit()
        print(f'A Consulta {id_consulta} de especialidade {especialidade} foi adicionada com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserior Consulta: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todas as Consultas
def read_consulta():
    print('*** Lê e exibe todos as Consultas da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id_consulta, especialidade , data_consulta, status, id_paciente
            FROM consultas ORDER BY id_consulta
        """
        cursor.execute(sql)
        print("\n --- Lista de Pacientes ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'id: {row[0]}, especialidade: {row[1]}, data_consulta: {row[2]}, status: {row[3]}, id_paciente: {row[4]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler Pacientes: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de uma Consulta
def update_consulta(id_consulta, nova_especialidade, nova_data_consulta, novo_status, novo_paciente):
    print(f'Atualizando os dados da Consulta pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE consultas
        set especialidade = :nova_especialidade, data_consulta = :nova_data_consulta, status = :novo_status, 
        id_paciente = :novo_paciente WHERE id_consulta = :id_consulta
        
        """
        cursor.execute(sql, {'nova_especialidade' : nova_especialidade, 'nova_data_consulta' : nova_data_consulta, 'novo_status' :novo_status, 'novo_paciente' : novo_paciente, 'id_consulta': id_consulta})
        conn.commit()
        if cursor.rowcount >0:
            print(f' A nova especialidade {nova_especialidade}, data_consulta{nova_data_consulta} e status{novo_status} do Paciente{id_consulta} foram atualizados!')
        else:
            print(f'Nenhuma Consulta com ID {id_consulta} foi encontrada')


    except oracledb.Error as e:
        print(f'Erro ao atualizar Consulta {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove uma consulta pelo Id

def delete_consulta(id_consulta):
    print(f' Excluindo a Consulta com id: {id_consulta}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM consultas WHERE 
        id_consulta=  :id_consulta
        """
        cursor.execute(sql, {'id_consulta' : id_consulta})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A consulta {id_consulta} foi excluida com sucesso!')
        else:
            print(f'Nenhuma Consulta com ID {id_consulta} foi encontrada')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir Consulta: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_consulta():

    while True:

        print('**Menu - Consulta**')
        print('1. Inserir uma nova Consulta')
        print('2. Listar todas as Consultas')
        print('3. Atualizar os dados de uma Consulta')
        print('4. Excluir uma Consulta')
        print('5. Encerrar o Programa')

        opcao=int(input('Digite uma opção: '))
        if opcao ==1:
            id_consulta = int(input('ID da Consulta: '))
            especialidade = (input('especialidade: '))
            data_consulta = (input('data da consulta: '))
            status= (input('status: '))
            id_paciente = int(input('ID do Paciente: '))
            create_consulta(id_consulta,especialidade,data_consulta,status, id_paciente)
    
        elif opcao==2:
            read_consulta()

        elif opcao==3:
            id_consulta = int(input('Digite o Id da Consulta: '))
            novo_especialidade = (input('Digite a nova especialidade da Consulta: '))
            novo_data_consulta = (input('Digite a nova data da Consulta: '))
            novo_status = (input('Digite o novo status: '))
            novo_paciente = int(input('Digite o novo Id do Paciente: '))
            update_consulta(id_consulta,novo_especialidade,novo_data_consulta,novo_status, novo_paciente)

        elif opcao==4:
            id_consulta = int(input('Digite o Id da Consulta: '))
            delete_consulta(id_consulta)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break

main_consulta
