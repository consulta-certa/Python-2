import oracledb
import json
from utilitarios import getConnection,validar_string,validar_inteiro,validar_data, validar_id

#Operações CRUD
def create_lembrete(id, data_envio, enviado, id_consulta):
    print('*** Inserindo um novo lembrete na tabela cc_lembretes ***')
    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO cc_lembretes (id, data_envio, enviado, id_consulta)
            VALUES (:id, :data_envio, :enviado, :id_consulta)
        """
        cursor.execute(sql, {
            'id' : id,
            'data_envio' : data_envio,
            'enviado': enviado,
            'id_consulta' : id_consulta
        })
        conn.commit()
        print(f' O Lembrete {id} da consulta: {id_consulta} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserior lembrete: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os Lembretes
def read_lembrete():
    print('*** Lê e exibe todos os lembretes da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, data_envio, enviado, id_consulta
            FROM cc_lembretes ORDER BY data_envio DESC
        """
        cursor.execute(sql)
        print("\n --- Lista de lembretes ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Data Envio: {row[1].strftime("%d/%m/%Y %H:%M")}, Enviado: {row[2]}, ID Consulta: {row[3]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler lembretes: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um lembrete
def update_lembrete(id, nova_data_envio, novo_enviado, novo_id_consulta):
    print(f'Atualizando os dados do lembrete pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE cc_lembretes
        SET data_envio = :nova_data_envio, enviado = :novo_enviado, id_consulta = :novo_id_consulta WHERE id = :id
        """
        cursor.execute(sql, {'nova_data_envio' : nova_data_envio, 'novo_enviado' :novo_enviado, 'novo_id_consulta' : novo_id_consulta, 'id': id})
        conn.commit()
        if cursor.rowcount >0:
            print(f'Os dados do lembrete de ID {id} foram atualizados!')
        else:
            print(f' Nenhum lembrete com ID {id} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um lembrete pelo Id
def delete_lembrete(id):
    print(f' Excluindo o lembrete com id: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """DELETE FROM cc_lembretes WHERE id = :id"""
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O lembrete {id} foi excluido com sucesso!')
        else:
            print(f'Nenhum lembrete com ID {id} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir lembrete: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

def exportar_lembretes_json():
    '''
    Exporta todos os lembretes cadastrados no banco Oracle
    para um arquivo local 'lembretes.json'.
    '''
    print('\n📤 Exportando dados dos lembretes para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, TO_CHAR(data_envio, 'DD/MM/YYYY HH24:MI:SS') as data_formatada, enviado, id_consulta
            FROM cc_lembretes ORDER BY data_envio DESC
        """)
        rows = cursor.fetchall()

        lembretes = [
            {'id': row[0], 'data_envio': row[1],'enviado': row[2], 'id_consulta': row[3]}
            for row in rows
        ]

        with open('lembretes.json', 'w', encoding='utf-8') as f:
            json.dump(lembretes, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para lembretes.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()

def validar_enviado():
    while True:
        enviado = input("O lembrete foi enviado? (s/n): ").lower()
        if enviado in ('s', 'n'):
            return enviado
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

#Programa Principal
def main_lembrete():

    while True:

        print('\n**Menu - Lembretes de Consulta**')
        print('1. Inserir um novo lembrete')
        print('2. Listar todos os lembretes')
        print('3. Atualizar os dados de um lembrete')
        print('4. Excluir um lembrete')
        print('5. Exportar Lembretes para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            id = validar_id()
            data_envio = validar_data('Digite a data e hora de envio (DD/MM/AAAA HH:MM): ')
            enviado = validar_enviado()
            id_consulta = validar_string('Digite o ID da consulta relacionada: ')
            create_lembrete(id, data_envio, enviado, id_consulta)
    
        elif opcao==2:
            read_lembrete()
            
        elif opcao == 3:
            id = validar_string('Digite o Id do lembrete que deseja atualizar: ')
            nova_data_envio = validar_data('Digite a nova data e hora de envio (DD/MM/AAAA HH:MM): ')
            novo_enviado = validar_enviado()
            novo_id_consulta = validar_string('Digite o novo ID da consulta relacionada: ')
            update_lembrete(id, nova_data_envio, novo_enviado, novo_id_consulta)

        elif opcao==4:
            id = validar_string('Digite o Id do lembrete que deseja excluir: ')
            delete_lembrete(id)

        elif opcao == 5:
            exportar_lembretes_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_lembrete()