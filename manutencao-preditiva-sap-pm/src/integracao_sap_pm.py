"""
Simulação de integração com SAP PM.
Cria payloads típicos de Notificação (QMEL) e Ordem (AUFK) e "envia" (mock).
"""
from datetime import datetime
from typing import Dict

def montar_payload_notificacao(equipment_id: str, descricao: str, prioridade: str="Média", reporter: str="IA") -> Dict:
    return {
        "tipo": "NOTIFICACAO",
        "equipamento": equipment_id,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_hora": datetime.now().isoformat(timespec="seconds"),
        "reporter": reporter
    }

def montar_payload_ordem(equipment_id: str, atividade: str, centro_trabalho: str="MANU-01", prioridade: str="Média") -> Dict:
    return {
        "tipo": "ORDEM",
        "equipamento": equipment_id,
        "atividade": atividade,
        "centro_trabalho": centro_trabalho,
        "prioridade": prioridade,
        "data_hora": datetime.now().isoformat(timespec="seconds")
    }

def enviar_mock(payload: Dict) -> None:
    # Aqui você substituiria por chamada real (requests para OData/REST ou BAPI)
    print("[SAP PM MOCK] Enviado payload:", payload)

if __name__ == "__main__":
    # Exemplo de uso
    notif = montar_payload_notificacao("EQT-007", "Vibração acima do limite. Probabilidade de falha > 0.7", "Alta")
    enviar_mock(notif)
    ordem = montar_payload_ordem("EQT-007", "Inspecionar rolamentos e reapertar acoplamentos", "MANU-01", "Alta")
    enviar_mock(ordem)