# Sistema Consulta Certa - Gerenciamento em Python com Oracle DB

## Descrição

Este projeto implementa um sistema de gerenciamento para uma clínica fictícia chamada **Consulta Certa**, utilizando Python para realizar operações CRUD (Criar, Ler, Atualizar, Excluir) em diversas entidades relacionadas ao atendimento médico.

O sistema conecta-se a um banco de dados Oracle para persistência dos dados e oferece menus interativos para facilitar o uso.

---

## Funcionalidades

- Gerenciamento de **Pacientes**, **Acompanhantes**, **Consultas**, **Lembretes**, **Contatos**, **Avaliações**, **Conversas com Chatbot**, **Conteúdos** e **Acessos de Funcionalidade**.
- Operações CRUD completas para cada entidade.
- Validação robusta de dados de entrada (nomes, emails, telefones, datas, booleanos, etc.).
- Tratamento de erros e exceções para garantir a integridade dos dados.
- Menus interativos com submenus para facilitar a navegação.
- Conexão com banco Oracle usando a biblioteca `oracledb`.

---

## Requisitos

- Python 3.7 ou superior
- Biblioteca `oracledb`
- Biblioteca `regex`

### Instalação das dependências

```
pip install oracledb regex
```

### Como usar
Configure o arquivo utilitarios.py com as credenciais corretas do banco Oracle (usuário, senha, host, porta e service_name).


## Execute o arquivo principal main.py:
```
python main.py
```
Navegue pelo menu principal para acessar os submenus de cada entidade.

Utilize as opções para inserir, listar, atualizar ou excluir registros.

## Estrutura do projeto
utilitarios.py: funções utilitárias para conexão com banco e validação de dados.
paciente.py: CRUD e menu para pacientes.
acompanhante.py: CRUD e menu para acompanhantes.
consulta.py: CRUD e menu para consultas.
lembrete.py: CRUD e menu para lembretes.
contato.py: CRUD e menu para contatos.
avaliacao.py: CRUD e menu para avaliações.
conversa_chatbot.py: CRUD e menu para conversas com chatbot.
conteudo.py: CRUD e menu para conteúdos.
acesso_funcionalidade.py: CRUD e menu para acessos de funcionalidade.
main.py: menu principal que integra todos os módulos.

## Observações
As validações garantem que os dados inseridos estejam no formato correto, evitando erros no banco.
O sistema foi desenvolvido para fins acadêmicos e pode ser expandido conforme necessidade.
As senhas dos pacientes são armazenadas em texto puro no banco, o que não é recomendado para ambientes reais. Para produção, utilize hashing seguro (Proximos Passos).


Autores
[Felipe Ferrete]
[Gustavo Bosak]
[Nikolas Brisola]
Vídeo explicativo - YOUTUBE
Link para o vídeo explicativo do projeto: [inserir link do YouTube]