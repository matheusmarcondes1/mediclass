"""
MEDICLASS: Sistema de Prontuário Eletrônico e Apoio à Decisão Clínica
Parte do Trabalho Prático de ELE078

Arquivo: profissionais.py
Autor: Matheus Marcondes <matheusmarcondes@ufmg.br>
Data de criação: 2025-06-21
Descrição:
    Módulo responsável pela superclasse Profissional e subclasses Medico, Enfermeiro e Tecnico,
    incluindo encapsulamento de atributos protegidos, métodos de login, hash de senha e lógica de decisão clínica.
Repositório: 
Licença: MIT License
Dependências:
    hashlib, typing, paciente, anamnese, diagnostico
"""

import hashlib
from typing import Any
from enum import Enum
from paciente import Paciente
from anamnese import Anamnese, TipoSintoma
from diagnostico import Diagnostico
from datetime import date, datetime


class Profissional:
    """
    Superclasse para usuários profissionais do sistema Mediclass.
    """
    def __init__(self, nome: str, registro_profissional: str, login: str, senha: str):
        self.nome = nome
        self.registro_profissional = registro_profissional
        self.login = login
        self._senha_hash = self._hash_senha(senha)

    def _hash_senha(self, senha: str) -> str:
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def autenticar(self, senha: str) -> bool:
        return self._senha_hash == hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def adicionar_paciente(self, paciente: Any) -> None:
        raise NotImplementedError("Implementar cadastro de paciente")

    def editar_paciente(self, paciente: Any) -> None:
        raise NotImplementedError("Implementar edição de paciente")

class Medico(Profissional):
    """
    Profissional com permissões de médico, capaz de sugerir diagnósticos.
    """
    def sugerir_diagnosticos(self, paciente: Paciente) -> list[Diagnostico]:
        anamnese = getattr(paciente, 'ultima_anamnese', None)
        if not anamnese:
            print("Nenhuma triagem disponível para este paciente.")
            return []

        sugestoes: list[Diagnostico] = []
        tipo = anamnese.tipo_sintoma

        # Gastrointestinal
        if tipo == TipoSintoma.GASTROINTESTINAL:
            print("Categoria: Gastrointestinal")
            print("1. Desconforto abdominal\n2. Disfunção intestinal\n3. Dor aguda")
            escolha = input("Selecione o subgrupo (1-3): ")
            if escolha == '1':
                resp = input("Dor no hipocôndrio direito pós-prandial? (S/N): ").strip().upper()
                if resp == 'S':
                    sugestoes.append(Diagnostico('Gastrointestinal', 'Possível colecistite', ['Ultrassonografia abdominal']))
            elif escolha == '2':
                resp = input("Febre + náuseas + diarreia? (S/N): ").strip().upper()
                if resp == 'S':
                    sugestoes.append(Diagnostico('Gastrointestinal', 'Possível gastroenterite infecciosa', ['Hemograma', 'Coprocultura']))
            elif escolha == '3':
                if input("Apresenta febre? (S/N): ").strip().upper() == 'S':
                    if input("Dor em fossa ilíaca direita? (S/N): ").strip().upper() == 'S':
                        sugestoes.append(Diagnostico('Gastrointestinal', 'Possível apendicite', ['Ultrassonografia abdominal']))
                    elif input("Dor no hipogástrio? (S/N): ").strip().upper() == 'S':
                        sugestoes.append(Diagnostico('Gastrointestinal', 'Possível cálculo renal', ['Radiografia de abdome sem preparo']))

        # Respiratório
        elif tipo == TipoSintoma.RESPIRATORIO:
            print("Categoria: Respiratório")
            print("1. Tosse aguda\n2. Dispneia\n3. Dor torácica pleurítica")
            escolha = input("Selecione o subgrupo (1-3): ")
            if escolha == '1':
                if input("Febre + congestão + estertores unilaterais? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Respiratório', 'Possível pneumonia', ['Radiografia de tórax']))
                elif input("Sem febre, pouca expectoração? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Respiratório', 'Possível bronquite aguda', ['Manejo sintomático']))
            elif escolha == '2':
                if input("Início súbito com chiado e histórico asmático? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Respiratório', 'Possível exacerbação de asma', ['Espirometria ou PEFR']))
            elif escolha == '3':
                if input("Dor ao respirar fundo + tosse seca? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Respiratório', 'Possível pleurite', ['Radiografia de tórax', 'Ultrassonografia pleural']))

        # Cardiovascular
        elif tipo == TipoSintoma.CARDIOVASCULAR:
            print("Categoria: Cardiovascular")
            print("1. Dor torácica\n2. Palpitações\n3. Dispneia")
            escolha = input("Selecione o subgrupo (1-3): ")
            if escolha == '1':
                if input("Dor opressiva no centro do tórax, irradia para braço ou mandíbula? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Cardiovascular', 'Possível IAM', ['ECG', 'Marcadores cardíacos']))
                elif input("Dor desencadeada por esforço, aliviada com repouso? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Cardiovascular', 'Possível angina instável', ['Teste ergométrico', 'Perfusão']))
            elif escolha == '2':
                if input("Ritmo irregular e rápido? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Cardiovascular', 'Possível arritmia supraventricular', ['ECG']))
            elif escolha == '3':
                if input("Dispneia aos mínimos esforços + edema de membros inferiores? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Cardiovascular', 'Possível insuficiência cardíaca', ['BNP', 'Ecocardiograma']))

        # Trauma
        elif tipo == TipoSintoma.TRAUMA:
            print("Categoria: Trauma")
            print("1. Trauma de tórax\n2. Trauma de cabeça\n3. Trauma de extremidades\n4. Trauma abdominal")
            escolha = input("Selecione o subgrupo (1-4): ")
            if escolha == '1':
                if input("Dor intensa + dificuldade respiratória súbita? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Trauma', 'Possível pneumotórax', ['Radiografia de tórax PA e perfil']))
            elif escolha == '2':
                if input("Perda transitória de consciência sem déficit focal? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Trauma', 'Possível TCE leve', ['TC de crânio se alteração neurológica']))
            elif escolha == '3':
                if input("Dor localizada + deformidade visível? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Trauma', 'Possível fratura de fêmur', ['Radiografia de quadril/fêmur']))
            elif escolha == '4':
                if input("Dor abdominal difusa + sinais de peritonite? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Trauma', 'Possível hemoperitônio', ['Ultrassonografia FAST']))

        # Dermatológico
        elif tipo == TipoSintoma.DERMATOLOGICO:
            print("Categoria: Dermatológico")
            print("1. Lesão única\n2. Múltiplas lesões pustulosas\n3. Placas pruriginosas\n4. Urticária")
            escolha = input("Selecione o subgrupo (1-4): ")
            if escolha == '1':
                if input("Eritema quente, doloroso, com limite mal definido? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Dermatológico', 'Possível celulite', ['Cultura de pele']))
            elif escolha == '2':
                if input("Área bem delimitada após contato com agente químico? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Dermatológico', 'Possível dermatite de contato', ['Patch test']))
            elif escolha == '3':
                if input("Lesões prateadas em cotovelos/joelhos? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Dermatológico', 'Possível psoríase', ['Biópsia de pele']))
            elif escolha == '4':
                if input("Pápulas pruriginosas que somem em horas? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Dermatológico', 'Possível urticária', ['Teste de provocação']))

        # Outros
        elif tipo == TipoSintoma.OUTROS:
            print("Categoria: Outros")
            print("1. Neurológico\n2. Endócrino\n3. Psiquiátrico\n4. Febre sem foco")
            escolha = input("Selecione o subgrupo (1-4): ")
            if escolha == '1':
                if input("Déficit motor ou sensitivo focal súbito? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Neurológico', 'Possível AVC', ['TC de crânio urgente']))
            elif escolha == '2':
                if input("Melhora após glicose? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Endócrino', 'Possível hipoglicemia', ['Glicemia capilar e venosa']))
            elif escolha == '3':
                if input("Taquicardia e medo sem causa aparente? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Psiquiátrico', 'Possível episódio de pânico', ['Avaliação psiquiátrica']))
            elif escolha == '4':
                if input("Febre >38°C por >3 semanas? (S/N): ").strip().upper() == 'S':
                    sugestoes.append(Diagnostico('Outros', 'Febre de origem indeterminada', ['Hemoculturas', 'Marcadores inflamatórios', 'Hemograma']))

        # Imprime os diagnósticos sugeridos antes de qualquer outra ação
        if sugestoes:
            print("\n--- Diagnósticos sugeridos ---")
            for diag in sugestoes:
                print(str(diag))
        else:
            print("Nenhum diagnóstico sugerido.")

        # Pergunta ao médico sobre agendamento de exame
        if input("\nDeseja solicitar exame a um técnico? (S/N): ").strip().upper() == 'S':
            print("Solicitação enviada.")
            paciente.atualizar_historico("Solicitação de exame enviada ao técnico.")

        # Pergunta ao médico se deseja gerar receituário
        if input("Deseja gerar receituário? (S/N): ").strip().upper() == 'S':
            self.gerar_receituario(paciente)

        # Pergunta ao médico se deseja gerar declaração de comparecimento
        if input("Deseja gerar declaração de comparecimento? (S/N): ").strip().upper() == 'S':
            self.gerar_declaracao_comparecimento(paciente)

        return sugestoes


    def gerar_receituario(self, paciente: Paciente) -> None:
        """
        Loop para inserir medicamentos, gravar histórico e exportar receituário em TXT com cabeçalho.
        """
        prescricoes: List[tuple[str, str, str, str]] = []
        print("Iniciando prescrição. Digite 0 para finalizar.")
        while True:
            med = input("Nome da medicação (ou 0 para terminar): ").strip()
            if med == '0':
                break
            pos = input("Posologia [miligramas]: ")
            intervalo = input("intervalo das doses [horas]: ")
            periodo = input("Período de tratamento [dias]: ")
            prescricoes.append((med, pos, intervalo, periodo))
            paciente.atualizar_historico(
                f"Prescrição adicionada em {datetime.now().strftime('%Y-%m-%d %H:%M')}: {med}, {pos}, {intervalo}, {periodo}"
            )
        filename = f"receituario_{paciente.cpf}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Hospital da Escola de Engenharia da UFMG\nSistema MediClass\n")
            f.write(f"Prescrição gerada em {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"Paciente: {paciente.nome} (CPF: {paciente.cpf})\n")
            f.write(f"Médico: {self.nome} (CRM: {self.registro_profissional})\n\n")
            for med, pos, intervalo, periodo in prescricoes:
                f.write(f"- {med}: {pos}mg a cada {intervalo} horas, durante {periodo} dias;\n")
            f.write(f"{self.nome} - CRM {self.registro_profissional}\n")
        print(f"Receituário exportado para {filename}")

    def gerar_declaracao_comparecimento(self, paciente: Paciente) -> None:
        """
        Gera declaração de comparecimento em TXT com cabeçalho e texto detalhado.
        """
        data = datetime.now().strftime('%Y-%m-%d')
        hora = datetime.now().strftime('%H:%M')
        tipo = paciente.ultima_anamnese.tipo_sintoma.value if hasattr(paciente, 'ultima_anamnese') else 'não especificado'
        filename = f"declaracao_{paciente.cpf}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Hospital da Escola de Engenharia da UFMG\nSistema MediClass\n")
            f.write(f"Declaração gerada em {data} às {hora}\n\n")
            f.write(f"Eu, {self.nome}, CRM {self.registro_profissional}, atesto para os devidos fins que o paciente ")
            f.write(f"{paciente.nome}, CPF {paciente.cpf}, compareceu a consulta clínica no dia {data}, ")
            f.write(f"dando entrada no hospital às {hora}, apresentando quadro sintomático {tipo}.\n\n")
            f.write("Cordialmente,\n")
            f.write(f"{self.nome} - CRM {self.registro_profissional}\n")
        paciente.atualizar_historico(
            f"Declaração de comparecimento gerada em {data} às {hora}."
        )
        print(f"Declaração exportada para {filename}")


class Enfermeiro(Profissional):
    """
    Profissional com permissões de enfermeiro, responsável pela triagem.
    """
    def triagem(self, paciente: Paciente) -> None:
        prioridade = False
        # frequência cardíaca (40-200 bpm)
        while True:
            try:
                fc = int(input("frequência cardíaca (40-200 bpm): "))
                if 40 <= fc <= 200:
                    break
                print("Valor fora da faixa válida (40-200). Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        if fc < 70 or fc > 120:
            print("frequência cardíaca incomum! Ativando prioridade.")
            prioridade = True
        # Pressão arterial sistólica (70-250 mmHg)
        while True:
            try:
                ps = int(input("Pressão arterial sistólica (70-250 mmHg): "))
                if 70 <= ps <= 250:
                    break
                print("Valor fora da faixa válida (70-250). Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        if ps < 90 or ps > 140:
            print("Pressão sistólica incomum! Ativando prioridade.")
            prioridade = True
        # Pressão arterial diastólica (40-150 mmHg)
        while True:
            try:
                pd = int(input("Pressão arterial diastólica (40-150 mmHg): "))
                if 40 <= pd <= 150:
                    break
                print("Valor fora da faixa válida (40-150). Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        if pd < 60 or pd > 90:
            print("Pressão diastólica incomum! Ativando prioridade.")
            prioridade = True
        # Oximetria (85-100%)
        while True:
            try:
                ox = int(input("Oximetria de pulso (85-100%): "))
                if 85 <= ox <= 100:
                    break
                print("Valor fora da faixa válida (85-100). Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        if ox < 95:
            print("Oximetria incomum! Ativando prioridade.")
            prioridade = True
        # Tipo de sintoma
        tipos = list(TipoSintoma)
        print("Selecione o tipo de sintoma:")
        for i, t in enumerate(tipos, 1):
            print(f"{i}. {t.value}")
        while True:
            try:
                choice = int(input("Opção: "))
                if 1 <= choice <= len(tipos):
                    tipo = tipos[choice-1]
                    break
                print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
       
        # Perguntas de anamnese (sim/não) específicas por tipo de sintoma
        if tipo == TipoSintoma.GASTROINTESTINAL:
            perguntas = [
                "náuseas ou vômitos",
                "diarreia",
                "constipação",
                "dor abdominal",
                "perda de peso inexplicada",
                "febre"
            ]  # Common GI topics: nausea/vomiting, diarrhea, constipation, pain; alarm signs: weight loss, fever :contentReference[oaicite:0]{index=0}
        elif tipo == TipoSintoma.RESPIRATORIO:
            perguntas = [
                "tosse",
                "dispneia",
                "expectoração",
                "hemoptise",
                "dor torácica",
                "febre"
            ]  # Ask about cough character, sputum, hemoptysis, dyspnea, chest pain, fever :contentReference[oaicite:1]{index=1}
        elif tipo == TipoSintoma.CARDIOVASCULAR:
            perguntas = [
                "dor torácica opressiva",
                "palpitações",
                "tontura ou desmaio",
                "edema de membros inferiores"
            ]  # Chest pain, palpitations, syncope/dizziness, peripheral edema :contentReference[oaicite:2]{index=2}
        elif tipo == TipoSintoma.TRAUMA:
            perguntas = [
                "perda de consciência",
                "sangramento ativo",
                "deformidade visível",
                "incapacidade de mover a área afetada"
            ]  # Mechanism, LOC, bleeding, deformity, functional loss :contentReference[oaicite:3]{index=3}
        elif tipo == TipoSintoma.DERMATOLOGICO:
            perguntas = [
                "lesão cutânea",
                "prurido",
                "dor na pele",
                "febre"
            ]  # Rash location/appearance, itch, pain, fever :contentReference[oaicite:4]{index=4}
        else:  # OUTROS
            perguntas = [
                "déficit motor ou sensitivo",
                "melhora após ingestão de glicose",
                "taquicardia e ansiedade",
                "febre sem foco >3 semanas"
            ]  # Neurológico, endocrino, psiquiátrico e febre de origem indeterminada
        respostas: dict[str, bool] = {}
        for p in perguntas:
            while True:
                resp = input(f"{p.capitalize()} (S/N): ").strip().upper()
                if resp in ('S', 'N'):
                    respostas[p] = (resp == 'S')
                    break
                print("Resposta inválida. Digite S ou N.")
        # Cria objeto Anamnese e atualiza histórico
        anamnese = Anamnese(fc, f"{ps}/{pd}", ox, respostas, tipo)
        paciente.atualizar_historico(f"Triagem: {anamnese.to_dict()}")
        if prioridade:
            paciente.prioritario = True
            paciente.atualizar_historico("FLAG: Prioridade ativada devido a valores incomuns.")
        # Armazena última anamnese no paciente
        paciente.ultima_anamnese = anamnese

class ExamType(Enum):
    ULTRASSON_ABDOMINAL = 'Ultrassonografia abdominal'
    HEMOGRAMA = 'Hemograma'
    COPROCULTURA = 'Coprocultura'
    RADIOGRAFIA_ABDOME = 'Radiografia de abdome sem preparo'
    RADIOGRAFIA_TORAX = 'Radiografia de tórax'
    ULTRASSON_PLEURAL = 'Ultrassonografia pleural'
    ECG = 'ECG'
    MARCADORES_C = 'Marcadores cardíacos'
    TESTE_ERGOMETRICO = 'Teste ergométrico'
    PERFUSAO = 'Perfusão'
    BNP = 'BNP'
    ECOCARDIOGRAMA = 'Ecocardiograma'
    RADIOGRAFIA_QUADRIL = 'Radiografia de quadril/fêmur'
    ULTRASSON_FAST = 'Ultrassonografia FAST'
    CULTURA_PELE = 'Cultura de pele'
    PATCH_TEST = 'Patch test'
    BIOPSIA_PELE = 'Biópsia de pele'
    TESTE_PROVOCACAO = 'Teste de provocação'
    TC_CRANIO = 'TC de crânio urgente'
    GLICEMIA = 'Glicemia capilar e venosa'
    HEMOCULTURAS = 'Hemoculturas'
    MARCADORES_INFLAMATORIOS = 'Marcadores inflamatórios'
    AVALIACAO_PSIQUIATRICA = 'Avaliação psiquiátrica'

class Tecnico(Profissional):
    """
    Profissional com permissões de técnico, responsável por adicionar exames.
    """
    def adicionar_exame_sistema(self, paciente: Paciente) -> None:
        """
        Permite ao técnico selecionar um tipo de exame pré-definido e registrar seu resultado.
        """
        print("Selecione o tipo de exame a adicionar:")
        tipos = list(ExamType)
        for idx, exame in enumerate(tipos, 1):
            print(f"{idx}. {exame.value}")
        while True:
            try:
                escolha = int(input("Opção (número): "))
                if 1 <= escolha <= len(tipos):
                    exame = tipos[escolha-1].value
                    break
                print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        resultado = input("Resultado do exame: ")
        paciente.adicionar_exame(exame, resultado)
        print(f"Exame '{exame}' com resultado '{resultado}' adicionado ao histórico.")
