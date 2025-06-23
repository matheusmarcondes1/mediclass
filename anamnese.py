"""
MEDICLASS: Sistema de Prontuário Eletrônico e Apoio À Decisão Clínica
Parte do Trabalho Prático de ELE078

Arquivo: anamnese.py
Autor: Matheus Marcondes <matheusmarcondes@ufmg.br>
Data de criação: 2025-06-21
Descrição:
    Módulo responsável pela classe Anamnese, modelando as perguntas e respostas de triagem.
Repositório: 
Licença: MIT License
Dependências:
    enum, datetime
"""

from enum import Enum
from datetime import datetime

class TipoSintoma(Enum):
    GASTROINTESTINAL = 'gastrointestinal'
    RESPIRATORIO = 'respiratório'
    CARDIOVASCULAR = 'cardiovascular'
    TRAUMA = 'trauma'
    DERMATOLOGICO = 'dermatológico'
    OUTROS = 'outros'

class Anamnese:
    """
    Representa as respostas da triagem de um paciente.
    Atributos:
        frequencia_cardiaca: int
        pressao_arterial: str
        saturacao_o2: float
        respostas_sim_nao: dict[str, bool]
        tipo_sintoma: TipoSintoma
        detalhes_sintoma: str | None
        timestamp: datetime
    """
    def __init__(
        self,
        frequencia_cardiaca: int,
        pressao_arterial: str,
        saturacao_o2: float,
        respostas_sim_nao: dict[str, bool],
        tipo_sintoma: TipoSintoma,
        detalhes_sintoma: str = None
    ):
        self.frequencia_cardiaca = frequencia_cardiaca
        self.pressao_arterial = pressao_arterial
        self.saturacao_o2 = saturacao_o2
        self.respostas_sim_nao = respostas_sim_nao
        self.tipo_sintoma = tipo_sintoma
        self.detalhes_sintoma = detalhes_sintoma
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        """
        Retorna um dicionário com todos os dados da anamnese.
        """
        return {
            'frequencia_cardiaca': self.frequencia_cardiaca,
            'pressao_arterial': self.pressao_arterial,
            'saturacao_o2': self.saturacao_o2,
            'respostas_sim_nao': self.respostas_sim_nao,
            'tipo_sintoma': self.tipo_sintoma.value,
            'detalhes_sintoma': self.detalhes_sintoma,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
