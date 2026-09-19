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
                "Escreva uma mensagem preventiva curta, cordial e clara em português do Brasil. "
                f"Segurado: {policyholder['nome']}; cidade: {city}; apólice: {policyholder['tipo_apolice']}; "
                f"evento: {risk['event_type']}; gravidade: {risk['severity']}. "
                "Não prometa cobertura nem solicite dados pessoais."
            )
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(model=OPENAI_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.4, max_tokens=140)
            content = response.choices[0].message.content
            if content:
                return {"message": content.strip(), "source": "OpenAI"}
        except Exception:
            pass  # Falhas de credencial, rede ou serviço não interrompem o MVP.
        return {"message": fallback, "source": "Fallback local"}

    @staticmethod
    def _fallback(policyholder: dict[str, Any], risk: dict[str, Any], city: str) -> str:
        return (
            f"Olá, {policyholder['nome']}. Identificamos {risk['event_type'].lower()} em {city}. "
            f"Como você possui seguro {policyholder['tipo_apolice']}, recomendamos reforçar medidas de prevenção "
            "e acompanhar os alertas oficiais. Em caso de necessidade, consulte os canais da sua seguradora."
        )
