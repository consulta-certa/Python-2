import oracledb
import json
from utilitarios import getConnection, validar_inteiro, validar_string, validar_data, validar_id

def create_acesso(id, funcionalidade, quantidade_acessos, tempo_permanencia_seg, data_acesso, id_paciente):
    """Registra um novo acesso e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_acessos_funcionalidade (id, funcionalidade, quantidade_acessos, tempo_permanencia_seg, data_acesso, id_paciente)
                    VALUES (:id, :funcionalidade, :quantidade_acessos, :tempo_permanencia_seg, :data_acesso, :id_paciente)
                """
                cursor.execute(sql, {
                    'id': id, 'funcionalidade': funcionalidade, 'quantidade_acessos': quantidade_acessos,
                    'tempo_permanencia_seg': tempo_permanencia_seg, 'data_acesso': data_acesso, 'id_paciente': id_paciente
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir acesso: {e}')
        return False

def read_acesso():
    """Lê e retorna uma lista de todos os acessos."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, funcionalidade, quantidade_acessos, tempo_permanencia_seg, TO_CHAR(data_acesso, 'DD/MM/YYYY HH24:MI:SS'), id_paciente FROM cc_acessos_funcionalidade ORDER BY id"
                cursor.execute(sql)
                acessos = []
                for row in cursor.fetchall():
                    acessos.append({
                        'id': row[0], 'funcionalidade': row[1], 'quantidade_acessos': row[2],
                        'tempo_permanencia_seg': row[3], 'data_acesso': row[4], 'id_paciente': row[5]
                    })
                return acessos
    except oracledb.Error as e:
        print(f'\n Erro ao ler acessos: {e}')
        return None

def update_acesso(id, nova_funcionalidade, nova_quantidade_acessos, novo_tempo_permanencia_seg, nova_data_acesso, novo_id_paciente):
    """Atualiza um acesso e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_acessos_funcionalidade
                    SET funcionalidade = :nova_funcionalidade, quantidade_acessos = :nova_quantidade_acessos,
                        tempo_permanencia_seg = :novo_tempo_permanencia_seg, data_acesso = :nova_data_acesso, id_paciente = :novo_id_paciente
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'nova_funcionalidade': nova_funcionalidade, 'nova_quantidade_acessos': nova_quantidade_acessos,
                    'novo_tempo_permanencia_seg': novo_tempo_permanencia_seg, 'nova_data_acesso': nova_data_acesso,
                    'novo_id_paciente': novo_id_paciente, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar acesso: {e}')
        return False

def delete_acesso(id):
    """Exclui um acesso e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_acessos_funcionalidade WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir acesso: {e}')
        return False

def exportar_acessos_json():
    """Exporta os acessos para JSON e retorna True em caso de sucesso."""
    print('\n📤 Exportando dados dos acessos para JSON...')
    acessos = read_acesso()
    if acessos is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not acessos:
        print("↪️ Nenhum acesso encontrado para exportar.")
        return True

    try:
        with open('acessos.json', 'w', encoding='utf-8') as f:
            json.dump(acessos, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para acessos.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_acesso():
    while True:
        print('\n**Menu - Acesso**')
        print('1. Inserir um novo acesso')
        print('2. Listar todos os acessos')
        print('3. Atualizar os dados de um acesso')
        print('4. Excluir um acesso')
        print('5. Exportar acessos para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo acesso ***')
            id = validar_id()
            funcionalidade = validar_string('Digite a Funcionalidade do acesso: ')
            quantidade_acessos = validar_inteiro('Digite a quantidade de acessos: ')
            tempo_permanencia_seg = validar_inteiro('Digite o tempo de permanencia em segundos: ')
            data_acesso = validar_data('Digite a data de acesso (DD/MM/AAAA HH:MM): ')
            id_paciente = validar_string('Digite o id do paciente: ')
            if create_acesso(id, funcionalidade, quantidade_acessos, tempo_permanencia_seg, data_acesso, id_paciente):
                print(f'\n O acesso à funcionalidade {funcionalidade} (ID: {id}) foi registrado com sucesso!')
            else:
                print('\n Falha ao registrar o acesso.')

        elif opcao == 2:
            print('\n*** Listando todos os acessos ***')
            acessos = read_acesso()
            if acessos is not None:
                if acessos:
                    print("\n--- Lista de Acessos ---")
                    for a in acessos:
                        print(f"ID: {a['id']}, Funcionalidade: {a['funcionalidade']}, Qtd. Acessos: {a['quantidade_acessos']}, "
                              f"Permanência (s): {a['tempo_permanencia_seg']}, Data: {a['data_acesso']}, ID Paciente: {a['id_paciente']}")
                        print('----------------------------------')
                else:
                    print("↪️ Nenhum acesso encontrado.")
            else:
                print(" Erro ao listar os acessos.")

        elif opcao == 3:
            print('\n*** Atualizando um acesso ***')
            id = validar_string('Digite o Id do acesso que deseja atualizar: ')
            nova_funcionalidade = validar_string('Digite a nova funcionalidade: ')
            nova_quantidade_acessos = validar_inteiro('Digite a nova quantidade de acessos: ')
            novo_tempo_permanencia_seg = validar_inteiro('Digite o novo tempo de permanência (s): ')
            nova_data_acesso = validar_data('Digite a nova data de acesso (DD/MM/AAAA HH:MM): ')
            novo_id_paciente = validar_string('Digite o novo id do paciente: ')

            if update_acesso(id, nova_funcionalidade, nova_quantidade_acessos, novo_tempo_permanencia_seg, nova_data_acesso, novo_id_paciente):
                print(f'\n Os dados do acesso {id} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum acesso com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um acesso ***')
            id = validar_string('Digite o Id do acesso que deseja excluir: ')
            if delete_acesso(id):
                print(f'\n O acesso {id} foi excluido com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum acesso com ID {id} foi encontrado ou ocorreu um erro.')
        
        elif opcao == 5:
            exportar_acessos_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_acesso()