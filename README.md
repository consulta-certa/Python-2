# Sistema Consulta Certa - Gerenciamento em Python com Oracle DB

## 📝 Descrição

Este projeto implementa um sistema de back-end em **Python** para gerenciar as operações de uma clínica fictícia chamada **Consulta Certa**. O sistema é robusto, modular e interage diretamente com um banco de dados **Oracle**, garantindo a persistência e a consistência dos dados.

A arquitetura foi desenhada para servir como a camada de dados para um sistema de front-end (como um site ou aplicativo móvel), oferecendo uma interface de linha de comando (CLI) para realizar todas as operações administrativas.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Banco de Dados:** Oracle DB
- **Bibliotecas Principais:**
  - `oracledb`: Para conexão e comunicação com o banco de dados Oracle.
  - `requests`: Para o consumo da API externa de busca de UBS.
  - `json`: Para a exportação de dados.

---

## ✨ Funcionalidades Principais

- **Gerenciamento Completo (CRUD):**
  - Módulos completos para gerenciar **Pacientes, Acompanhantes, Consultas, Lembretes, Contatos, Avaliações, Conversas com Chatbot, Conteúdos e Acessos**.
  - Cada módulo permite **Inserir, Consultar, Atualizar e Excluir** registros.

- **Validação de Dados:**
  - Um módulo de utilitários centraliza a validação de todas as entradas, como e-mails, telefones, CEPs, datas e outros formatos, garantindo a integridade dos dados.

- **Exportação de Dados:**
  - Todos os módulos de CRUD incluem uma funcionalidade para **exportar os dados consultados para um arquivo `.json`**, facilitando a integração e a análise de dados.

- **Consumo de API Externa:**
  - O sistema consome uma **API REST externa** (hospedada no Render) para buscar Unidades Básicas de Saúde (UBS) próximas a um CEP informado.

- **Menus Interativos:**
  - Uma interface de linha de comando (CLI) com menus e submenus que guiam o usuário de forma intuitiva através das operações.

---

## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:**
    - Ter o Python 3 instalado.
    - Ter acesso a um banco de dados Oracle e as credenciais de conexão.
    - Instalar as bibliotecas necessárias:
      ```bash
      pip install oracledb requests
      ```

2.  **Configuração:**
    - Atualize as credenciais de conexão com o banco de dados no arquivo `utilitarios.py` ou onde a função `getConnection` estiver definida.

3.  **Execução:**
    - Para iniciar o sistema, execute o arquivo `main.py` no seu terminal:
      ```bash
      python main.py
      ```
    - Navegue pelos menus para acessar as funcionalidades desejadas.

---

## 👨‍💻 Autores

- **Felipe Ferrete** - RM562999
- **Gustavo Bosak** - RM566315
- **Nikolas Brisola** - RM564371

---

## 🎥 Vídeo Explicativo - YouTube

Assista à nossa demonstração completa do projeto, explicando a arquitetura do código e mostrando o sistema em ação:

**[Link para o vídeo explicativo do projeto](https://youtu.be/IXAUbEz6NIw)**
