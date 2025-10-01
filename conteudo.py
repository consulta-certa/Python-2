import oracledb
from utilitarios import getConnection,validar_inteiro,validar_string,validar_data

'''
1.8. CONTEUDO deve ser representado com as chaves: id_conteudo, tipo, titulo, texto, video,
imagem, data_publicacao

'''
#Operações CRUD
def create_conteudo(id_conteudo, tipo, titulo, texto, video, imagem, data_publicacao):
    print('*** Inserindo um novo conteudo na tabela conteudos ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO conteudos (id_conteudo, tipo, titulo, texto, video, imagem, data_publicacao)
            VALUES (:id_conteudo, :tipo, :titulo, :texto, :video, :imagem, :data_publicacao)
        """
        cursor.execute(sql, {
            'id_conteudo' : id_conteudo,
            'tipo' : tipo,
            'titulo' : titulo,
            'texto' : texto,
            'video' : video,
            'imagem' : imagem,
            'data_publicacao' : data_publicacao
        })
        conn.commit()
        print(f' O conteudo de ID: {id_conteudo}, TIPO: {tipo}, TITULO: {titulo}, TEXTO: {texto}, VIDEO: {video}, IMAGEM: {imagem} e Data de publicacao: {data_publicacao} foi adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir conteudo: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()    

#Exibir os dados de todos os conteudos
def read_conteudo():
    print('*** Lê e exibe todos os conteudos da tabela ***')
    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT id_conteudo, tipo , titulo, texto, video, imagem, data_publicacao
            FROM conteudos ORDER BY id_conteudo
        """
        cursor.execute(sql)
        print("\n --- Lista de conteudos ---")
        rows = cursor.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, tipo: {row[1]}, titulo: {row[2]}, texto: {row[3]}, video: {row[4]}, imagem: {row[5]}, data_publicacao: {row[6]}')
            print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler conteudos: {e}')
    finally:
        if conn:
            conn.close()


#Update
#Atualizar um dado de um conteudo
def update_conteudo(id_conteudo, novo_tipo, novo_titulo, novo_texto, novo_video, nova_imagem, nova_publicacao):
    print(f'Atualizando os dados do conteudo pelo ID')

    conn = getConnection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """

        UPDATE conteudos
        set tipo = :novo_tipo, titulo = :novo_titulo, texto = :novo_texto, video = :novo_video, imagem = :nova_imagem, data_publicacao = :nova_publicacao WHERE id_conteudo = :id_conteudo
        
        """
        cursor.execute(sql, {'novo_tipo' : novo_tipo, 'novo_titulo' : novo_titulo, 'novo_texto' :novo_texto, 'novo_video' : novo_video, 'nova_imagem' : nova_imagem, 'nova_publicacao' : nova_publicacao, 'id_conteudo': id_conteudo})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O novo tipo: {novo_tipo}, titulo: {novo_titulo}, texto: {novo_texto}, video: {novo_video}, imagem: {nova_imagem} e data de publicacao: {nova_publicacao} do conteudo de ID: {id_conteudo} foram atualizados!')
        else:
            print(f'Nenhum conteudo com ID {id_conteudo} foi encontrado')


    except oracledb.Error as e:
        print(f'Erro ao atualizar dado {e}')
        conn.rollback()

    finally:
        if conn:
            conn.close()

#DELETE
#remove um conteudo pelo Id

def delete_conteudo(id_conteudo):
    print(f' Excluindo o conteudo com id: {id_conteudo}')

    conn = getConnection()

    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
        DELETE FROM conteudos WHERE 
        id_conteudo=  :id_conteudo
        """
        cursor.execute(sql, {'id_conteudo' : id_conteudo})
        conn.commit()
        if cursor.rowcount >0:
            print(f'O conteudo de ID: {id_conteudo} foi excluido com sucesso!')
        else:
            print(f'Nenhum conteudo com ID {id_conteudo} foi encontrado')
        
    except oracledb.Error as e:
        print(f'Erro ao Excluir conteudo: {e}')
        conn.rollback()
        
    finally:
        if conn:
            conn.close()

    

#Programa Principal

def main_conteudo():

    while True:

        print('**Menu - conteúdo**')
        print('1. Inserir um novo conteúdo')
        print('2. Listar todos os conteúdos')
        print('3. Atualizar os dados de um conteúdo')
        print('4. Excluir um conteúdo')
        print('5. Voltar ao menu principal')

        opcao=validar_inteiro('Digite uma opção: ')
        if opcao ==1:
            id_conteudo = validar_inteiro('Digite o ID do conteúdo: ')
            tipo = validar_string('Digite o tipo do conteúdo entre FAQ ou Guia (f/gp/gt): ') 
            titulo = validar_string('Digite o titulo do conteúdo: ')
            texto= validar_string('Digite o texto: ')
            video = validar_string('Digite a URL do video: ')
            imagem = validar_string('URL da imagem: ')
            data_publicacao = validar_data('Digite a data de publicação do conteúdo: ')
            
            create_conteudo(id_conteudo,tipo,titulo,texto,video,imagem,data_publicacao)
    
        elif opcao==2:
            read_conteudo()

        elif opcao==3:
            id_conteudo = validar_inteiro('Digite o Id do conteúdo: ')
            novo_tipo = validar_string('Digite o novo tipo do conteúdo entre FAQ ou Guia (f/gp/gt): ')
            novo_titulo = validar_string('Digite o novo titulo do conteúdo: ')
            novo_texto = validar_string('Digite o novo texto: ')
            novo_video = validar_string('Digite a nova URL do video: ')
            nova_imagem = validar_string('Digite a nova Url da imagem: ')
            nova_publicacao = validar_data('Digite a nova data de publicação do conteúdo: ')
            update_conteudo(id_conteudo,novo_tipo,novo_titulo,novo_texto,novo_video,nova_imagem,nova_publicacao)

        elif opcao==4:
            id_conteudo = validar_inteiro('Digite o Id do conteudo: ')
            delete_conteudo(id_conteudo)
    
        elif opcao == 5:
            print('Encerrando o programa... volte sempre')
            break
        else:
            print("❌ Opção inválida. Tente novamente com um número inteiro entre 1 e 5.")        

main_conteudo
