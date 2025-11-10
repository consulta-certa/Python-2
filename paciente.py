import oracledb
import json
from utilitarios import getConnection, validar_nome, validar_inteiro, validar_email, validar_telefone, validar_string, validar_id, validar_sim_nao

def create_paciente(id, nome, email, senha, telefone, acompanhantes):
    """Insere um novo paciente no banco e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO CC_pacientes (id, nome, email, senha, telefone, acompanhantes)
                    VALUES (:id, :nome, :email, :senha, :telefone, :acompanhantes)
                """
                cursor.execute(sql, {'id': id, 'nome': nome, 'email': email, 'senha': senha, 'telefone': telefone, 'acompanhantes': acompanhantes})
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir Paciente: {e}')
        return False

def read_paciente():
    """Lê e retorna uma lista de todos os pacientes do banco."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, nome, email, senha, telefone, acompanhantes FROM CC_pacientes ORDER BY nome"
                cursor.execute(sql)
                pacientes = []
                for row in cursor.fetchall():
                    pacientes.append({'id': row[0], 'nome': row[1], 'email': row[2], 'senha': row[3], 'telefone': row[4], 'acompanhantes': row[5]})
                return pacientes
    except oracledb.Error as e:
        print(f'\n Erro ao ler Pacientes: {e}')
        return None

def update_paciente(id, novo_nome, novo_email, nova_senha, novo_telefone, novo_acompanhantes):
    """Atualiza um paciente e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE CC_pacientes
                    SET nome = :novo_nome, email = :novo_email, senha = :nova_senha, telefone = :novo_telefone, acompanhantes = :novo_acompanhantes
                    WHERE id = :id
                """
                cursor.execute(sql, {'novo_nome': novo_nome, 'novo_email': novo_email, 'nova_senha': nova_senha, 'novo_telefone': novo_telefone, 'novo_acompanhantes': novo_acompanhantes, 'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar Paciente: {e}')
        return False

def delete_paciente(id):
    """Exclui um paciente e retorna True se a exclusão for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM CC_pacientes WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Paciente: {e}')
        return False

def exportar_pacientes_json():
    """Exporta os pacientes para um arquivo JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados dos pacientes para JSON...')
    pacientes = read_paciente()
    if pacientes is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not pacientes:
        print(" Nenhum paciente cadastrado para exportar.")
        return True

    try:
        with open('pacientes.json', 'w', encoding='utf-8') as f:
            json.dump(pacientes, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para pacientes.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_paciente():
    while True:
        print('\n**Menu - Paciente**')
        print('1. Inserir um novo Paciente')
        print('2. Listar todos os Pacientes')
        print('3. Atualizar os dados de um Paciente')
        print('4. Excluir um Paciente')
        print('5. Exportar Pacientes para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo paciente ***')
            id = validar_id()
            nome = validar_nome('Digite o nome do paciente: ')
            email = validar_email('Digite o email do paciente: ')
            senha = validar_string('Digite a senha do paciente: ')
            telefone = validar_telefone('Digite o telefone do paciente: ')
            acompanhantes = validar_sim_nao("O paciente terá acompanhantes? (s/n): ")
            
            if create_paciente(id, nome, email, senha, telefone, acompanhantes):
                print(f'\n Paciente {nome} (ID: {id}) foi adicionado com sucesso!')
            else:
                print('\n Falha ao adicionar o paciente.')

        elif opcao == 2:
            print('\n*** Listando todos os Pacientes ***')
            pacientes = read_paciente()
            if pacientes is not None:
                if pacientes:
                    print("\n--- Lista de Pacientes ---")
                    for p in pacientes:
                        print(f"ID: {p['id']}, Nome: {p['nome']}, Email: {p['email']}, Senha: {'*' * len(p['senha'])}, Telefone: {p['telefone']}, Acompanhantes: {p['acompanhantes']}")
                        print('----------------------------------')
                else:
                    print(" Nenhum paciente encontrado.")
            else:
                print(" Erro ao listar os pacientes.")

        elif opcao == 3:
            print('\n*** Atualizando um Paciente ***')
            id = validar_string('Digite o Id do Paciente que deseja atualizar: ')
            novo_nome = validar_nome('Digite o novo Nome do Paciente: ')
            novo_email = validar_email('Digite o novo email do Paciente: ')
            nova_senha = validar_string('Digite a nova senha do Paciente:')
            novo_telefone = validar_telefone('Digite o novo telefone: ')
            novo_acompanhantes = validar_sim_nao("O paciente terá acompanhantes? (s/n): ")
            
            if update_paciente(id, novo_nome, novo_email, nova_senha, novo_telefone, novo_acompanhantes):
                print(f'\n Os dados do Paciente {id} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum Paciente com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um Paciente ***')
            id = validar_string('Digite o Id do Paciente que deseja excluir: ')
            if delete_paciente(id):
                print(f'\n O Paciente {id} foi excluído com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum Paciente com ID {id} foi encontrado ou ocorreu um erro.')
        
        elif opcao == 5:
            exportar_pacientes_json()
    
        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_paciente()