import oracledb
from utilitarios import getConnection,validar_string,validar_inteiro,validar_data

'''
1.6. AVALIACAO deve ser representado por um dicionário com as chaves: id_avaliacao, nota, comentario,
data_avaliacao e id_lembrete.
'''
#Operações CRUD
def create_avaliacao(id_avaliacao, nota, comentario, data_avaliacao, id_lembrete,):
    print('*** Inserindo uma nova avaliação na tabela avaliacoes ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO avaliacoes (id_avaliacao, nota, comentario, data_avalicao, id_lembrete)
            VALUES (:id_avaliacao, :nota, :comentario, :data_avalicao, :id_lembrete)
        """
        cursor.execute(sql, {
            'id_avaliacao' : id_avaliacao,
            'nota' : nota,
            'comentario' : comentario,
            'data_avalicao' : data_avaliacao,
            'id_lembrete' : id_lembrete
        })
        conn.commit()
        print(f' A avaliação de ID: {id_avaliacao}, nota: {nota}, comentario: {comentario}, data_avalicao: {data_avaliacao} e id_lembrete: {id_lembrete} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir avaliação: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os avaliacaos
def read_avaliacao():
    print('*** Lê e exibe todos as avaliações da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id_avaliacao, nota, comentario, data_avalicao, id_lembrete
            FROM avaliacoes ORDER BY id_avaliacao
        """
        cursor.execute(sql)
        print("\n --- Lista de avaliações ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, nota: {row[1]}, comentario: {row[2]}, data_avalicao: {row[3]}, id_lembrete: {row[4]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler as avaliações: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um avaliacao
def update_avaliacao(id_avaliacao, nova_nota, novo_comentario, nova_data_avaliacao, novo_id_lembrete):
    print(f'Atualizando os dados da avaliação pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE avaliacoes
        set nota = :nova_nota, comentario = :novo_comentario, data_avalicao = :nova_data_avaliacao, id_lembrete = :novo_id_lembrete WHERE id_avaliacao = :id_avaliacao
        
        """
        cursor.execute(sql, {'nova_nota' : nova_nota, 'novo_comentario' : novo_comentario, 'nova_data_avaliacao' :nova_data_avaliacao, 'novo_id_lembrete' : novo_id_lembrete, 'id_avaliacao': id_avaliacao})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A nova nota {nova_nota}, comentario: {novo_comentario}, data_avaliacao: {nova_data_avaliacao}, id_lembrete: {novo_id_lembrete}, da avaliacao de ID:{id_avaliacao} foram atualizados!')
        else:
            print(f'Nenhum avaliação com ID {id_avaliacao} foi encontrada')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um avaliacao pelo Id

def delete_avaliacao(id_avaliacao):
    print(f' Excluindo a avaliação com id: {id_avaliacao}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM avaliacoes WHERE 
        id_avaliacao=  :id_avaliacao
        """
        cursor.execute(sql, {'id_avaliacao' : id_avaliacao})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A avaliação de ID: {id_avaliacao} foi excluida com sucesso!')
        else:
            print(f'Nenhuma avaliação com ID {id_avaliacao} foi encontrada')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir avaliação: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_avaliacao():

    while True:

        print('**Menu - avaliação**')
        print('1. Inserir uma nova avaliação')
        print('2. Listar todas as avaliações')
        print('3. Atualizar os dados de uma avaliação')
        print('4. Excluir uma avaliação')
        print('5. Encerrar o Programa')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id_avaliacao = validar_inteiro('Digite o ID avaliação: ')
            nota = validar_inteiro('Digite a nota da consulta: ')
            comentario = validar_string('Digite o comentario sobre a consulta: ')
            data_avaliacao= validar_data('Digite a data da avaliacao: ')
            id_lembrete=validar_inteiro('Digite o ID do lembrete: ')
            create_avaliacao(id_avaliacao,nota,comentario,data_avaliacao,id_lembrete)
    
        elif opcao==2:
            read_avaliacao()

        elif opcao==3:
            id_avaliacao = validar_inteiro('Digite o Id da avaliação: ')
            nova_nota = validar_inteiro('Digite a nova nota da avaliação: ')
            novo_comentario = validar_string('Digite o novo comentario da avaliação: ')
            nova_data_avaliacao = validar_data('Digite a nova data da avaliação: ')
            novo_id_lembrete = validar_inteiro('Digite o novo id do lembrete: ')
            update_avaliacao(id_avaliacao,nova_nota,novo_comentario,nova_data_avaliacao,novo_id_lembrete)

        elif opcao==4:
            id_avaliacao = validar_inteiro('Digite o Id da avaliação: ')
            delete_avaliacao(id_avaliacao)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 0 e 5.")
            
main_avaliacao