import oracledb
import json
from utilitarios import getConnection, validar_string, validar_inteiro, validar_data, validar_id

def create_lembrete(id, data_envio, enviado, id_consulta):
    """Cria um novo lembrete e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_lembretes (id, data_envio, enviado, id_consulta)
                    VALUES (:id, :data_envio, :enviado, :id_consulta)
                """
                cursor.execute(sql, {
                    'id': id, 'data_envio': data_envio, 'enviado': enviado, 'id_consulta': id_consulta
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao criar lembrete: {e}')
        return False

def read_lembrete():
    """Lê e retorna uma lista de todos os lembretes."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, data_envio, enviado, id_consulta FROM cc_lembretes ORDER BY data_envio DESC"
                cursor.execute(sql)
                lembretes = []
                for row in cursor.fetchall():
                    lembretes.append({
                        'id': row[0], 'data_envio': row[1].strftime("%d/%m/%Y %H:%M"),
                        'enviado': row[2], 'id_consulta': row[3]
                    })
                return lembretes
    except oracledb.Error as e:
        print(f'\n Erro ao ler lembretes: {e}')
        return None

def update_lembrete(id, nova_data_envio, novo_enviado, novo_id_consulta):
    """Atualiza um lembrete e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_lembretes
                    SET data_envio = :nova_data_envio, enviado = :novo_enviado, id_consulta = :novo_id_consulta
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'nova_data_envio': nova_data_envio, 'novo_enviado': novo_enviado,
                    'novo_id_consulta': novo_id_consulta, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar lembrete: {e}')
        return False

def delete_lembrete(id):
    """Exclui um lembrete e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_lembretes WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir lembrete: {e}')
        return False

def exportar_lembretes_json():
    """Exporta os lembretes para JSON e retorna True em caso de sucesso."""
    print('\n📤 Exportando dados dos lembretes para JSON...')
    lembretes = read_lembrete()
    if lembretes is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not lembretes:
        print("↪️ Nenhum lembrete encontrado para exportar.")
        return True

    try:
        with open('lembretes.json', 'w', encoding='utf-8') as f:
            json.dump(lembretes, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para lembretes.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def validar_enviado():
    while True:
        enviado = input("O lembrete foi enviado? (s/n): ").lower()
        if enviado in ('s', 'n'):
            return enviado
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

def main_lembrete():
    while True:
        print('\n**Menu - Lembretes de Consulta**')
        print('1. Inserir um novo lembrete')
        print('2. Listar todos os lembretes')
        print('3. Atualizar os dados de um lembrete')
        print('4. Excluir um lembrete')
        print('5. Exportar Lembretes para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo lembrete ***')
            id = validar_id()
            data_envio = validar_data('Digite a data e hora de envio (DD/MM/AAAA HH:MM): ')
            enviado = validar_enviado()
            id_consulta = validar_string('Digite o ID da consulta relacionada: ')
            if create_lembrete(id, data_envio, enviado, id_consulta):
                print(f'\n Lembrete {id} da consulta {id_consulta} foi adicionado com sucesso!')
            else:
                print('\n Falha ao adicionar o lembrete.')

        elif opcao == 2:
            print('\n*** Listando todos os lembretes ***')
            lembretes = read_lembrete()
            if lembretes is not None:
                if lembretes:
                    print("\n--- Lista de Lembretes ---")
                    for l in lembretes:
                        print(f"ID: {l['id']}, Data Envio: {l['data_envio']}, Enviado: {l['enviado']}, ID Consulta: {l['id_consulta']}")
                        print('----------------------------------')
                else:
                    print("↪️ Nenhum lembrete encontrado.")
            else:
                print(" Erro ao listar os lembretes.")

        elif opcao == 3:
            print('\n*** Atualizando um lembrete ***')
            id = validar_string('Digite o Id do lembrete que deseja atualizar: ')
            nova_data_envio = validar_data('Digite a nova data e hora de envio (DD/MM/AAAA HH:MM): ')
            novo_enviado = validar_enviado()
            novo_id_consulta = validar_string('Digite o novo ID da consulta relacionada: ')
            
            if update_lembrete(id, nova_data_envio, novo_enviado, novo_id_consulta):
                print(f'\n Os dados do lembrete {id} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum lembrete com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um lembrete ***')
            id = validar_string('Digite o Id do lembrete que deseja excluir: ')
            if delete_lembrete(id):
                print(f'\n O lembrete {id} foi excluido com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum lembrete com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 5:
            exportar_lembretes_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_lembrete()