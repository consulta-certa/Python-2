from paciente import main_paciente
from acompanhante import main_acompanhante
from consulta import main_consulta
from lembrete import main_lembrete
from contato import main_contato
from avaliacao import main_avaliacao
from conversa_chatbot import main_conversa_chatbot
from conteudo import main_conteudo
from acesso_funcionalidade import main_acesso
from utilitarios import validar_inteiro
from integracao import menu_integracoes



def exibir_menu():
    """Exibe as opções do menu principal."""
    print("\n" + "="*40)
    print("==== Sistema Consulta Certa ====")
    print("="*40)
    print("1.  Gerenciar Pacientes.")
    print("2.  Gerenciar Acompanhantes.")
    print("3.  Gerenciar Consultas.")
    print("4.  Gerenciar Lembretes.")
    print("5.  Gerenciar Contatos.")
    print("6.  Gerenciar Avaliações.")
    print("7.  Gerenciar Conversas Chatbot.")
    print("8.  Gerenciar Conteúdos.")
    print("9.  Gerenciar Acessos de Funcionalidade")
    print("10. Gerenciar Integrações (Exportar Json/ViaCep)")
    print("0. Sair: Encerra o Sistema Consulta Certa.")
    print("="*40)


def main():
    while True:
        exibir_menu()
        
        opcao = validar_inteiro("Escolha uma opção de 0 a 10: ")

        if opcao == 1:
            main_paciente()
        elif opcao == 2:
            main_acompanhante()
        elif opcao == 3:
            main_consulta()
        elif opcao == 4:
            main_lembrete()
        elif opcao == 5:
            main_contato()
        elif opcao == 6:
            main_avaliacao()
        elif opcao == 7:
            main_conversa_chatbot()
        elif opcao == 8:
            main_conteudo()
        elif opcao == 9:
            main_acesso()
        elif opcao == 10:
            menu_integracoes()
        elif opcao == 0:
            print("\n👋 Encerrando o sistema... até logo!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente com um número inteiro entre 0 e 9.")


if __name__ == "__main__":
    main()