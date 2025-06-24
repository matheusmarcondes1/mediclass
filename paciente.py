"""
MEDICLASS: Sistema de Prontuário Eletrônico e Apoio à Decisão Clínica
Parte do Trabalho Prático de ELE078

Arquivo: paciente.py
Autor: Matheus Marcondes <matheusmarcondes@ufmg.br>
Data de criação: 2025-06-21
Descrição:
    Módulo responsável pela classe Paciente, incluindo persistência de histórico médico,
    registro de entrada, atualização e consulta de histórico, e gerenciamento de exames.
Repositório: 
Licença: MIT License
Dependências:
    os, datetime
"""

import os
from datetime import date, datetime

class Paciente:       # Representa um paciente no sistema Mediclass.

    def __init__(
        self,
        nome: str,
        cpf: str,
        contato: str,
        convenio: str,
        data_nascimento: date,
        leito: str,
        enfermeiro_triagem: str
    ):

        self.cpf = cpf
        self.nome = nome
        self.contato = contato
        self.convenio = convenio
        self.data_nascimento = data_nascimento
        self.leito = leito
        self.data_entrada = None
        self.enfermeiro_triagem = enfermeiro_triagem
        self.resultados_exames = []
        self.prioritario = False

        # cria diretório de históricos se não existir
        os.makedirs('historicos', exist_ok=True)        # garante que a pasta historicos existe antes de gravar qualquer arquivo
        self._historico_file = os.path.join('historicos', f"{self.cpf}.txt")       # cria caminho do histórico a ser gravado utilizando CPF

        # checa a prexistencia do arquivo a ser gravado e inicializa arquivo de historico
        if not os.path.exists(self._historico_file):
            with open(self._historico_file, 'w', encoding='utf-8') as f:
                f.write(f"Histórico de {self.nome} (CPF: {self.cpf})\n")
                f.write(f"Criado em: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
                f.write('-' * 50 + '\n')

    def registrar_entrada(self) -> None:
        self.data_entrada = datetime.now().date()                                # registra a entrada no historico com timestamp
        registro = f"Entrada no leito {self.leito} em {self.data_entrada}"        
        self.atualizar_historico(registro)

    def atualizar_historico(self, registro: str) -> None:                        # cria padrao para adicoes no historico, várias funções dependem dela
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self._historico_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {registro}\n")

    def consultar_historico(self) -> str:                                        # apenas retorna o historico no prompt
        with open(self._historico_file, 'r', encoding='utf-8') as f:
            return f.read()

    def adicionar_exame(self, exame: str, resultado: str) -> None:               # registro de um exame no histórico
        self.resultados_exames.append({'exame': exame, 'resultado': resultado})
        registro = f"Exame: {exame} | Resultado: {resultado}"
        self.atualizar_historico(registro)
