import oracledb
import json
from utilitarios import getConnection,validar_inteiro,validar_string,validar_data, validar_id, validar_tipo

#Operações CRUD
def create_conteudo(id, tipo, titulo, texto, video, imagem, data_publicacao):
    print('*** Inserindo um novo conteúdo na tabela cc_conteudos ***')
    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO cc_conteudos (id, tipo, titulo, texto, video, imagem, data_publicacao)
            VALUES (:id, :tipo, :titulo, :texto, :video, :imagem, :data_publicacao)
        """
        cursor.execute(sql, {
            'id' : id,
            'tipo' : tipo,
            'titulo' : titulo,
            'texto' : texto,
            'video' : video,
            'imagem' : imagem,
            'data_publicacao' : data_publicacao
        })
        conn.commit()
        print(f' O conteúdo de ID: {id}, Título: {titulo} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir conteúdo: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os conteudos
def read_conteudo():
    print('*** Lê e exibe todos os conteúdos da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id, tipo , titulo, texto, video, imagem, data_publicacao
            FROM cc_conteudos ORDER BY data_publicacao DESC
        """
        cursor.execute(sql)
        print("\n --- Lista de conteúdos ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Tipo: {row[1]}, Título: {row[2]}, Data: {row[6].strftime("%d/%m/%Y")}\nTexto: {row[3]}\nVideo: {row[4]}\nImagem: {row[5]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler conteúdos: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um conteudo
def update_conteudo(id, novo_tipo, novo_titulo, novo_texto, novo_video, nova_imagem, nova_data_publicacao):
    print(f'Atualizando os dados do conteúdo pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE cc_conteudos
        SET tipo = :novo_tipo, titulo = :novo_titulo, texto = :novo_texto, video = :novo_video, imagem = :nova_imagem, data_publicacao = :nova_data_publicacao WHERE id = :id
        """
        cursor.execute(sql, {'novo_tipo' : novo_tipo, 'novo_titulo' : novo_titulo, 'novo_texto' :novo_texto, 'novo_video' : novo_video, 'nova_imagem' : nova_imagem, 'nova_data_publicacao' : nova_data_publicacao, 'id': id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'O conteúdo de ID {id} foi atualizado com sucesso!')
        else:
            print(f'Nenhum conteúdo com ID {id} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um conteudo pelo Id
def delete_conteudo(id):
    print(f' Excluindo o conteúdo com id: {id}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """DELETE FROM cc_conteudos WHERE id = :id"""
        cursor.execute(sql, {'id' : id})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'O conteúdo de ID: {id} foi excluido com sucesso!')
        else:
            print(f'Nenhum conteúdo com ID {id} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir conteúdo: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

def exportar_conteudos_json():
    '''
    Exporta todos os conteúdos cadastrados no banco Oracle
    para um arquivo local 'conteudos.json'.
    '''
    print('\n📤 Exportando dados dos conteúdos para JSON...')

    conn = getConnection()
    if not conn:
        print('Não foi possível conectar ao banco.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, tipo, titulo, texto, video, imagem, TO_CHAR(data_publicacao, 'DD/MM/YYYY') as data_formatada
            FROM cc_conteudos ORDER BY data_publicacao DESC
        """)
        rows = cursor.fetchall()

        conteudos = [
            {'id': row[0], 'tipo': row[1],'titulo': row[2],'texto': row[3], 'video': row[4], 'imagem': row[5], 'data_publicacao': row[6]}
            for row in rows
        ]

        with open('conteudos.json', 'w', encoding='utf-8') as f:
            json.dump(conteudos, f, ensure_ascii=False, indent=4)

        print('Dados exportados com sucesso para conteudos.json.')

    except Exception as e:
        print(f'Erro ao exportar: {e}')
    finally:
        conn.close()
    

#Programa Principal
def main_conteudo():

    while True:

        print('\n**Menu - Conteúdo**')
        print('1. Inserir um novo conteúdo')
        print('2. Listar todos os conteúdos')
        print('3. Atualizar os dados de um conteúdo')
        print('4. Excluir um conteúdo')
        print('5. Exportar Conteúdos para Json')
        print('6. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao ==1:
            id = validar_id()
            tipo = validar_tipo('Digite o tipo do conteúdo (f/p/t/i): ') 
            titulo = validar_string('Digite o titulo do conteúdo: ')
            texto = validar_string('Digite o texto: ')
            video = validar_string('Digite a URL do video: ')
            imagem = validar_string('Digite a URL da imagem: ')
            data_publicacao = validar_data('Digite a data de publicação (DD/MM/AAAA HH:MM): ')
            
            create_conteudo(id, tipo, titulo, texto, video, imagem, data_publicacao)
    
        elif opcao==2:
            read_conteudo()

        elif opcao==3:
            id = validar_string('Digite o Id do conteúdo que deseja atualizar: ')
            novo_tipo = validar_tipo('Digite o novo tipo do conteúdo (f/p/t/i): ')
            novo_titulo = validar_string('Digite o novo titulo do conteúdo: ')
            novo_texto = validar_string('Digite o novo texto: ')
            novo_video = validar_string('Digite a nova URL do video: ')
            nova_imagem = validar_string('Digite a nova URL da imagem: ')
            nova_data_publicacao = validar_data('Digite a nova data de publicação (DD/MM/AAAA HH:MM): ')
            update_conteudo(id, novo_tipo, novo_titulo, novo_texto, novo_video, nova_imagem, nova_data_publicacao)

        elif opcao==4:
            id = validar_string('Digite o Id do conteudo que deseja excluir: ')
            delete_conteudo(id)

        elif opcao == 5:
            exportar_conteudos_json()
    
        elif opcao == 6:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_conteudo()