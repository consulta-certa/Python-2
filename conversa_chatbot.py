import oracledb
import json
from utilitarios import getConnection,validar_string,validar_inteiro, validar_id

#Operações CRUD
def create_conversa_chatbot(id, id_paciente, pergunta, aprovacao):
    print('*** Inserindo uma nova conversa na tabela cc_chatbot ***')
    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO cc_chatbot (id, id_paciente, pergunta, aprovacao)
            VALUES (:id, :id_paciente, :pergunta, :aprovacao)
        """
        cursor.execute(sql, {
            'id' : id,
            'id_paciente' : id_paciente,
            'pergunta' : pergunta,
            'aprovacao' : aprovacao
        })
        conn.commit()
        print(f' A conversa com chatbot de ID: {id} foi adicionada com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir a conversa chatbot: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todas as conversa_chatbot
def read_conversa_chatbot():
    print('*** Lê e exibe todas as conversas com chatbot da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, id_paciente, pergunta, aprovacao
            FROM cc_chatbot ORDER BY id
        """
        cursor.execute(sql)
        print("\n --- Lista de conversas com chatbot ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, ID Paciente: {row[1]}, Pergunta: {row[2]}, Aprovação: {row[3]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler conversas com chatbots: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um conversa_chatbot
def update_conversa_chatbot(id, novo_id_paciente, nova_pergunta, nova_aprovacao):
    print(f'Atualizando os dados da conversa chatbot pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE cc_chatbot
        SET id_paciente = :novo_id_paciente, pergunta = :nova_pergunta, aprovacao = :nova_aprovacao WHERE id = :id
        """
        cursor.execute(sql, {'novo_id_paciente': novo_id_paciente, 'nova_pergunta' : nova_pergunta, 'nova_aprovacao' : nova_aprovacao,'id': id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'Os dados da conversa {id} foram atualizados!')
        else:
            print(f'Nenhuma conversa com chatbot de ID {id} foi encontrada')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove uma conversa_chatbot pelo Id
def delete_conversa_chatbot(id):
    print(f' Excluindo a conversa com chatbot de ID: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """DELETE FROM cc_chatbot WHERE id = :id"""
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'A conversa com chatbot de ID: {id} foi excluida com sucesso!')
        else:
            print(f'Nenhuma conversa com chatbot de ID {id} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir a conversa com chatbot: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

def exportar_conversas_chatbot_json():
    '''
    Exporta todas as conversas do chatbot cadastradas no banco Oracle
    para um arquivo local 'conversas_chatbot.json'.
    '''
    print('\n📤 Exportando dados das conversas do chatbot para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, id_paciente, pergunta, aprovacao
            FROM cc_chatbot ORDER BY id
        """)
        rows = cursor.fetchall() 

        conversas = [
            {'id': row[0], 'id_paciente': row[1], 'pergunta': row[2],'aprovacao': row[3]}
            for row in rows
        ]

        with open('conversas_chatbot.json', 'w', encoding='utf-8') as f:
            json.dump(conversas, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para conversas_chatbot.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()

def validar_aprovacao():
    while True:
        aprovacao = input("Digite a aprovação (s/n): ").lower()
        if aprovacao in ('s', 'n'):
            return aprovacao
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

#Programa Principal
def main_conversa_chatbot():

    while True:

        print('\n**Menu - Conversas com Chatbot**')
        print('1. Inserir uma nova conversa com chatbot')
        print('2. Listar todas as conversas com chatbots')
        print('3. Atualizar os dados de uma conversa com chatbot')
        print('4. Excluir uma conversa com chatbot')
        print('5. Exportar Conversas para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao ==1:
            id = validar_id()
            id_paciente = validar_string("Digite o ID do paciente: ")
            pergunta = validar_string('Digite a pergunta: ')
            aprovacao = validar_aprovacao()
            create_conversa_chatbot(id, id_paciente, pergunta, aprovacao)
    
        elif opcao==2:
            read_conversa_chatbot()

        elif opcao==3:
            id = validar_string('Digite o Id da conversa com chatbot: ')
            novo_id_paciente = validar_string("Digite o novo ID do paciente: ")
            nova_pergunta = validar_string('Digite a nova pergunta da conversa com chatbot: ')
            nova_aprovacao = validar_aprovacao()
            update_conversa_chatbot(id, novo_id_paciente, nova_pergunta, nova_aprovacao)

        elif opcao==4:
            id = validar_string('Digite o Id da conversa com chatbot que deseja excluir: ')
            delete_conversa_chatbot(id)

        elif opcao == 5:
            exportar_conversas_chatbot_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_conversa_chatbot()