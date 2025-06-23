"""
MEDICLASS: Sistema de Prontuário Eletrônico e Apoio à Decisão Clínica
Parte do Trabalho Prático de ELE078

Arquivo: diagnostico.py
Autor: Matheus Marcondes <matheusmarcondes@ufmg.br>
Data de criação: 2025-06-21
Descrição:
    Módulo responsável pela classe Diagnostico,
    encapsulando informações de sugestão clínica.
Repositório: 
Licença: MIT License
Dependências:
    typing
"""

from typing import List

class Diagnostico:
    """
    Representa um diagnóstico sugerido pelo sistema.
    """
    def __init__(
        self,
        categoria: str,
        descricao: str,
        exames_sugeridos: List[str]
    ):
        self.categoria: str = categoria
        self.descricao: str = descricao
        self.exames_sugeridos: List[str] = exames_sugeridos

    def __str__(self) -> str:
        exames = ', '.join(self.exames_sugeridos)
        return f"{self.categoria}: {self.descricao} (Exames sugeridos: {exames})"