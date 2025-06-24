"""
MEDICLASS: Sistema de Prontuário Eletrônico e Apoio À Decisão Clínica
Parte do Trabalho Prático de ELE078

Arquivo: sistema.py
Autor: Matheus Marcondes <matheusmarcondes@ufmg.br>
Data de criação: 2025-06-21
Descrição:
    Módulo principal com a classe SistemaMediclass,
    responsável pela interface via prompt e fluxos de login, cadastro, triagem,
    diagnóstico, visualização, exportação de prontuário em TXT e adição de exames por técnico,
    mantendo dados em memória.
Repositório: 
Licença: MIT License
Dependências:
    sys, datetime, profissionais, paciente
"""

import sys
from datetime import date

from profissionais import Medico, Enfermeiro, Tecnico, Profissional
from paciente import Paciente

class SistemaMediclass:
    def __init__(self):
        # armazenamento em memória de Profissionais (usuarios) e pacientes
        self.usuarios: dict[str, Profissional] = {}
        self.pacientes: dict[str, Paciente] = {}
        
    # adiciona usuario
    def registrar_usuario(self, usuario: Profissional) -> None:
        self.usuarios[usuario.login] = usuario
        
    # LOGIN
    def login(self) -> Profissional | None:
        login = input("Login: ")
        senha = input("Senha: ")
        usuario = self.usuarios.get(login)
        if usuario and usuario.autenticar(senha):
            print(f"Bem-vindo(a), {usuario.nome}!")
            return usuario
        print("Credenciais inválidas.")
        return None

    def menu_principal(self, usuario: Profissional) -> None:
        while True:
            print("\n--- Menu Principal ---")
            print("1. Registrar entrada de paciente")
            print("2. Realizar triagem (enfermeiro)")
            print("3. Realizar consulta (médico)")
            print("4. Visualizar prontuário")
            print("5. Exportar prontuário (.txt)")
            print("6. Adicionar exame (técnico)")
            print("0. Logout")
            escolha = input("Escolha uma opção: ")
            if escolha == '0':
                print("Logout realizado.")
                break
            elif escolha == '1':
                self.op_registrar_entrada(usuario)
            elif escolha == '2':
                self.op_triagem(usuario)
            elif escolha == '3':
                self.op_diagnostico(usuario)
            elif escolha == '4':
                self.op_visualizar_prontuario(usuario)
            elif escolha == '5':
                self.op_exportar_prontuario(usuario)
            elif escolha == '6':
                self.op_adicionar_exame(usuario)
            else:
                print("Opção inválida.")

    def op_registrar_entrada(self, usuario: Profissional) -> None:
        cpf = input("CPF do paciente: ")
        paciente = self.pacientes.get(cpf)
        if not paciente:
            print("Paciente não encontrado. Cadastrando novo.")
            nome = input("Nome completo: ")
            contato = input("Contato: ")
            convenio = input("Convênio: ")
            while True:
                data_str = input("Data de nascimento (YYYY-MM-DD): ")
                try:
                    data_nasc = date.fromisoformat(data_str)
                    break
                except ValueError:
                    print("Formato inválido. Use YYYY-MM-DD.")
            leito = input("Leito: ")
            enfermeiro = usuario.nome if isinstance(usuario, Enfermeiro) else ''
            paciente = Paciente(
                nome=nome,
                cpf=cpf,
                contato=contato,
                convenio=convenio,
                data_nascimento=data_nasc,
                leito=leito,
                enfermeiro_triagem=enfermeiro
            )
            paciente.ultima_anamnese = None
            self.pacientes[cpf] = paciente
        else:
            if not hasattr(paciente, 'ultima_anamnese'):
                paciente.ultima_anamnese = None
        paciente.registrar_entrada()
        print("Entrada registrada.")


    def op_triagem(self, usuario: Profissional) -> None:
        if not isinstance(usuario, Enfermeiro):        # controla acesso ao método triagem para Enf
            print("Acesso negado. Apenas enfermeiros podem realizar triagem.")
            return
        cpf = input("CPF do paciente: ")               # busca paciente pelo CPF
        paciente = self.pacientes.get(cpf)
        if not paciente:
            print("Paciente não encontrado.")
            return
        usuario.triagem(paciente)                      # conduz triagem e retorna ao menu
        print("Triagem concluída.")

    def op_diagnostico(self, usuario: Profissional) -> None:
        if not isinstance(usuario, Medico):            # controla acesso ao método para Med
            print("Acesso negado. Apenas médicos podem iniciar consultas.")
            return
        cpf = input("CPF do paciente: ")              # busca paciente pelo CPF
        paciente = self.pacientes.get(cpf)
        if not paciente:
            print("Paciente não encontrado.")
            return
        sugestoes = usuario.sugerir_diagnosticos(paciente)
        if not sugestoes:                             # caso Diagnostico nulo/inconclusivo
            print("Nenhum diagnóstico sugerido.")
            return
        print("--- Diagnósticos sugeridos ---")
        for diag in sugestoes:                        # printa possiveis Diagnosticos
            print(str(diag))

        # PÓS CONSULTA
        if input("Deseja solicitar exame a um técnico? (S/N): ").strip().upper() == 'S':
            print("Solicitação enviada.")
            paciente.atualizar_historico("Solicitação de exame enviada ao técnico.")
            
        if input("Deseja gerar receituário? (S/N): ").strip().upper() == 'S':
            usuario.gerar_receituario(paciente)
            
        if input("Deseja gerar declaração de comparecimento? (S/N): ").strip().upper() == 'S':
            usuario.gerar_declaracao_comparecimento(paciente)
            
        print("Consulta encerrada. Retornando ao menu.")
        self.menu_principal(usuario)                                # redundancia para retornar ao menu
        return

    def op_visualizar_prontuario(self, usuario: Profissional) -> None:
        cpf = input("CPF do paciente: ")                                    # busca paciente pelo CPF
        paciente = self.pacientes.get(cpf)
        if not paciente:
            print("Paciente não encontrado.")
            return

        # imprime informações do prontuario no prompt
        print(f"\n=== Prontuário de {paciente.nome} ===")
        print(f"CPF: {paciente.cpf}")
        print(f"Contato: {paciente.contato}")
        print(f"Convênio: {paciente.convenio}")
        print(f"Data de nascimento: {paciente.data_nascimento.isoformat()}")
        print(f"Leito: {paciente.leito}")
        print(f"Enfermeiro: {paciente.enfermeiro_triagem}")
        print(f"Prioritário: {'Sim' if paciente.prioritario else 'Não'}")
        print("\n--- Histórico Médico ---")
        print(paciente.consultar_historico())
        if hasattr(paciente, 'ultima_anamnese') and paciente.ultima_anamnese:    # posta a ultima anamnese se existente
            print("\n--- Última Anamnese ---")
            for k, v in paciente.ultima_anamnese.to_dict().items():
                print(f"{k}: {v}")
        else:
            print("Nenhuma anamnese disponível.")

    def op_exportar_prontuario(self, usuario: Profissional) -> None:
        cpf = input("CPF do paciente para exportação: ")                        # busca paciente pelo cpf
        paciente = self.pacientes.get(cpf)
        if not paciente:
            print("Paciente não encontrado.")
            return   

        # cria arquivo para exportacao com dados registrados
        filename = f"prontuario_{paciente.cpf}.txt"
        conteudo = [
            f"Prontuário de {paciente.nome}",
            f"CPF: {paciente.cpf}",
            f"Contato: {paciente.contato}",
            f"Convênio: {paciente.convenio}",
            f"Data de nascimento: {paciente.data_nascimento.isoformat()}",
            f"Leito: {paciente.leito}",
            f"Enfermeiro: {paciente.enfermeiro_triagem}",
            f"Prioritário: {'Sim' if paciente.prioritario else 'Não'}",
            "\nHistórico Médico:",
            paciente.consultar_historico()
        ]

        if hasattr(paciente, 'ultima_anamnese') and paciente.ultima_anamnese:    # coloca informações da ultima anamnese (se existente) no arquivo
            conteudo.append("\nÚltima Anamnese:")
            for k, v in paciente.ultima_anamnese.to_dict().items():
                conteudo.append(f"{k}: {v}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(conteudo))
        print(f"Prontuário exportado para {filename}")

    def op_adicionar_exame(self, usuario: Profissional) -> None:
        
        if not isinstance(usuario, Tecnico):        # controla acesso ao método para Tec
            print("Acesso negado. Apenas técnicos podem adicionar exames.")
            return
            
        cpf = input("CPF do paciente para adicionar exame: ")    # busca paciente pelo CPF
        paciente = self.pacientes.get(cpf)
        if not paciente:
            print("Paciente não encontrado.")
            return
        usuario.adicionar_exame_sistema(paciente)

    def executar(self) -> None:
        """
        Executa o loop principal (login + menu), permitindo logout sem perda de dados.
        """
        while True:
            usuario = self.login()
            if not usuario:
                print("Encerrando sistema.")
                break
            self.menu_principal(usuario)

if __name__ == "__main__":
    sistema = SistemaMediclass()
    sistema.registrar_usuario(Medico("Dr. Teste", "CRM123", "med", "senha"))
    sistema.registrar_usuario(Enfermeiro("Enf. Teste", "COREN456", "enf", "senha"))
    sistema.registrar_usuario(Tecnico("Tec. Teste", "CRTR789", "tec", "senha"))
    sistema.executar()
