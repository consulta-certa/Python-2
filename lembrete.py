import oracledb
from utilitarios import getConnection,validar_string,validar_inteiro,validar_data

'''
1.4. lembretes devem ser representados com as chaves: id_lembrete,
data_envio e id_consulta // Tem que ter mensagem e id_paciente para verificação?'''

#Operações CRUD
def create_lembrete(id_lembrete, data_envio, id_consulta):
    print('*** Inserindo um novo lembrete na tabela lembretes ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO lembretes (id_lembrete, data_envio, id_consulta)
            VALUES (:id_lembrete, :data_envio, :id_consulta)
        """
        cursor.execute(sql, {
            'id_lembrete' : id_lembrete,
            'data_envio' : data_envio,
            'id_consulta' : id_consulta
        })
        conn.commit()
        print(f' O Lembrete {id_lembrete} da consulta: {id_consulta} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserior lembrete: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os Lembretes ativos
def read_lembrete():
    print('*** Lê e exibe todos os lembretes da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id_lembrete, data_envio, id_consulta
            FROM lembretes ORDER BY id_lembrete
        """
        cursor.execute(sql)
        print("\n --- Lista de lembretes ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID do Lembrete: {row[0]}, data e hora registradas: {row[1]}, id da consulta: {row[2]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler lembretes: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um lembrete
def update_lembrete(id_lembrete, nova_data_envio, novo_id_consulta):
    print(f'Atualizando os dados do lembrete pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE lembretes
        set data_envio = :nova_data_envio, id_consulta = :novo_id_consulta WHERE id_lembrete = :id_lembrete
        
        """
        cursor.execute(sql, {'nova_data_envio' : nova_data_envio, 'novo_id_consulta' :novo_id_consulta, 'id_lembrete': id_lembrete})
        conn.commit()
        if cursor.rowcount >0:
            print(f' A nova data de envio: {nova_data_envio} e id da consulta: {novo_id_consulta} do lembrete: {id_lembrete} foram atualizados!')
        else:
            print(f' Nenhum lembrete com ID {id_lembrete} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um lembrete pelo Id

def delete_lembrete(id_lembrete):
    print(f' Excluindo o lembrete com id: {id_lembrete}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM lembretes WHERE 
        id_lembrete=  :id_lembrete
        """
        cursor.execute(sql, {'id_lembrete' : id_lembrete})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O lembrete {id_lembrete} foi excluido com sucesso!')
        else:
            print(f'Nenhum lembrete com ID {id_lembrete} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir lembrete: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_lembrete():

    while True:

        print('**Menu - lembrete**')
        print('1. Inserir um novo lembrete')
        print('2. Listar todos os lembretes')
        print('3. Atualizar os dados de um lembrete')
        print('4. Excluir um lembrete')
        print('5. Encerrar o Programa')

        opcao=validar_inteiro('Digite uma opção entre 1 a 5: ')
        if opcao == 1:
            id_lembrete = validar_inteiro('Digite o ID do lembrete: ')
            data_envio = validar_data('Digite a data e hora de envio (DD/MM/AAAA HH:MM): ')
            id_consulta = validar_inteiro('Digite o ID da consulta: ')

            create_lembrete(id_lembrete, data_envio, id_consulta)
    
        elif opcao==2:
            read_lembrete()
            
        elif opcao == 3:
            id_lembrete = validar_inteiro('Digite o Id do lembrete: ')
            nova_data_envio = validar_data('Digite a nova data e hora de envio (DD/MM/AAAA HH:MM): ')
            novo_id_consulta = validar_inteiro('Digite o novo id da consulta: ')

            update_lembrete(id_lembrete, nova_data_envio, novo_id_consulta)

        elif opcao==4:
            id_lembrete = validar_inteiro('Digite o Id do lembrete: ')
            delete_lembrete(id_lembrete)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 1 e 5.")

main_lembrete
