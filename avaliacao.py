import oracledb
import json
from utilitarios import getConnection,validar_string,validar_inteiro,validar_data, validar_id

#Operações CRUD
def create_avaliacao(id, nota, comentario, data_avaliacao):
    print('*** Inserindo uma nova avaliação na tabela cc_avaliacoes ***')
    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO cc_avaliacoes (id, nota, comentario, data_avaliacao)
            VALUES (:id, :nota, :comentario, :data_avaliacao)
        """
        cursor.execute(sql, {
            'id' : id,
            'nota' : nota,
            'comentario' : comentario,
            'data_avaliacao' : data_avaliacao
        })
        conn.commit()
        print(f' A avaliação de ID: {id}, nota: {nota}, comentario: {comentario}, data_avaliacao: {data_avaliacao} foi adicionada com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir avaliação: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os avaliacoes
def read_avaliacao():
    print('*** Lê e exibe todos as avaliações da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, nota, comentario, data_avaliacao
            FROM cc_avaliacoes ORDER BY data_avaliacao DESC
        """
        cursor.execute(sql)
        print("\n --- Lista de avaliações ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Nota: {row[1]}, Comentário: {row[2]}, Data: {row[3].strftime("%d/%m/%Y")}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler as avaliações: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um avaliacao
def update_avaliacao(id, nova_nota, novo_comentario, nova_data_avaliacao):
    print(f'Atualizando os dados da avaliação pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE cc_avaliacoes
        SET nota = :nova_nota, comentario = :novo_comentario, data_avaliacao = :nova_data_avaliacao WHERE id = :id
        """
        cursor.execute(sql, {'nova_nota' : nova_nota, 'novo_comentario' : novo_comentario, 'nova_data_avaliacao' :nova_data_avaliacao, 'id': id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'A avaliação de ID {id} foi atualizada com sucesso!')
        else:
            print(f'Nenhuma avaliação com ID {id} foi encontrada')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um avaliacao pelo Id
def delete_avaliacao(id):
    print(f' Excluindo a avaliação com id: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """DELETE FROM cc_avaliacoes WHERE id = :id"""
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'A avaliação de ID: {id} foi excluida com sucesso!')
        else:
            print(f'Nenhuma avaliação com ID {id} foi encontrada')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir avaliação: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

def exportar_avaliacoes_json():
    '''
    Exporta todas as avaliações cadastradas no banco Oracle
    para um arquivo local 'avaliacoes.json'.
    '''
    print('\n📤 Exportando dados das avaliações para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nota, comentario, TO_CHAR(data_avaliacao, 'DD/MM/YYYY') as data_formatada
            FROM cc_avaliacoes ORDER BY data_avaliacao DESC
        """)
        rows = cursor.fetchall()

        avaliacoes = [
            {'id': row[0], 'nota': row[1],'comentario': row[2],'data_avaliacao': row[3]}
            for row in rows
        ]

        with open('avaliacoes.json', 'w', encoding='utf-8') as f:
            json.dump(avaliacoes, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para avaliacoes.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()

#Programa Principal
def main_avaliacao():

    while True:

        print('\n**Menu - Avaliação**')
        print('1. Inserir uma nova avaliação')
        print('2. Listar todas as avaliações')
        print('3. Atualizar os dados de uma avaliação')
        print('4. Excluir uma avaliação')
        print('5. Exportar Avaliações para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao ==1:
            id = validar_id()
            while True:
                nota = validar_inteiro('Digite a nota da consulta (de 0 a 5): ')
                if 0 <= nota <= 5:
                    break
                else:
                    print('Nota inválida. Por favor, insira um valor entre 0 e 5.')
            comentario = validar_string('Digite um comentário sobre a consulta: ', maximo=255)
            data_avaliacao = validar_data('Digite a data da avaliação (DD/MM/AAAA HH:MM): ')
            create_avaliacao(id, nota, comentario, data_avaliacao)
    
        elif opcao==2:
            read_avaliacao()

        elif opcao==3:
            id = validar_string('Digite o Id da avaliação que deseja atualizar: ')
            while True:
                nova_nota = validar_inteiro('Digite a nova nota da avaliação (de 0 a 5): ')
                if 0 <= nova_nota <= 5:
                    break
                else:
                    print('Nota inválida. Por favor, insira um valor entre 0 e 5.')
            novo_comentario = validar_string('Digite o novo comentário da avaliação: ', maximo=255)
            nova_data_avaliacao = validar_data('Digite a nova data da avaliação (DD/MM/AAAA HH:MM): ')
            update_avaliacao(id, nova_nota, novo_comentario, nova_data_avaliacao)

        elif opcao==4:
            id = validar_string('Digite o Id da avaliação que deseja excluir: ')
            delete_avaliacao(id)

        elif opcao == 5:
            exportar_avaliacoes_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_avaliacao()