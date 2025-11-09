import oracledb
import json
from utilitarios import getConnection, validar_inteiro,validar_string,validar_data

'''
1.9. ACESSO_FUNCIONALIDADE deve ser representado com as chaves: id, funcionalidade,
quantidade_acessos e tempo_permanencia_seg, data_acesso, id_paciente

verificar check_acessos_funcionalidades

'''
#Operações CRUD
def create_acesso(id, funcionalidade, quantidade_acessos, tempo_permanencia_seg, data_acesso, id_paciente):
    print('*** Inserindo um novo acesso na tabela CC_ACESSOS_FUNCIONALIDADE ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO CC_ACESSOS_FUNCIONALIDADE (id, funcionalidade, quantidade_acessos, tempo_permanencia_seg, data_acesso, id_paciente)
            VALUES (:id, :funcionalidade, :quantidade_acessos, :tempo_permanencia_seg, :data_acesso, :id_paciente)
        """
        cursor.execute(sql, {
            'id' : id,
            'funcionalidade' : funcionalidade,
            'quantidade_acessos' : quantidade_acessos,
            'tempo_permanencia_seg' : tempo_permanencia_seg,
            'data_acesso' : data_acesso,
            'id_paciente' : id_paciente
        })
        conn.commit()
        print(f' O acesso de ID: {id}, funcionalidade: {funcionalidade}, quantidade de acessos: {quantidade_acessos}, tempo de permanencia em segundos: {tempo_permanencia_seg,}, data de acesso: {data_acesso} do paciente de id: {id_paciente} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir acesso: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os acessos
def read_acesso():
    print('*** Lê e exibe todos os acessos da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, funcionalidade , quantidade_acessos, tempo_permanencia_seg, data_acesso, id_paciente 
            FROM CC_ACESSOS_FUNCIONALIDADE ORDER BY id
        """
        cursor.execute(sql)
        print("\n --- Lista de acessos ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, funcionalidade: {row[1]}, quantidade de acessos: {row[2]}, tempo de permanencia em segundos: {row[3]}, data de acesso: {row[4]} e id do paciente: {row[5]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler acessos: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um acesso
def update_acesso(id, nova_funcionalidade, nova_quantidade_acessos, novo_tempo_permanencia_seg, nova_data_acesso, novo_id_paciente):
    print(f'Atualizando os dados do acesso pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE CC_ACESSOS_FUNCIONALIDADE
        set funcionalidade = :nova_funcionalidade, quantidade_acessos = :nova_quantidade_acessos, tempo_permanencia_seg = :novo_tempo_permanencia_seg, data_acesso = :nova_data_acesso, id_paciente = :novo_id_paciente WHERE id = :id
        
        """
        cursor.execute(sql,{'nova_funcionalidade' : nova_funcionalidade, 'nova_quantidade_acessos' : nova_quantidade_acessos, 'novo_tempo_permanencia_seg' : novo_tempo_permanencia_seg, 'nova_data_acesso': nova_data_acesso, 'novo_id_paciente' : novo_id_paciente, 'id': id})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A nova funcionalidade {nova_funcionalidade}, quantidade de acessos: {nova_quantidade_acessos}, tempo de permanencia em seg: {novo_tempo_permanencia_seg}, nova data de acesso: {nova_data_acesso} e novo id do paciente: {novo_id_paciente} do acesso de ID: {id} foram atualizados!')
        else:
            print(f'Nenhum acesso com ID {id} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um acesso pelo Id

def delete_acesso(id):
    print(f' Excluindo o acesso com id: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM CC_ACESSOS_FUNCIONALIDADE WHERE
        id=  :id
        """
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O acesso de ID: {id} foi excluido com sucesso!')
        else:
            print(f'Nenhum acesso com ID {id} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir acesso: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()


def exportar_acessos_json():
    '''
    Exporta todos os acessos cadastrados no banco Oracle
    para um arquivo local 'acessos.json'.
    '''
    print('\n📤 Exportando dados dos acessos para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, funcionalidade , quantidade_acessos, tempo_permanencia_seg, data_acesso, id_paciente 
            FROM CC_ACESSOS_FUNCIONALIDADE ORDER BY id
        """)
        rows = cursor.fetchall() 

        acessos = [
            {'id': row[0], 'funcionalidade': row[1],'quantidade_acessos': row[2],'tempo_permanencia_seg': row[3], 'data_acesso': row[4], 'id_paciente' : row[5]}
            for row in rows
        ]

        with open('acessos.json', 'w', encoding='utf-8') as f:
            json.dump(acessos, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para acessos.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()
    

#Programa Principal

def main_acesso():

    while True:

        print('**Menu - acesso**')
        print('1. Inserir um novo acesso')
        print('2. Listar todos os acessos')
        print('3. Atualizar os dados de um acesso')
        print('4. Excluir um acesso')
        print('5. Exportar acessos para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id = validar_inteiro('Digite o ID do acesso: ')
            funcionalidade = validar_string('Digite a Funcionalidade do acesso: ')
            quantidade_acessos = validar_inteiro('Digite a quantidade de acessos: ')
            tempo_permanencia_seg= validar_inteiro('Digite o tempo de permanencia em segundos: ')
            data_acesso=validar_data('Digite a data de acesso: ')
            id_paciente=validar_inteiro('Digite o id do paciente: ')
            create_acesso(id,funcionalidade,quantidade_acessos,tempo_permanencia_seg, data_acesso, id_paciente)
    
        elif opcao==2:
            read_acesso()

        elif opcao==3:
            id = validar_inteiro('Digite o Id do acesso: ')
            nova_funcionalidade = validar_string('Digite a nova funcionalidade do acesso: ')
            nova_quantidade_acessos = validar_inteiro('Digite a nova quantidade de acessos do acesso: ')
            novo_tempo_permanencia_seg = validar_inteiro('Digite o novo tempo de permanencia em segundos: ')
            nova_data_acesso=validar_data('Digite a nova data de acesso: ')
            novo_id_paciente=validar_inteiro('Digite o novo id do paciente: ')
            update_acesso(id,nova_funcionalidade,nova_quantidade_acessos,novo_tempo_permanencia_seg,nova_data_acesso,novo_id_paciente)

        elif opcao==4:
            id = validar_inteiro('Digite o Id do acesso: ')
            delete_acesso(id)
            
        elif opcao == 5:
            exportar_acessos_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_acesso()
