"""
Documentação do Projeto - Gerenciamento de Dados em Python

Este projeto implementa uma camada de acesso a dados (DAO - Data Access Object) para gerenciar diversas entidades relacionadas ao contexto da aplicação, utilizando listas em memória e conexão com banco de dados Oracle.

Entidades e suas Representações:

- Paciente: dicionário com campos id_paciente, nome, email e telefone.
- Acompanhante: dicionário com campos id_acompanhante, email, telefone, parentesco e id_paciente.
- Consulta: dicionário com campos id_consulta, especialidade, data_consulta (tipo datetime), status e id_paciente.
- Lembrete: dicionário com campos id_lembrete, canal_envio, data_envio, id_consulta, além de mensagem e id_paciente para verificação.
- Contato: dicionário com campos id_contato, nome, telefone, email, numero, rua, bairro, cidade e cep.
- Avaliação: dicionário com campos id_avaliacao, nota, comentario, data_avaliacao e id_lembrete.
- Conversa_Chatbot: dicionário com campos id_conversa, pergunta e aprovacao.
- Conteúdo: dicionário com campos id_conteudo, tipo, titulo, texto, video, imagem e data_publicacao.
- Acesso_Funcionalidade: dicionário com campos id_acesso, funcionalidade, quantidade_acessos e tempo_permanencia.

Funcionalidades Implementadas:
CRUD completo (criar, ler, atualizar e excluir) para todas as entidades listadas.
Menu interativo com submenus para facilitar o acesso às operações do sistema.
Validação de dados de entrada para garantir integridade e consistência.
Tratamento de exceções para operações de inserção, alteração e exclusão.
Integração com banco de dados Oracle para persistência dos dados.
Este projeto visa organizar e facilitar o gerenciamento dos dados coletados nas disciplinas anteriores, aplicando conceitos de programação estruturada, modularização e boas práticas de desenvolvimento em Python.
"""