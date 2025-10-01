import oracledb
from utilitarios import getConnection,validar_inteiro,validar_string,validar_nome,validar_email,validar_telefone,validar_cep

'''
1.5. CONTATO deve ser representado com as chaves: id_contato, nome, telefone,
email, numero, rua, bairro, cidade e cep.'''

#Operações CRUD
def create_contato(id_contato, nome, telefone, email, numero, rua, bairro, cidade, cep):
    print('*** Inserindo um novo contato na tabela contatos ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO contatos (id_contato, nome, telefone, email, numero, rua, bairro, cidade, cep)
            VALUES (:id_contato, :nome, :telefone, :email, :numero, :rua, :bairro, :cidade, :cep)
        """
        cursor.execute(sql, {
            'id_contato' : id_contato,
            'nome' : nome,
            'telefone' : telefone,
            'email' : email,
            'numero' : numero,
            'rua' : rua,
            'bairro' : bairro,
            'cidade' : cidade,
            'cep' : cep
        })
        conn.commit()
        print(f' O contato de ID: {id_contato}, nome: {nome}, telefone: {telefone}, email: {email}, numero: {numero}, rua: {rua} e bairro: {bairro}, cidade: {cidade} e cep: {cep} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir contato: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os contatos
def read_contato():
    print('*** Lê e exibe todos os contatos da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id_contato, nome , telefone, email, numero, rua, bairro, cidade, cep
            FROM contatos ORDER BY id_contato
        """
        cursor.execute(sql)
        print("\n --- Lista de contatos ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'id: {row[0]}, nome: {row[1]}, telefone: {row[2]}, email: {row[3]}, numero: {row[4]}, rua: {row[5]}, bairro: {row[6]}, cidade: {row[7]}, cep: {row[8]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler contatos: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um contato
def update_contato(id_contato, novo_nome, novo_telefone, novo_email, novo_numero, nova_rua, novo_bairro, nova_cidade, novo_cep):
    print(f'Atualizando os dados do contato pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE contatos
        set nome = :novo_nome, telefone = :novo_telefone, email = :novo_email, numero = :novo_numero, rua = :nova_rua, bairro = :novo_bairro, cidade = :nova_cidade, cep = :novo_cep WHERE id_contato = :id_contato
        
        """
        cursor.execute(sql, {'novo_nome' : novo_nome, 'novo_telefone' : novo_telefone, 'novo_email' :novo_email, 'numero' : novo_numero, 'rua' : nova_rua, 'bairro' : novo_bairro, 'cidade' : nova_cidade, 'cep' : novo_cep, 'id_contato': id_contato})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O novo nome {novo_nome}, telefone: {novo_telefone}, email: {novo_email}, numero: {novo_numero}, rua: {nova_rua}, bairro: {novo_bairro}, cidade: {nova_cidade} e cep: {novo_cep} do contato de ID:{id_contato} foram atualizados!')
        else:
            print(f'Nenhum contato com ID {id_contato} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um contato pelo Id

def delete_contato(id_contato):
    print(f' Excluindo o contato com id: {id_contato}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM contatos WHERE 
        id_contato=  :id_contato
        """
        cursor.execute(sql, {'id_contato' : id_contato})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O contato de ID: {id_contato} foi excluido com sucesso!')
        else:
            print(f'Nenhum contato com ID {id_contato} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir contato: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_contato():

    while True:

        print('**Menu - contato**')
        print('1. Inserir um novo contato')
        print('2. Listar todos os contatos')
        print('3. Atualizar os dados de um contato')
        print('4. Excluir um contato')
        print('5. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id_contato = validar_inteiro('Digite o ID do contato: ')
            nome = validar_nome('Digite o nome do contato: ')
            telefone = validar_telefone('Digite o o telefone do contato: ')
            email= validar_email('Digite o email do contato: ')
            numero=validar_inteiro('Digite o numero da residência do contato: ')
            rua=validar_string('Digite a rua do contato: ')
            bairro=validar_string('Digite o bairro do contato: ') 
            cidade=validar_string('Digite a cidade do contato: ')
            cep=validar_cep('Digite o cep do contato: ')
            create_contato(id_contato,nome,telefone,email,numero,rua,bairro,cidade,cep)
    
        elif opcao==2:
            read_contato()

        elif opcao==3:
            id_contato = validar_inteiro('Digite o Id do contato: ')
            novo_nome = validar_nome('Digite o novo nome do contato: ')
            novo_telefone = validar_telefone('Digite o novo telefone do contato: ')
            novo_email = validar_email('Digite o novo email do contato: ')
            novo_numero = validar_inteiro('Digite o novo numero do contato: ')
            nova_rua = validar_string('Digite a nova rua do contato: ')
            novo_bairro = validar_string('Digite o novo bairro do contato: ')
            nova_cidade = validar_string('Digite a nova cidade do contato: ')
            novo_cep = validar_cep('Digite o novo cep do contato: ')
            update_contato(id_contato,novo_nome,novo_telefone,novo_email,novo_numero,nova_rua,novo_bairro,nova_cidade,novo_cep)

        elif opcao==4:
            id_contato = validar_inteiro('Digite o Id do contato: ')
            delete_contato(id_contato)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 1 e 5.")

main_contato