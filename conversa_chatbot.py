import oracledb
import json
from utilitarios import getConnection, validar_string, validar_inteiro, validar_id

def create_conversa_chatbot(id, id_paciente, pergunta, aprovacao):
    """Insere um novo registro de conversa e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_chatbot (id, id_paciente, pergunta, aprovacao)
                    VALUES (:id, :id_paciente, :pergunta, :aprovacao)
                """
                cursor.execute(sql, {
                    'id': id, 'id_paciente': id_paciente, 'pergunta': pergunta, 'aprovacao': aprovacao
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'Erro ao inserir a conversa do chatbot: {e}')
        return False

def read_conversa_chatbot():
    """Lê e retorna uma lista de todas as conversas do chatbot."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, id_paciente, pergunta, aprovacao FROM cc_chatbot ORDER BY id"
                cursor.execute(sql)
                conversas = []
                for row in cursor.fetchall():
                    conversas.append({
                        'id': row[0], 'id_paciente': row[1], 'pergunta': row[2], 'aprovacao': row[3]
                    })
                return conversas
    except oracledb.Error as e:
        print(f'Erro ao ler conversas com o chatbot: {e}')
        return None

def update_conversa_chatbot(id, novo_id_paciente, nova_pergunta, nova_aprovacao):
    """Atualiza uma conversa do chatbot e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_chatbot
                    SET id_paciente = :novo_id_paciente, pergunta = :nova_pergunta, aprovacao = :nova_aprovacao
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'novo_id_paciente': novo_id_paciente, 'nova_pergunta': nova_pergunta,
                    'nova_aprovacao': nova_aprovacao, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'Erro ao atualizar a conversa do chatbot: {e}')
        return False

def delete_conversa_chatbot(id):
    """Exclui uma conversa do chatbot e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_chatbot WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'Erro ao excluir a conversa do chatbot: {e}')
        return False

def exportar_conversas_chatbot_json():
    """Exporta as conversas do chatbot para JSON e retorna True em caso de sucesso."""
    print('Exportando dados das conversas do chatbot para JSON...')
    conversas = read_conversa_chatbot()
    if conversas is None:
        print('Nao foi possivel obter os dados para exportar.')
        return False
    if not conversas:
        print("Nenhuma conversa encontrada para exportar.")
        return True

    try:
        with open('conversas_chatbot.json', 'w', encoding='utf-8') as f:
            json.dump(conversas, f, ensure_ascii=False, indent=4)
        print('Dados exportados com sucesso para conversas_chatbot.json.')
        return True
    except IOError as e:
        print(f'Erro ao escrever o arquivo JSON: {e}')
        return False

def validar_aprovacao():
    while True:
        aprovacao = input("Digite a aprovação (s/n): ").lower()
        if aprovacao in ('s', 'n'):
            return aprovacao
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

def main_conversa_chatbot():
    while True:
        print('\n**Menu - Conversas com Chatbot**')
        print('1. Inserir uma nova conversa com chatbot')
        print('2. Listar todas as conversas com chatbots')
        print('3. Atualizar os dados de uma conversa com chatbot')
        print('4. Excluir uma conversa com chatbot')
        print('5. Exportar Conversas para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo uma nova conversa ***')
            id = validar_id()
            id_paciente = validar_string("Digite o ID do paciente: ")
            pergunta = validar_string('Digite a pergunta: ')
            aprovacao = validar_aprovacao()
            if create_conversa_chatbot(id, id_paciente, pergunta, aprovacao):
                print(f'A conversa (ID: {id}) foi adicionada com sucesso!')
            else:
                print('Falha ao adicionar a conversa.')

        elif opcao == 2:
            print('\n*** Listando todas as conversas ***')
            conversas = read_conversa_chatbot()
            if conversas is not None:
                if conversas:
                    print("\n--- Lista de Conversas com Chatbot ---")
                    for c in conversas:
                        print(f"ID: {c['id']}, ID Paciente: {c['id_paciente']}, Pergunta: {c['pergunta']}, Aprovação: {c['aprovacao']}")
                        print('----------------------------------')
                else:
                    print("Nenhuma conversa encontrada.")
            else:
                print("Erro ao listar as conversas.")

        elif opcao == 3:
            print('\n*** Atualizando uma conversa ***')
            id = validar_string('Digite o Id da conversa com chatbot: ')
            novo_id_paciente = validar_string("Digite o novo ID do paciente: ")
            nova_pergunta = validar_string('Digite a nova pergunta: ')
            nova_aprovacao = validar_aprovacao()
            if update_conversa_chatbot(id, novo_id_paciente, nova_pergunta, nova_aprovacao):
                print(f'Os dados da conversa {id} foram atualizados com sucesso!')
            else:
                print(f'Falha ao atualizar. Nenhuma conversa com ID {id} foi encontrada ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo uma conversa ***')
            id = validar_string('Digite o Id da conversa com chatbot que deseja excluir: ')
            if delete_conversa_chatbot(id):
                print(f'A conversa com chatbot de ID: {id} foi excluida com sucesso!')
            else:
                print(f'Falha ao excluir. Nenhuma conversa com ID {id} foi encontrada ou ocorreu um erro.')
        
        elif opcao == 5:
            exportar_conversas_chatbot_json()

        elif opcao == 6:
            print('Retornando ao menu principal...')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_conversa_chatbot()