import oracledb
import json
from utilitarios import getConnection,validar_nome,validar_inteiro,validar_email,validar_telefone

'''
1.1 Cada PACIENTE deve ser representado com as chaves: id_paciente, nome, email, senha, telefone e acompanhante.
'''
#Operações CRUD
def create_paciente(id_paciente, nome, email, senha, telefone, acompanhante):
    print('*** Inserindo um novo paciente na tabela pacientes ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO pacientes (id_paciente, nome, email, senha, telefone, acompanhante)
            VALUES (:id_paciente, :nome, :email, :senha, :telefone, :acompanhante)
        """
        cursor.execute(sql, {
            'id_paciente' : id_paciente,
            'nome' : nome,
            'email' : email,
            'senha' : senha,
            'telefone' : telefone,
            'acompanhante' : acompanhante
    
        })
        conn.commit()
        print(f'Paciente {id_paciente} de nome {nome} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserior Paciente: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os Pacientes
def read_paciente():
    print('*** Lê e exibe todos os Pacientes da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id_paciente, nome , email, senha, telefone, acompanhante
            FROM pacientes ORDER BY id_paciente
        """
        cursor.execute(sql)
        print("\n --- Lista de Pacientes ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Nome: {row[1]}, Email: {row[2]}, Senha: {row[3]}, Telefone: {row[4]}, Acompanhante: {row[5]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler Pacientes: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um Paciente
def update_paciente(id_paciente, novo_nome, novo_email, novo_telefone, nova_senha, novo_acompanhante):
    print(f'Atualizando os dados do Paciente pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE pacientes
        set nome = :novo_nome, email = :novo_email, senha = :nova_senha, telefone = :novo_telefone, acompanhante = :novo_acompanhante  WHERE id_paciente = :id_paciente
        
        """
        cursor.execute(sql, {'novo_nome' : novo_nome, 'novo_email' : novo_email, 'nova_senha' : nova_senha, 'novo_telefone' : novo_telefone, 'novo_acompanhante' : novo_acompanhante, 'id_paciente': id_paciente})
        conn.commit()
        if cursor.rowcount >0:
            print(f' O novo Nome: {novo_nome}, Email: {novo_email}, Telefone: {novo_telefone}, Senha: {nova_senha} e se tem Acompanhante: {novo_acompanhante} do Paciente: {id_paciente} foram atualizados!')
        else:
            print(f'Nenhum Paciente com ID {id_paciente} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um Paciente pelo Id

def delete_paciente(id_paciente):
    print(f' Excluindo o Paciente com id: {id_paciente}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM pacientes WHERE 
        id_paciente=  :id_paciente
        """
        cursor.execute(sql, {'id_paciente' : id_paciente})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O Paciente {id_paciente} foi excluido com sucesso!')
        else:
            print(f'Nenhum Paciente com ID {id_paciente} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir Paciente: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

def exportar_pacientes_json():
    '''
    Exporta todos os pacientes cadastrados no banco Oracle
    para um arquivo local 'pacientes.json'.
    '''
    print('\n📤 Exportando dados dos pacientes para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_paciente, nome , email, senha, telefone, acompanhante
            FROM pacientes ORDER BY id_paciente
        """)
        rows = cursor.fetchall()

        pacientes = [
            {'id_paciente': r[0], 'nome': r[1], 'email': r[2], 'telefone': r[3]}
            for r in rows
        ]

        with open('pacientes.json', 'w', encoding='utf-8') as f:
            json.dump(pacientes, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para pacientes.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()
    

#Programa Principal

def main_paciente():

    while True:

        print('**Menu - Paciente**')
        print('1. Inserir um novo Paciente')
        print('2. Listar todos os Pacientes')
        print('3. Atualizar os dados de um Paciente')
        print('4. Excluir um Paciente')
        print('5. Exportar Pacientes para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id_paciente = validar_inteiro('Digite o ID do paciente: ')
            nome = validar_nome('Digite o nome do paciente: ')
            email = validar_email('Digite o email do paciente: ')
            senha = (input('Digite a senha do paciente: '))
            telefone= validar_telefone('Digite o telefone do paciente: ')
            acompanhante = (input('O paciente terá acompanhante? (S/N): '))
            
            create_paciente(id_paciente,nome,email,senha,telefone,acompanhante)
    
        elif opcao==2:
            read_paciente()

        elif opcao==3:
            id_paciente = validar_inteiro('Digite o Id do Paciente: ')
            novo_nome = validar_nome('Digite o novo Nome do Paciente: ')
            novo_email = validar_email('Digite o novo email do Paciente: ')
            nova_senha = (input('Digite a nova senha do Paciente:'))
            novo_telefone = validar_telefone('Digite o novo telefone: ')
            novo_acompanhante = (input('O paciente terá acompanhante? (S/N): '))
            
            update_paciente(id_paciente,novo_nome,novo_email,nova_senha,novo_telefone,novo_acompanhante)

        elif opcao==4:
            id_paciente = validar_inteiro('Digite o Id do Paciente: ')
            delete_paciente(id_paciente)
        
        elif opcao == 5:
            exportar_pacientes_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 1 e 5.")

if __name__ == "__main__":
    main_paciente()
