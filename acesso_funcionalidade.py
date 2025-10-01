import oracledb
from utilitarios import getConnection, validar_inteiro,validar_string

'''
1.9. ACESSO_FUNCIONALIDADE deve ser representado com as chaves: id_acesso, funcionalidade,
quantidade_acessos e tempo_permanencia_seg

'''
#Operações CRUD
def create_acesso(id_acesso, funcionalidade, quantidade_acessos, tempo_permanencia_seg):
    print('*** Inserindo um novo acesso na tabela acessos_funcionalidade ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO acessos_funcionalidade (id_acesso, funcionalidade, quantidade_acessos, tempo_permanencia_seg)
            VALUES (:id_acesso, :funcionalidade, :quantidade_acessos, :tempo_permanencia_seg)
        """
        cursor.execute(sql, {
            'id_acesso' : id_acesso,
            'funcionalidade' : funcionalidade,
            'quantidade_acessos' : quantidade_acessos,
            'tempo_permanencia_seg' : tempo_permanencia_seg,
        })
        conn.commit()
        print(f' O acesso de ID: {id_acesso}, funcionalidade: {funcionalidade}, quantidade de acessos: {quantidade_acessos}, e tempo de permanencia em segundos: {tempo_permanencia_seg} foi adicionado com sucesso!')
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
            SELECT id_acesso, funcionalidade , quantidade_acessos, tempo_permanencia_seg 
            FROM acessos_funcionalidade ORDER BY id_acesso
        """
        cursor.execute(sql)
        print("\n --- Lista de acessos ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, funcionalidade: {row[1]}, quantidade de acessos: {row[2]}, tempo de permanencia em segundos: {row[3]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler acessos: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um acesso
def update_acesso(id_acesso, nova_funcionalidade, nova_quantidade_acessos, novo_tempo_permanencia_seg,):
    print(f'Atualizando os dados do acesso pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE acessos_funcionalidade
        set funcionalidade = :nova_funcionalidade, quantidade_acessos = :nova_quantidade_acessos, tempo_permanencia_seg = :novo_tempo_permanencia_seg WHERE id_acesso = :id_acesso
        
        """
        cursor.execute(sql, {'nova_funcionalidade' : nova_funcionalidade, 'nova_quantidade_acessos' : nova_quantidade_acessos, 'novo_tempo_permanencia_seg' :novo_tempo_permanencia_seg,'id_acesso': id_acesso})
        conn.commit()
        if cursor.rowcount >0:
            print(f'A nova funcionalidade {nova_funcionalidade}, quantidade de acessos: {nova_quantidade_acessos} e tempo de permanencia em seg: {novo_tempo_permanencia_seg} do acesso de ID: {id_acesso} foram atualizados!')
        else:
            print(f'Nenhum acesso com ID {id_acesso} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um acesso pelo Id

def delete_acesso(id_acesso):
    print(f' Excluindo o acesso com id: {id_acesso}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM acessos_funcionalidade WHERE
        id_acesso=  :id_acesso
        """
        cursor.execute(sql, {'id_acesso' : id_acesso})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O acesso de ID: {id_acesso} foi excluido com sucesso!')
        else:
            print(f'Nenhum acesso com ID {id_acesso} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir acesso: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_acesso():

    while True:

        print('**Menu - acesso**')
        print('1. Inserir um novo acesso')
        print('2. Listar todos os acessos')
        print('3. Atualizar os dados de um acesso')
        print('4. Excluir um acesso')
        print('5. Encerrar o Programa')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id_acesso = validar_inteiro('Digite o ID do acesso: ')
            funcionalidade = validar_string('Digite a Funcionalidade do acesso: ')
            quantidade_acessos = validar_string('Digite a quantidade de acessos: ')
            tempo_permanencia_seg= validar_string('Digite o tempo de permanencia em segundos: ')
            create_acesso(id_acesso,funcionalidade,quantidade_acessos,tempo_permanencia_seg)
    
        elif opcao==2:
            read_acesso()

        elif opcao==3:
            id_acesso = validar_inteiro('Digite o Id do acesso: ')
            nova_funcionalidade = validar_string('Digite a nova funcionalidade do acesso: ')
            nova_quantidade_acessos = validar_string('Digite a nova quantidade de acessos do acesso: ')
            novo_tempo_permanencia_seg = validar_string('Digite o novo tempo de permanencia em segundos: ')
            update_acesso(id_acesso,nova_funcionalidade,nova_quantidade_acessos,novo_tempo_permanencia_seg)

        elif opcao==4:
            id_acesso = validar_inteiro('Digite o Id do acesso: ')
            delete_acesso(id_acesso)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 1 e 5.")

main_acesso