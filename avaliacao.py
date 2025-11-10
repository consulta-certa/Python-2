import oracledb
import json
from utilitarios import getConnection, validar_string, validar_inteiro, validar_data, validar_id

def create_avaliacao(id, nota, comentario, data_avaliacao):
    """Cria uma nova avaliação e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_avaliacoes (id, nota, comentario, data_avaliacao)
                    VALUES (:id, :nota, :comentario, :data_avaliacao)
                """
                cursor.execute(sql, {
                    'id': id, 'nota': nota, 'comentario': comentario, 'data_avaliacao': data_avaliacao
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir avaliação: {e}')
        return False

def read_avaliacao():
    """Lê e retorna uma lista de todas as avaliações."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, nota, comentario, TO_CHAR(data_avaliacao, 'DD/MM/YYYY') FROM cc_avaliacoes ORDER BY data_avaliacao DESC"
                cursor.execute(sql)
                avaliacoes = []
                for row in cursor.fetchall():
                    avaliacoes.append({
                        'id': row[0], 'nota': row[1], 'comentario': row[2], 'data_avaliacao': row[3]
                    })
                return avaliacoes
    except oracledb.Error as e:
        print(f'\n Erro ao ler as avaliações: {e}')
        return None

def update_avaliacao(id, nova_nota, novo_comentario, nova_data_avaliacao):
    """Atualiza uma avaliação e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_avaliacoes
                    SET nota = :nova_nota, comentario = :novo_comentario, data_avaliacao = :nova_data_avaliacao
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'nova_nota': nova_nota, 'novo_comentario': novo_comentario,
                    'nova_data_avaliacao': nova_data_avaliacao, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar avaliação: {e}')
        return False

def delete_avaliacao(id):
    """Exclui uma avaliação e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_avaliacoes WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir avaliação: {e}')
        return False

def exportar_avaliacoes_json():
    """Exporta as avaliações para JSON e retorna True em caso de sucesso."""
    print('\n📤 Exportando dados das avaliações para JSON...')
    avaliacoes = read_avaliacao()
    if avaliacoes is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not avaliacoes:
        print("↪️ Nenhuma avaliação encontrada para exportar.")
        return True

    try:
        with open('avaliacoes.json', 'w', encoding='utf-8') as f:
            json.dump(avaliacoes, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para avaliacoes.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_avaliacao():
    while True:
        print('\n**Menu - Avaliação**')
        print('1. Inserir uma nova avaliação')
        print('2. Listar todas as avaliações')
        print('3. Atualizar os dados de uma avaliação')
        print('4. Excluir uma avaliação')
        print('5. Exportar Avaliações para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo uma nova avaliação ***')
            id = validar_id()
            while True:
                nota = validar_inteiro('Digite a nota da consulta (de 0 a 5): ')
                if 0 <= nota <= 5:
                    break
                else:
                    print('Nota inválida. Por favor, insira um valor entre 0 e 5.')
            comentario = validar_string('Digite um comentário sobre a consulta: ')
            data_avaliacao = validar_data('Digite a data da avaliação (DD/MM/AAAA HH:MM): ')
            if create_avaliacao(id, nota, comentario, data_avaliacao):
                print(f'\n Avaliação (ID: {id}) com nota {nota} foi adicionada com sucesso!')
            else:
                print('\n Falha ao adicionar a avaliação.')

        elif opcao == 2:
            print('\n*** Listando todas as avaliações ***')
            avaliacoes = read_avaliacao()
            if avaliacoes is not None:
                if avaliacoes:
                    print("\n--- Lista de Avaliações ---")
                    for a in avaliacoes:
                        print(f"ID: {a['id']}, Nota: {a['nota']}, Comentário: {a['comentario']}, Data: {a['data_avaliacao']}")
                        print('----------------------------------')
                else:
                    print("↪️ Nenhuma avaliação encontrada.")
            else:
                print(" Erro ao listar as avaliações.")

        elif opcao == 3:
            print('\n*** Atualizando uma avaliação ***')
            id = validar_string('Digite o Id da avaliação que deseja atualizar: ')
            while True:
                nova_nota = validar_inteiro('Digite a nova nota da avaliação (de 0 a 5): ')
                if 0 <= nova_nota <= 5:
                    break
                else:
                    print('Nota inválida. Por favor, insira um valor entre 0 e 5.')
            novo_comentario = validar_string('Digite o novo comentário da avaliação: ')
            nova_data_avaliacao = validar_data('Digite a nova data da avaliação (DD/MM/AAAA HH:MM): ')
            if update_avaliacao(id, nova_nota, novo_comentario, nova_data_avaliacao):
                print(f'\n A avaliação de ID {id} foi atualizada com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhuma avaliação com ID {id} foi encontrada ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo uma avaliação ***')
            id = validar_string('Digite o Id da avaliação que deseja excluir: ')
            if delete_avaliacao(id):
                print(f'\n A avaliação de ID: {id} foi excluida com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhuma avaliação com ID {id} foi encontrada ou ocorreu um erro.')

        elif opcao == 5:
            exportar_avaliacoes_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_avaliacao()