# Relatório Técnico — InsurMinds Desafio 5

## Objetivo

Construir um MVP de comunicação proativa com segurados diante de eventos climáticos, demonstrando uma arquitetura multiagente simples, testável e adequada ao contexto acadêmico.

## Problema

Chuvas intensas, vendavais e tempestades podem afetar bens segurados. A comunicação preventiva ajuda o segurado a tomar precauções, mas precisa relacionar o evento, a localidade e a apólice de forma rápida.

## Solução proposta

O Streamlit recebe uma cidade e uma fonte de clima. O orquestrador executa, nessa ordem, `WeatherAgent`, `RiskAgent`, `PolicyAgent` e `MessageAgent`. O resultado mostra dados, classificação, segurados selecionados e comunicações preventivas.

## Arquitetura

O `CommunicationOrchestrator` reduz o acoplamento entre os agentes. Cada agente possui uma responsabilidade única e retorna estruturas simples, permitindo testes isolados.

## Os quatro agentes

1. **WeatherAgent:** consulta o endpoint de previsão da Open-Meteo com latitude e longitude. Retorna temperatura, precipitação, chuva, vento e código WMO atual. Uma falha de rede gera um resultado indisponível, sem exceção para a interface.
2. **RiskAgent:** aplica regras explícitas aos dados meteorológicos e retorna evento, gravidade, detalhes e apólices afetadas.
3. **PolicyAgent:** carrega a base CSV fictícia, filtra pela cidade e pelo tipo de apólice aplicável.
4. **MessageAgent:** cria uma mensagem por segurado. Se houver `OPENAI_API_KEY`, tenta a OpenAI; sem chave ou diante de erro, usa fallback local.

## API Open-Meteo

Foi escolhida por ser pública e não exigir chave neste uso. A consulta solicita os campos atuais `temperature_2m`, `precipitation`, `rain`, `wind_speed_10m` e `weather_code`, com vento em km/h.

## Regras de negócio

- Precipitação ou chuva maior ou igual a 20 mm: **chuva intensa / risco de alagamento**, gravidade alta.
- Vento maior ou igual a 60 km/h: **vento forte / risco de vendaval**, gravidade média.
- Código WMO 95, 96 ou 99: **tempestade**; 96 e 99 são apresentados como **tempestade com granizo**, gravidade alta.
- Os eventos deste MVP podem afetar seguros **Auto** e **Residencial**. Tempestade recebe prioridade por representar o cenário mais severo.

## Base fictícia

`data/policyholders.csv` contém oito segurados fictícios, dois em cada cidade: São Paulo, Rio de Janeiro, Curitiba e Porto Alegre. Há uma apólice Auto e uma Residencial por cidade. Os dados não representam pessoas reais.

## Uso de IA generativa

A IA é opcional. A chave é lida somente por variável de ambiente, nunca é registrada no código. O fallback local assegura funcionamento gratuito, previsível e demonstrável.

## Modo de demonstração

Há três cenários repetíveis: chuva intensa, vento forte e tempestade/granizo. A interface declara explicitamente: “Cenário simulado para fins acadêmicos e de demonstração.”

## Exemplos de mensagens

- “Olá, Ana Souza. Identificamos chuva intensa / risco de alagamento em São Paulo. Como você possui seguro Auto, recomendamos reforçar medidas de prevenção e acompanhar os alertas oficiais.”
- “Olá, Felipe Costa. Identificamos tempestade com granizo em Curitiba. Como você possui seguro Residencial, recomendamos reforçar medidas de prevenção e acompanhar os alertas oficiais.”

## Testes realizados

Os testes em `tests/` validam a regra de chuva intensa do RiskAgent, ausência de risco, cruzamento de cidade/apólice pelo PolicyAgent e a execução básica de ponta a ponta do orquestrador com cenário simulado.

## Conclusões

O MVP comprova o fluxo de comunicação proativa sem depender de chaves pagas. Para evolução futura, seria necessário integrar dados de apólices reais com controles de privacidade, geolocalização mais precisa, alertas oficiais e validação atuarial das regras.
