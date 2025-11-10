import oracledb
import json
from utilitarios import getConnection, validar_string, validar_inteiro, validar_data, validar_id

def create_consulta(id, especialidade, data_consulta, ativa, id_paciente):
    """Agenda uma nova consulta e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_consultas (id, especialidade, data_consulta, ativa, id_paciente)
                    VALUES (:id, :especialidade, :data_consulta, :ativa, :id_paciente)
                """
                cursor.execute(sql, {
                    'id': id, 'especialidade': especialidade, 'data_consulta': data_consulta,
                    'ativa': ativa, 'id_paciente': id_paciente
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao agendar consulta: {e}')
        return False

def read_consulta():
    """Lê e retorna uma lista de todas as consultas."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, especialidade, data_consulta, ativa, id_paciente FROM cc_consultas ORDER BY data_consulta DESC"
                cursor.execute(sql)
                consultas = []
                for row in cursor.fetchall():
                    consultas.append({
                        'id': row[0], 'especialidade': row[1], 'data_consulta': row[2].strftime("%d/%m/%Y %H:%M"),
                        'ativa': row[3], 'id_paciente': row[4]
                    })
                return consultas
    except oracledb.Error as e:
        print(f'\n Erro ao ler consultas: {e}')
        return None

def update_consulta(id, nova_especialidade, nova_data_consulta, nova_ativa, novo_id_paciente):
    """Atualiza uma consulta e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_consultas
                    SET especialidade = :nova_especialidade, data_consulta = :nova_data_consulta,
                        ativa = :nova_ativa, id_paciente = :novo_id_paciente
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'nova_especialidade': nova_especialidade, 'nova_data_consulta': nova_data_consulta,
                    'nova_ativa': nova_ativa, 'novo_id_paciente': novo_id_paciente, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar consulta: {e}')
        return False

def delete_consulta(id):
    """Exclui uma consulta e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_consultas WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir consulta: {e}')
        return False

def exportar_consultas_json():
    """Exporta as consultas para JSON e retorna True em caso de sucesso."""
    print('\n📤 Exportando dados das consultas para JSON...')
    consultas = read_consulta()
    if consultas is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not consultas:
        print("↪️ Nenhuma consulta encontrada para exportar.")
        return True

    try:
        with open('consultas.json', 'w', encoding='utf-8') as f:
            json.dump(consultas, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para consultas.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def validar_status_consulta():
    while True:
        status = input("Digite o status da consulta (s para ativa, n para inativa): ").lower()
        if status in ('s', 'n'):
            return status
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

def main_consulta():
    while True:
        print('\n**Menu - Consulta**')
        print('1. Agendar uma nova Consulta')
        print('2. Listar todas as Consultas')
        print('3. Atualizar os dados de uma Consulta')
        print('4. Excluir uma Consulta')
        print('5. Exportar Consultas para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Agendando uma nova consulta ***')
            id = validar_id()
            especialidade = validar_string('Digite a especialidade da consulta: ')
            data_consulta = validar_data('Digite a data da consulta (DD/MM/AAAA HH:MM): ')
            ativa = validar_status_consulta()
            id_paciente = validar_string('Digite o ID do Paciente: ')
            if create_consulta(id, especialidade, data_consulta, ativa, id_paciente):
                print(f'\n Consulta {id} de especialidade {especialidade} foi agendada com sucesso!')
            else:
                print('\n Falha ao agendar a consulta.')

        elif opcao == 2:
            print('\n*** Listando todas as consultas ***')
            consultas = read_consulta()
            if consultas is not None:
                if consultas:
                    print("\n--- Lista de Consultas ---")
                    for c in consultas:
                        print(f"ID: {c['id']}, Especialidade: {c['especialidade']}, Data: {c['data_consulta']}, Ativa: {c['ativa']}, ID Paciente: {c['id_paciente']}")
                        print('----------------------------------')
                else:
                    print("↪️ Nenhuma consulta encontrada.")
            else:
                print(" Erro ao listar as consultas.")

        elif opcao == 3:
            print('\n*** Atualizando uma consulta ***')
            id = validar_string('Digite o Id da Consulta que deseja atualizar: ')
            nova_especialidade = validar_string('Digite a nova especialidade: ')
            nova_data_consulta = validar_data('Digite a nova data (DD/MM/AAAA HH:MM): ')
            nova_ativa = validar_status_consulta()
            novo_id_paciente = validar_string('Digite o novo Id do Paciente: ')
            
            if update_consulta(id, nova_especialidade, nova_data_consulta, nova_ativa, novo_id_paciente):
                print(f'\n Os dados da consulta {id} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhuma consulta com ID {id} foi encontrada ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo uma consulta ***')
            id = validar_string('Digite o Id da Consulta que deseja excluir: ')
            if delete_consulta(id):
                print(f'\n A consulta {id} foi excluida com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhuma consulta com ID {id} foi encontrada ou ocorreu um erro.')

        elif opcao == 5:
            exportar_consultas_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_consulta()