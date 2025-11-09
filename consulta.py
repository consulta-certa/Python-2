import oracledb
import json
from utilitarios import getConnection,validar_string,validar_inteiro,validar_data, validar_id

#Operações CRUD
def create_consulta(id, especialidade, data_consulta, ativa, id_paciente):
    print('*** Inserindo uma nova Consulta na tabela cc_consultas ***')
    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO cc_consultas (id, especialidade, data_consulta, ativa, id_paciente)
            VALUES (:id, :especialidade, :data_consulta, :ativa, :id_paciente)
        """
        cursor.execute(sql, {
            'id' : id,
            'especialidade' : especialidade,
            'data_consulta' : data_consulta,
            'ativa' : ativa,
            'id_paciente' : id_paciente
        })
        conn.commit()
        print(f'A Consulta {id} de especialidade {especialidade} foi adicionada com sucesso!')
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
            SELECT id, especialidade , data_consulta, ativa, id_paciente
            FROM cc_consultas ORDER BY data_consulta DESC
        """
        cursor.execute(sql)
        print("\n --- Lista de Consultas ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Especialidade: {row[1]}, Data: {row[2].strftime("%d/%m/%Y %H:%M")}, Ativa: {row[3]}, ID Paciente: {row[4]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler Consultas: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de uma Consulta
def update_consulta(id, nova_especialidade, nova_data_consulta, nova_ativa, novo_id_paciente):
    print(f'Atualizando os dados da Consulta pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE cc_consultas
        SET especialidade = :nova_especialidade, data_consulta = :nova_data_consulta, ativa = :nova_ativa, id_paciente = :novo_id_paciente 
        WHERE id = :id
        """
        cursor.execute(sql, {'nova_especialidade' : nova_especialidade, 'nova_data_consulta' : nova_data_consulta, 'nova_ativa' :nova_ativa, 'novo_id_paciente' : novo_id_paciente, 'id': id})
        conn.commit()
        if cursor.rowcount >0:
            print(f' Os dados da consulta de ID {id} foram atualizados!')
        else:
            print(f'Nenhuma Consulta com ID {id} foi encontrada')


    except oracledb.Error as e:
        print(f'Erro ao atualizar Consulta {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove uma consulta pelo Id
def delete_consulta(id):
    print(f' Excluindo a Consulta com id: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """DELETE FROM cc_consultas WHERE id = :id"""
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A consulta {id} foi excluida com sucesso!')
        else:
            print(f'Nenhuma Consulta com ID {id} foi encontrada')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir Consulta: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

def exportar_consultas_json():
    '''
    Exporta todas as consultas cadastradas no banco Oracle
    para um arquivo local 'consultas.json'.
    '''
    print('\n📤 Exportando dados das consultas para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, especialidade, TO_CHAR(data_consulta, 'DD/MM/YYYY HH24:MI:SS') as data_formatada, ativa, id_paciente
            FROM cc_consultas ORDER BY data_consulta DESC
        """)
        rows = cursor.fetchall()

        consultas = [
            {'id': row[0], 'especialidade': row[1],'data_consulta': row[2],'ativa': row[3], 'id_paciente': row[4]}
            for row in rows
        ]

        with open('consultas.json', 'w', encoding='utf-8') as f:
            json.dump(consultas, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para consultas.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()


def validar_status_consulta():
    while True:
        status = input("Digite o status da consulta (s para ativa, n para inativa): ").lower()
        if status in ('s', 'n'):
            return status
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

#Programa Principal
def main_consulta():

    while True:

        print('\n**Menu - Consulta**')
        print('1. Agendar uma nova Consulta')
        print('2. Listar todas as Consultas')
        print('3. Atualizar os dados de uma Consulta')
        print('4. Excluir uma Consulta')
        print('5. Exportar Consultas para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao ==1:
            id = validar_id()
            especialidade = validar_string('Digite a especialidade da consulta: ', maximo=50)
            data_consulta = validar_data('Digite a data da consulta (DD/MM/AAAA HH:MM): ')
            ativa = validar_status_consulta()
            id_paciente = validar_string('Digite o ID do Paciente: ')
            create_consulta(id, especialidade, data_consulta, ativa, id_paciente)
    
        elif opcao==2:
            read_consulta()

        elif opcao==3:
            id = validar_string('Digite o Id da Consulta que deseja atualizar: ')
            nova_especialidade = validar_string('Digite a nova especialidade da Consulta: ', maximo=50)
            nova_data_consulta = validar_data('Digite a nova data da Consulta (DD/MM/AAAA HH:MM): ')
            nova_ativa = validar_status_consulta()
            novo_id_paciente = validar_string('Digite o novo Id do Paciente: ')
            update_consulta(id, nova_especialidade, nova_data_consulta, nova_ativa, novo_id_paciente)

        elif opcao==4:
            id = validar_string('Digite o Id da Consulta que deseja excluir: ')
            delete_consulta(id)

        elif opcao == 5:
            exportar_consultas_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_consulta()