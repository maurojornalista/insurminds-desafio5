"""Agente de comunicação com OpenAI opcional e fallback seguro."""
from __future__ import annotations

from typing import Any

from src.config import OPENAI_API_KEY, OPENAI_MODEL


class MessageAgent:
    """Gera mensagens personalizadas sem exigir serviço pago para funcionar."""

    def generate(self, policyholder: dict[str, Any], risk: dict[str, Any], city: str) -> dict[str, str]:
        fallback = self._fallback(policyholder, risk, city)
        if not OPENAI_API_KEY:
            return {"message": fallback, "source": "Fallback local"}
        try:
            from openai import OpenAI

            prompt = (
                "Escreva uma mensagem preventiva curta, cordial e personalizada em português do Brasil. "
                f"Segurado: {policyholder['nome']}; cidade: {city}; apólice: {policyholder['tipo_apolice']}; "
                f"evento: {risk['event_type']}; gravidade: {risk['severity']}. Inclua duas ou três orientações "
                "práticas adequadas à apólice. Não prometa cobertura nem solicite dados pessoais. Termine orientando "
                "a acompanhar alertas oficiais e procurar os canais da seguradora se necessário."
            )
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(model=OPENAI_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.4, max_tokens=180)
            content = response.choices[0].message.content
            if content:
                return {"message": content.strip(), "source": "OpenAI"}
        except Exception:
            pass  # Falhas de credencial, rede ou serviço não interrompem o MVP.
        return {"message": fallback, "source": "Fallback local"}

    @staticmethod
    def _fallback(policyholder: dict[str, Any], risk: dict[str, Any], city: str) -> str:
        policy_type = str(policyholder["tipo_apolice"])
        event = str(risk["event_type"])
        event_key = event.casefold()
        if "alagamento" in event_key or "chuva intensa" in event_key:
            recommendations = (
                "Evite vias com histórico de alagamento, não atravesse áreas com água acumulada e, se possível, mantenha o veículo em local elevado."
                if policy_type == "Auto"
                else "Mantenha ralos e calhas desobstruídos, retire objetos de áreas externas e proteja equipamentos elétricos em locais sujeitos à entrada de água."
            )
        elif "vendaval" in event_key or "vento forte" in event_key:
            recommendations = (
                "Estacione longe de árvores, postes e estruturas instáveis, evite deslocamentos desnecessários e reduza a velocidade caso precise dirigir."
                if policy_type == "Auto"
                else "Recolha ou fixe objetos externos, mantenha portas e janelas bem fechadas e evite permanecer próximo a árvores ou estruturas instáveis."
            )
        else:  # Tempestade e tempestade com granizo.
            recommendations = (
                "Se possível, mantenha o veículo em local coberto, evite dirigir durante a tempestade e não estacione sob árvores ou estruturas frágeis."
                if policy_type == "Auto"
                else "Feche portas e janelas, retire equipamentos elétricos de tomadas quando seguro fazê-lo e mantenha áreas externas livres de objetos soltos."
            )
        return (
            f"Olá, {policyholder['nome']}. Identificamos {event.lower()} em {city}. "
            f"Para sua proteção no seguro {policy_type}, recomendamos: {recommendations} "
            "Acompanhe os alertas oficiais e procure os canais da seguradora se necessário."
        )
