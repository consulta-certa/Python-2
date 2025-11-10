import oracledb
import json
from utilitarios import getConnection, validar_inteiro, validar_string, validar_data, validar_id, validar_tipo

def create_conteudo(id, tipo, titulo, texto, video, imagem, data_publicacao):
    """Cria um novo conteúdo e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO cc_conteudos (id, tipo, titulo, texto, video, imagem, data_publicacao)
                    VALUES (:id, :tipo, :titulo, :texto, :video, :imagem, :data_publicacao)
                """
                cursor.execute(sql, {
                    'id': id, 'tipo': tipo, 'titulo': titulo, 'texto': texto,
                    'video': video, 'imagem': imagem, 'data_publicacao': data_publicacao
                })
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'Erro ao inserir conteúdo: {e}')
        return False

def read_conteudo():
    """Lê e retorna uma lista de todos os conteúdos."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    SELECT id, tipo, titulo, texto, video, imagem, data_publicacao
                    FROM cc_conteudos ORDER BY data_publicacao DESC
                """
                cursor.execute(sql)
                conteudos = []
                for row in cursor.fetchall():
                    conteudos.append({
                        'id': row[0], 'tipo': row[1], 'titulo': row[2], 'texto': row[3],
                        'video': row[4], 'imagem': row[5], 'data_publicacao': row[6]
                    })
                return conteudos
    except oracledb.Error as e:
        print(f'Erro ao ler conteúdos: {e}')
        return None

def update_conteudo(id, novo_tipo, novo_titulo, novo_texto, novo_video, nova_imagem, nova_data_publicacao):
    """Atualiza um conteúdo e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE cc_conteudos
                    SET tipo = :novo_tipo, titulo = :novo_titulo, texto = :novo_texto, video = :novo_video,
                        imagem = :nova_imagem, data_publicacao = :nova_data_publicacao
                    WHERE id = :id
                """
                cursor.execute(sql, {
                    'novo_tipo': novo_tipo, 'novo_titulo': novo_titulo, 'novo_texto': novo_texto,
                    'novo_video': novo_video, 'nova_imagem': nova_imagem,
                    'nova_data_publicacao': nova_data_publicacao, 'id': id
                })
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'Erro ao atualizar conteúdo: {e}')
        return False

def delete_conteudo(id):
    """Exclui um conteúdo e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cc_conteudos WHERE id = :id"
                cursor.execute(sql, {'id': id})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'Erro ao excluir conteúdo: {e}')
        return False

def exportar_conteudos_json():
    """Exporta os conteúdos para JSON e retorna True em caso de sucesso."""
    print('Exportando dados dos conteúdos para JSON...')
    conteudos = read_conteudo()
    if conteudos is None:
        print('Nao foi possivel obter os dados para exportar.')
        return False
    if not conteudos:
        print("Nenhum conteúdo encontrado para exportar.")
        return True

    try:
        with open('conteudos.json', 'w', encoding='utf-8') as f:
            json.dump(conteudos, f, ensure_ascii=False, indent=4, default=str)
        print('Dados exportados com sucesso para conteudos.json.')
        return True
    except IOError as e:
        print(f'Erro ao escrever o arquivo JSON: {e}')
        return False

def main_conteudo():
    while True:
        print('\n**Menu - Conteúdo**')
        print('1. Inserir um novo conteúdo')
        print('2. Listar todos os conteúdos')
        print('3. Atualizar os dados de um conteúdo')
        print('4. Excluir um conteúdo')
        print('5. Exportar Conteúdos para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo conteúdo ***')
            id = validar_id()
            tipo = validar_tipo('Digite o tipo do conteúdo (f/p/t/i): ')
            titulo = validar_string('Digite o titulo do conteúdo: ')
            texto = validar_string('Digite o texto: ')
            video = validar_string('Digite a URL do video: ')
            imagem = validar_string('Digite a URL da imagem: ')
            data_publicacao = validar_data('Digite a data de publicação (DD/MM/AAAA HH:MM): ')
            if create_conteudo(id, tipo, titulo, texto, video, imagem, data_publicacao):
                print(f'O conteúdo de ID: {id}, Título: {titulo} foi adicionado com sucesso!')
            else:
                print('Falha ao inserir o conteúdo.')

        elif opcao == 2:
            print('\n*** Listando todos os conteúdos ***')
            conteudos = read_conteudo()
            if conteudos is not None:
                if conteudos:
                    print("\n--- Lista de Conteúdos ---")
                    for c in conteudos:
                        data_formatada = c['data_publicacao'].strftime('%d/%m/%Y') if c['data_publicacao'] else ''
                        print(f"ID: {c['id']}, Tipo: {c['tipo']}, Título: {c['titulo']}, Data: {data_formatada}")
                        print(f"Texto: {c['texto']}")
                        print(f"Video: {c['video']}")
                        print(f"Imagem: {c['imagem']}")
                        print('----------------------------------')
                else:
                    print("Nenhum conteúdo encontrado.")
            else:
                print("Erro ao listar os conteúdos.")

        elif opcao == 3:
            print('\n*** Atualizando um conteúdo ***')
            id = validar_string('Digite o Id do conteúdo que deseja atualizar: ')
            novo_tipo = validar_tipo('Digite o novo tipo do conteúdo (f/p/t/i): ')
            novo_titulo = validar_string('Digite o novo titulo do conteúdo: ')
            novo_texto = validar_string('Digite o novo texto: ')
            novo_video = validar_string('Digite a nova URL do video: ')
            nova_imagem = validar_string('Digite a nova URL da imagem: ')
            nova_data_publicacao = validar_data('Digite a nova data de publicação (DD/MM/AAAA HH:MM): ')
            if update_conteudo(id, novo_tipo, novo_titulo, novo_texto, novo_video, nova_imagem, nova_data_publicacao):
                print(f'O conteúdo de ID {id} foi atualizado com sucesso!')
            else:
                print(f'Falha ao atualizar. Nenhum conteúdo com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um conteúdo ***')
            id = validar_string('Digite o Id do conteudo que deseja excluir: ')
            if delete_conteudo(id):
                print(f'O conteúdo de ID: {id} foi excluido com sucesso!')
            else:
                print(f'Falha ao excluir. Nenhum conteúdo com ID {id} foi encontrado ou ocorreu um erro.')

        elif opcao == 5:
            exportar_conteudos_json()

        elif opcao == 6:
            print('Retornando ao menu principal...')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_conteudo()