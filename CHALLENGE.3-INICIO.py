

'''
Challenge 3 - Inicio
-----------------
Realizar uma DAO (Data Access Object) para gerenciar uma lista de usuários em memória.
A DAO deve permitir adicionar, remover, atualizar e listar usuários.

1.UTILIZAÇÕES EM DAO:

1.1 Cada PACIENTE deve ser representado por um dicionário com as chaves: id_paciente, nome, email e telefone.

1.2. Cada ACOMPANHANTE deve ser representado por um dicionário com as chaves: id_acompanhante,
email, telefone, parentesco e id_paciente.

1.3. CONSULTA devem ser representadas por um dicionário com as chaves: id_consulta, especialidade,
data_consulta Localdatetime, status e id_paciente.

1.4. LEMBRETE devem ser representados por um dicionário com as chaves: id_lembrete, canal_envio,
data_envio e id_consulta // Tem que ter mensagem e id_paciente para verificação?

1.5. CONTATO deve ser representado por um dicionário com as chaves: id_contato, nome, telefone,
email, numero, rua, bairro, cidade e cep.

1.6. AVALIACAO deve ser representado por um dicionário com as chaves: id_avaliacao, nota, comentario,
data_avaliacao e id_lembrete.

1.7. CONVERSA_CHATBOT deve ser representado por um dicionário com as chaves: id_conversa, pergunta e aprovacao.

1.8. CONTEUDO deve ser representado por um dicionário com as chaves: id_conteudo, tipo, titulo, texto, video,
imagem, data_publicacao

1.9. ACESSO_FUNCIONALIDADE deve ser representado por um dicionario com as chaves: id_acesso, funcionalidade,
quantidade_acessos e tempo_permanencia


2. 
fazer crud disso tudo, pqp. tem 6 dias pra isso. Slk.
like
def criar_paciente, atualizar_paciente, excluir_paciente, ler_paciente
def criar_acompanhante, atualizar_acompanhante, excluir_acompanhante, ler acompanhante
etc...

3. Realização do menu para poder acessar todo o codigo

4. Linkar essa bomba com o banco de dados para o codigo ser util

5. Acho q é isso.


def create_ceo(first_name, last_name, company, age):
    print('*** Inserindo um novo CEO na tabela CEO_DETAILS ***')
    conn = getConnection()

    #validação da conexão
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #obter um cursor
        sql = """
            INSERT INTO ceo_details (first_name, last_name, company, age)
            VALUES (:first_name, :last_name, :company, :age)
        """
        cursor.execute(sql, {
            'first_name' : first_name,
            'last_name' : last_name,
            'company' : company,
            'age' : age
        })
        conn.commit()
        print(f'CEO {first_name} {last_name} adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserior CEO: {e}')
        conn.rollback()
    finally:
        if conn:
            conn.close()   
'''
