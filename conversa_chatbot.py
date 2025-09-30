import oracledb
from utilitarios import getConnection,validar_string,validar_inteiro

'''
1.7. CONVERSA_CHATBOT deve ser representado com as chaves: id_conversa, pergunta e aprovacao.
'''
#Operações CRUD
def create_conversa_chatbot(id_conversa, pergunta, aprovacao):
    print('*** Inserindo uma nova conversa na tabela conversas_chatbot ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO conversas_chatbot (id_conversa, pergunta, aprovacao)
            VALUES (:id_conversa, :pergunta, :aprovacao)
        """
        cursor.execute(sql, {
            'id_conversa' : id_conversa,
            'pergunta' : pergunta,
            'aprovacao' : aprovacao
        })
        conn.commit()
        print(f' A conversa com chatbot de ID: {id_conversa} foi adicionado com sucesso!')
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
            SELECT id_conversa, pergunta , aprovacao
            FROM conversas_chatbot ORDER BY id_conversa
        """
        cursor.execute(sql)
        print("\n --- Lista de conversas com chatbot ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, pergunta: {row[1]}, aprovacao: {row[2]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler conversas com chatbots: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um conversa_chatbot
def update_conversa_chatbot(id_conversa, nova_pergunta, nova_aprovaçao):
    print(f'Atualizando os dados da conversa chatbot pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE conversas_chatbot
        set pergunta = :nova_pergunta, aprovacao = :nova_aprovaçao, = :novo WHERE id_conversa = :id_conversa
        
        """
        cursor.execute(sql, {'nova_pergunta' : nova_pergunta, 'nova_aprovaçao' : nova_aprovaçao,'id_conversa': id_conversa})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A nova pergunta {nova_pergunta}, nova aprovação {nova_aprovaçao} da conversa: {id_conversa} foram atualizados!')
        else:
            print(f'Nenhuma conversa com chatbot de ID {id_conversa} foi encontrada')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove uma conversa_chatbot pelo Id

def delete_conversa_chatbot(id_conversa):
    print(f' Excluindo a conversa com chatbot de ID: {id_conversa}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM conversas_chatbot WHERE 
        id_conversa=  :id_conversa
        """
        cursor.execute(sql, {'id_conversa' : id_conversa})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A conversa com chatbot de ID: {id_conversa} foi excluido com sucesso!')
        else:
            print(f'Nenhuma conversa com chatbot de ID {id_conversa} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir a conversa com chatbot: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_conversa_chatbot():

    while True:

        print('**Menu - conversas com chatbot**')
        print('1. Inserir uma nova conversa com chatbot')
        print('2. Listar todas as conversas com chatbots')
        print('3. Atualizar os dados de uma conversa com chatbot')
        print('4. Excluir uma conversa com chatbot')
        print('5. Encerrar o Programa')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id_conversa =validar_inteiro('Digite o ID da conversa: ')
            pergunta = validar_string('Digite a pergunta: ')
            aprovacao = (input('Digite a aprovação (S/N): '))
            create_conversa_chatbot(id_conversa,pergunta,aprovacao)
    
        elif opcao==2:
            read_conversa_chatbot()

        elif opcao==3:
            id_conversa = validar_inteiro('Digite o Id da conversa com chatbot: ')
            nova_pergunta = validar_string('Digite a nova pergunta da conversa com chatbot: ')
            nova_aprovaçao = (input('Digite o nova aprovação da conversa com chatbot (S/N): '))
            update_conversa_chatbot(id_conversa,nova_pergunta,nova_aprovaçao)

        elif opcao==4:
            id_conversa = validar_inteiro('Digite o Id da conversa com chatbot: ')
            delete_conversa_chatbot(id_conversa)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 0 e 5.")

main_conversa_chatbot
