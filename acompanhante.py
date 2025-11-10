import oracledb
import json
from utilitarios import getConnection, validar_inteiro, validar_string, validar_nome, validar_email, validar_telefone, validar_id

def create_acompanhante(id, nome, email, telefone, parentesco, id_paciente):
    """Insere um novo acompanhante e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_acompanhantes (id, nome, email, telefone, parentesco, id_paciente)
                    VALUES (:id, :nome, :email, :telefone, :parentesco, :id_paciente)
                """
                cursor.execute(sql, {
                    'id': id, 'nome': nome, 'email': email, 'telefone': telefone,
                    'parentesco': parentesco, 'id_paciente': id_paciente
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir acompanhante: {e}')
        return False

def read_acompanhante():
    """Lê e retorna uma lista de todos os acompanhantes."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, nome, email, telefone, parentesco, id_paciente FROM cc_acompanhantes ORDER BY nome"
                cursor.execute(sql)
                acompanhantes = []
                for row in cursor.fetchall():
                    acompanhantes.append({
                        'id': row[0], 'nome': row[1], 'email': row[2], 'telefone': row[3],
                        'parentesco': row[4], 'id_paciente': row[5]
                    })
                return acompanhantes
    except oracledb.Error as e:
        print(f'\n Erro ao ler acompanhantes: {e}')
        return None

def update_acompanhante(id, novo_nome, novo_email, novo_telefone, novo_parentesco, novo_id_paciente):
    """Atualiza um acompanhante e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_acompanhantes
                    SET nome = :novo_nome, email = :novo_email, telefone = :novo_telefone,
                        parentesco = :novo_parentesco, id_paciente = :novo_id_paciente
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'novo_nome': novo_nome, 'novo_email': novo_email, 'novo_telefone': novo_telefone,
                    'novo_parentesco': novo_parentesco, 'novo_id_paciente': novo_id_paciente, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar acompanhante: {e}')
        return False

def delete_acompanhante(id):
    """Exclui um acompanhante e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_acompanhantes WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir acompanhante: {e}')
        return False

def exportar_acompanhantes_json():
    """Exporta os acompanhantes para JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados dos acompanhantes para JSON...')
    acompanhantes = read_acompanhante()
    if acompanhantes is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not acompanhantes:
        print(" Nenhum acompanhante cadastrado para exportar.")
        return True

    try:
        with open('acompanhantes.json', 'w', encoding='utf-8') as f:
            json.dump(acompanhantes, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para acompanhantes.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_acompanhante():
    while True:
        print('\n**Menu - Acompanhante**')
        print('1. Inserir um novo acompanhante')
        print('2. Listar todos os acompanhantes')
        print('3. Atualizar os dados de um acompanhante')
        print('4. Excluir um acompanhante')
        print('5. Exportar Acompanhantes para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo acompanhante ***')
            id = validar_id()
            nome = validar_nome('Digite o nome do acompanhante: ')
            email = validar_email('Digite o email do acompanhante: ')
            telefone = validar_telefone('Digite o telefone do acompanhante: ')
            parentesco = validar_string('Digite o grau de parentesco: ')
            id_paciente = validar_string('Digite o ID do paciente relacionado: ')
            if create_acompanhante(id, nome, email, telefone, parentesco, id_paciente):
                print(f'\n Acompanhante {nome} (ID: {id}) foi adicionado com sucesso!')
            else:
                print('\n Falha ao adicionar o acompanhante.')

        elif opcao == 2:
            print('\n*** Listando todos os acompanhantes ***')
            acompanhantes = read_acompanhante()
            if acompanhantes is not None:
                if acompanhantes:
                    print("\n--- Lista de Acompanhantes ---")
                    for a in acompanhantes:
                        print(f"ID: {a['id']}, Nome: {a['nome']}, Email: {a['email']}, Telefone: {a['telefone']}, Parentesco: {a['parentesco']}, ID Paciente: {a['id_paciente']}")
                        print('----------------------------------')
                else:
                    print(" Nenhum acompanhante encontrado.")
            else:
                print(" Erro ao listar os acompanhantes.")

        elif opcao == 3:
            print('\n*** Atualizando um acompanhante ***')
            id = validar_string('Digite o Id do acompanhante que deseja atualizar: ')
            novo_nome = validar_nome('Digite o novo nome: ')
            novo_email = validar_email('Digite o novo email: ')
            novo_telefone = validar_telefone('Digite o novo telefone: ')
            novo_parentesco = validar_string('Digite o novo grau de parentesco: ')
            novo_id_paciente = validar_string('Digite o novo ID do paciente relacionado: ')
            
            if update_acompanhante(id, novo_nome, novo_email, novo_telefone, novo_parentesco, novo_id_paciente):
                print(f'\n Os dados do acompanhante {id} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum acompanhante com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um acompanhante ***')
            id = validar_string('Digite o Id do acompanhante que deseja excluir: ')
            if delete_acompanhante(id):
                print(f'\n O acompanhante {id} foi excluído com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum acompanhante com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 5:
            exportar_acompanhantes_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_acompanhante()