"""
MEDICLASS: Sistema de Prontuário Eletrônico e Apoio à Decisão Clínica
Parte do Trabalho Prático de ELE078

Arquivo: main.py
Autor: Matheus Marcondes <matheusmarcondes@ufmg.br>
Data de criação: 2025-06-21
Descrição:
    Ponto de entrada para execução e testes de integração do sistema Mediclass.
    Gerencia persistência de usuários e pacientes em JSON e invoca o CLI.
Repositório: 
Licença: MIT License
Dependências:
    json, sistema, paciente
"""

import json
from datetime import date

from sistema import SistemaMediclass
from profissionais import Medico, Enfermeiro, Tecnico
from paciente import Paciente

DATA_FILE = 'mediclass_data.json'


def load_data() -> dict:
    """
    Carrega dados de usuários e pacientes a partir do arquivo JSON.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data: dict) -> None:
    """
    Salva dados de usuários e pacientes no arquivo JSON.
    """
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main() -> None:
    sistema = SistemaMediclass()

    # Carregar persistência
    raw = load_data()

    # Reconstruir pacientes do JSON
    for pdata in raw.get('pacientes', []):
        try:
            data_nasc = date.fromisoformat(pdata['data_nascimento'])
        except Exception:
            continue
        paciente = Paciente(
            nome=pdata['nome'],
            cpf=pdata['cpf'],
            contato=pdata['contato'],
            convenio=pdata['convenio'],
            data_nascimento=data_nasc,
            leito=pdata['leito'],
            enfermeiro_triagem=pdata.get('enfermeiro_triagem', '')
        )
        paciente.prioritario = pdata.get('prioritario', False)
        sistema.pacientes[paciente.cpf] = paciente

    # TODO: Reconstruir usuários a partir de raw.get('usuarios', [])
    # Para enquanto testes iniciais, registramos usuários padrão
    sistema.registrar_usuario(Medico("Dr. Teste", "CRM123", "med", "senha"))
    sistema.registrar_usuario(Enfermeiro("Enf. Teste", "COREN456", "enf", "senha"))
    sistema.registrar_usuario(Tecnico("Tec. Teste", "CRTR789", "tec", "senha"))

    # Executar fluxo principal (CLI interativo)
    sistema.executar()

    # Persistir estado atual
    data = {
        'usuarios': [
            {
                'tipo': u.__class__.__name__,
                'nome': u.nome,
                'registro_profissional': u.registro_profissional,
                'login': u.login,
                '_senha_hash': getattr(u, '_senha_hash', '')
            }
            for u in sistema.usuarios.values()
        ],
        'pacientes': [
            {
                'nome': p.nome,
                'cpf': p.cpf,
                'contato': p.contato,
                'convenio': p.convenio,
                'data_nascimento': p.data_nascimento.isoformat(),
                'leito': p.leito,
                'enfermeiro_triagem': p.enfermeiro_triagem,
                'prioritario': p.prioritario
            }
            for p in sistema.pacientes.values()
        ]
    }
    save_data(data)


if __name__ == "__main__":
    main()
