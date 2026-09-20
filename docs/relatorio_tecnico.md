# Relatório Técnico - InsurMinds Desafio 5

## Identificação

**Projeto:** InsurMinds - Comunicação Climática Proativa  
**Curso:** InsurMinds - IA Aplicada a Seguros (I2A2)  
**Desafio:** Desafio 5  
**Grupo:** Insight Builders  

**Integrantes:**  
Márcio de la Cruz Lui  
Mauro José de Oliveira  
Pedro Antonio Franceschini  

**Repositório:** https://github.com/maurojornalista/insurminds-desafio5  
**Aplicação publicada:** https://insurminds-desafio-5.streamlit.app

## 1. Objetivo

Construir um MVP de comunicação proativa com segurados diante de eventos climáticos, demonstrando uma arquitetura multiagente simples, testável e adequada ao contexto acadêmico.

A proposta é antecipar situações de risco, relacionar o evento meteorológico à localidade e ao tipo de apólice e preparar comunicações preventivas específicas para os segurados potencialmente afetados.

## 2. Problema

Chuvas intensas, vendavais e tempestades podem afetar veículos e imóveis segurados. Em um modelo puramente reativo, a comunicação com o segurado tende a acontecer somente após a ocorrência do evento. O MVP propõe uma abordagem preventiva: consultar dados meteorológicos, classificar o risco, identificar os segurados relevantes e gerar uma orientação adequada ao contexto.

## 3. Solução proposta

A aplicação foi desenvolvida em Python e Streamlit. O usuário seleciona uma cidade e escolhe entre clima real, obtido pela API pública Open-Meteo, ou cenário de demonstração, com dados explicitamente simulados para fins acadêmicos.

O fluxo é coordenado pelo `CommunicationOrchestrator`, que executa quatro agentes especializados:

`WeatherAgent -> RiskAgent -> PolicyAgent -> MessageAgent`

O resultado apresenta dados meteorológicos, previsão horária, classificação do risco, segurados selecionados e mensagens preventivas.

## 4. Arquitetura multiagente

1. **WeatherAgent - Coleta Meteorológica:** consulta a API Open-Meteo, retorna condições atuais e uma previsão horária das próximas 12 horas.
2. **RiskAgent - Classificação de Risco:** aplica regras explícitas e retorna evento, gravidade e apólices afetadas.
3. **PolicyAgent - Seleção de Segurados:** cruza cidade e tipo de apólice com a base fictícia.
4. **MessageAgent - Geração de Comunicação:** produz mensagem preventiva personalizada; pode usar OpenAI, com fallback local seguro.

O `CommunicationOrchestrator` coordena os quatro agentes.

## 5. Integração com API Open-Meteo

No modo **Clima real**, o WeatherAgent realiza uma requisição HTTP para:

`https://api.open-meteo.com/v1/forecast`

A consulta solicita `temperature_2m`, `precipitation`, `rain`, `wind_speed_10m` e `weather_code`, além de dados horários de precipitação, chuva, vento e código meteorológico.

A interface mostra os dados atuais, a previsão de precipitação das próximas 12 horas e um bloco com dados brutos resumidos da API.

## 6. Regras de negócio

- precipitação ou chuva >= 20 mm: **chuva intensa / risco de alagamento**, gravidade alta;
- vento >= 60 km/h: **vento forte / risco de vendaval**, gravidade média;
- código WMO 95, 96 ou 99: **tempestade**;
- códigos 96 e 99: **tempestade com granizo**, gravidade alta;
- eventos podem afetar apólices **Auto** e **Residencial**.

Os limiares são didáticos e não substituem critérios oficiais ou atuariais.

## 7. Base fictícia de segurados

A base `data/policyholders.csv` contém oito segurados fictícios, distribuídos entre São Paulo, Rio de Janeiro, Curitiba e Porto Alegre, com seguros Auto e Residencial.

## 8. Cenários de demonstração

Há três cenários repetíveis: chuva intensa, vento forte e tempestade/granizo. Cada um possui evolução simulada nas próximas 12 horas, sempre identificada como fictícia.

## 9. Geração de comunicação

As mensagens são específicas por tipo de apólice e evento. O fallback local garante funcionamento mesmo sem chave paga.

## 10. Interface

A interface Streamlit apresenta cards meteorológicos, previsão real ou simulada de 12 horas, status de risco, tabela de segurados, mensagens preventivas e dados brutos da API.

**Aplicação:** https://insurminds-desafio-5.streamlit.app

## 11. Testes e validação

A validação final executou **7 testes automatizados**, todos aprovados (`7 passed`), cobrindo RiskAgent, PolicyAgent, MessageAgent, WeatherAgent e o fluxo do orquestrador.

## 12. Tecnologias utilizadas

Python, Streamlit, Requests, Pandas, python-dotenv, Open-Meteo API, OpenAI API opcional, Pytest, GitHub e Streamlit Community Cloud.

## 13. Segurança e limitações

- nenhuma chave real é armazenada no GitHub;
- `.env` está ignorado;
- a base é fictícia;
- o cruzamento geográfico é simplificado por cidade;
- regras de risco são didáticas;
- o sistema não substitui alertas oficiais ou decisões operacionais de seguradoras.

## 14. Conclusão

O MVP demonstra um fluxo completo de comunicação climática proativa, com dados externos, classificação de risco, identificação de segurados e mensagens personalizadas.

## 15. Links de entrega

**GitHub:** https://github.com/maurojornalista/insurminds-desafio5  
**Aplicação:** https://insurminds-desafio-5.streamlit.app  
**Licença:** MIT
