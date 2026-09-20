# Relatório Técnico - InsurMinds Desafio 5

## Identificação

**Projeto:** InsurMinds - Comunicação Climática Proativa  
**Curso:** InsurMinds - IA Aplicada a Seguros (I2A2)  
**Desafio:** Desafio 5  
**Responsável pela entrega:** Mauro de Oliveira  
**Repositório:** https://github.com/maurojornalista/insurminds-desafio5  
**Aplicação publicada:** https://insurminds-desafio-5.streamlit.app

## 1. Objetivo

Construir um MVP de comunicação proativa com segurados diante de eventos climáticos, demonstrando uma arquitetura multiagente simples, testável e adequada ao contexto acadêmico.

A proposta é antecipar situações de risco, relacionar o evento meteorológico à localidade e ao tipo de apólice e preparar comunicações preventivas específicas para os segurados potencialmente afetados.

## 2. Problema

Chuvas intensas, vendavais e tempestades podem afetar veículos e imóveis segurados. Em um modelo puramente reativo, a comunicação com o segurado tende a acontecer somente após a ocorrência do evento. O MVP propõe uma abordagem preventiva: consultar dados meteorológicos, classificar o risco, identificar os segurados relevantes e gerar uma orientação adequada ao contexto.

## 3. Solução proposta

A aplicação foi desenvolvida em Python e Streamlit. O usuário seleciona uma cidade e escolhe entre:

- **Clima real**, obtido pela API pública Open-Meteo; ou
- **Cenário de demonstração**, com dados explicitamente simulados para fins acadêmicos.

O fluxo é coordenado pelo `CommunicationOrchestrator`, que executa quatro agentes especializados:

`WeatherAgent -> RiskAgent -> PolicyAgent -> MessageAgent`

O resultado apresenta dados meteorológicos, previsão horária, classificação do risco, segurados selecionados e mensagens preventivas.

## 4. Arquitetura multiagente

A arquitetura utiliza separação de responsabilidades:

1. **WeatherAgent - Coleta Meteorológica**  
   Consulta a API Open-Meteo com latitude e longitude. Retorna temperatura, precipitação, chuva, velocidade do vento e código meteorológico WMO. Também normaliza uma previsão horária das próximas 12 horas. Falhas de rede são tratadas sem interromper a interface.

2. **RiskAgent - Classificação de Risco**  
   Aplica regras explícitas aos dados meteorológicos e retorna tipo de evento, gravidade, detalhes e tipos de apólice potencialmente afetados.

3. **PolicyAgent - Seleção de Segurados**  
   Carrega a base fictícia `data/policyholders.csv`, filtra pela cidade e cruza o tipo de apólice com o risco identificado.

4. **MessageAgent - Geração de Comunicação**  
   Produz uma mensagem preventiva por segurado. Quando `OPENAI_API_KEY` está configurada, pode usar OpenAI; sem chave ou em caso de falha, utiliza fallback local, mantendo o MVP funcional.

O `CommunicationOrchestrator` reduz o acoplamento entre os agentes e facilita testes isolados e manutenção.

## 5. Integração com API Open-Meteo

No modo **Clima real**, o WeatherAgent realiza uma requisição HTTP para o endpoint:

`https://api.open-meteo.com/v1/forecast`

A consulta solicita dados atuais:

- `temperature_2m`
- `precipitation`
- `rain`
- `wind_speed_10m`
- `weather_code`

Também solicita dados horários:

- `precipitation`
- `rain`
- `wind_speed_10m`
- `weather_code`

A interface apresenta os dados atuais e um gráfico compacto com a previsão de precipitação das próximas 12 horas. O bloco **Dados brutos da API** mostra a fonte, horário da consulta, coordenadas e um resumo da resposta recebida.

A Open-Meteo foi escolhida por ser pública e não exigir chave de API neste uso.

## 6. Regras de negócio

As regras implementadas no MVP são didáticas e explícitas:

- precipitação ou chuva maior ou igual a 20 mm: **chuva intensa / risco de alagamento**, gravidade alta;
- vento maior ou igual a 60 km/h: **vento forte / risco de vendaval**, gravidade média;
- código WMO 95, 96 ou 99: **tempestade**;
- códigos 96 e 99 são apresentados como **tempestade com granizo**, gravidade alta;
- eventos do MVP podem afetar seguros **Auto** e **Residencial**;
- tempestade recebe prioridade quando representa o cenário mais severo.

Esses limiares servem ao protótipo acadêmico e não substituem critérios oficiais, atuariais ou operacionais de seguradoras.

## 7. Base fictícia de segurados

A base `data/policyholders.csv` contém oito segurados fictícios distribuídos em quatro cidades:

- São Paulo;
- Rio de Janeiro;
- Curitiba;
- Porto Alegre.

Há registros de seguros **Auto** e **Residencial**. Os nomes, contatos e bens segurados são fictícios e existem apenas para demonstrar o funcionamento do fluxo.

## 8. Cenários de demonstração

Além do clima real, a aplicação oferece três cenários repetíveis:

- chuva intensa;
- vento forte;
- tempestade/granizo.

A interface identifica claramente esses dados como simulados. Para melhorar a demonstração visual, cada cenário possui uma **evolução simulada nas próximas 12 horas**, sem mistura com dados reais da Open-Meteo.

Exemplos:

- chuva intensa: crescimento da precipitação, pico e redução;
- vento forte: aumento da velocidade do vento, pico e redução;
- tempestade/granizo: janela concentrada de maior severidade.

## 9. Geração de comunicação

O MessageAgent adapta a mensagem ao tipo de evento e à apólice.

Exemplo - **Seguro Auto + vendaval**:

> Olá, Ana Souza. Identificamos vento forte / risco de vendaval em São Paulo. Para sua proteção no seguro Auto, recomendamos: estacione longe de árvores, postes e estruturas instáveis, evite deslocamentos desnecessários e reduza a velocidade caso precise dirigir. Acompanhe os alertas oficiais e procure os canais da seguradora se necessário.

Exemplo - **Seguro Residencial + vendaval**:

> Olá, Bruno Lima. Identificamos vento forte / risco de vendaval em São Paulo. Para sua proteção no seguro Residencial, recomendamos: recolha ou fixe objetos externos, mantenha portas e janelas bem fechadas e evite permanecer próximo a árvores ou estruturas instáveis. Acompanhe os alertas oficiais e procure os canais da seguradora se necessário.

O fallback local permite demonstrar a aplicação sem serviço pago. A integração com OpenAI é opcional e utiliza variável de ambiente, sem registrar chaves no repositório.

## 10. Interface

A interface Streamlit foi organizada para evidenciar o fluxo multiagente:

- seleção da cidade;
- seleção da fonte dos dados;
- cards meteorológicos;
- previsão real ou evolução simulada de 12 horas;
- status visual do risco;
- tabela de segurados selecionados;
- cards de comunicação preventiva;
- expander com dados brutos da API.

A aplicação está publicada em:

**https://insurminds-desafio-5.streamlit.app**

## 11. Testes e validação

A suíte automatizada cobre:

- classificação de risco;
- ausência de risco;
- seleção de segurados por cidade e apólice;
- execução do orquestrador;
- personalização do MessageAgent;
- parsing da previsão horária do WeatherAgent.

Na validação final, foram executados **7 testes**, todos aprovados:

`7 passed`

Também foram realizados testes manuais no Streamlit com clima real e com os cenários simulados.

## 12. Tecnologias utilizadas

- Python 3;
- Streamlit;
- Requests;
- Pandas;
- python-dotenv;
- Open-Meteo API;
- OpenAI API opcional;
- Pytest;
- GitHub;
- Streamlit Community Cloud.

Não foi utilizado LangChain, pois a arquitetura proposta pôde ser implementada de forma mais simples e direta para o escopo acadêmico.

## 13. Segurança e limitações

- nenhuma chave real de API é armazenada no GitHub;
- o arquivo `.env` está ignorado pelo Git;
- a base de segurados é fictícia;
- o cruzamento geográfico é simplificado por cidade;
- as regras de risco são didáticas;
- o sistema não substitui alertas oficiais, análise atuarial, regulação ou decisão operacional de uma seguradora;
- o fallback local é utilizado quando não há chave de IA configurada.

## 14. Conclusão

O MVP demonstra um fluxo completo de comunicação climática proativa: coleta de dados externos, classificação de risco, identificação de segurados e geração de mensagens preventivas personalizadas.

A arquitetura multiagente tornou o sistema modular e explicável. A integração com a Open-Meteo permite trabalhar com dados reais e previsão horária, enquanto os cenários simulados garantem uma demonstração repetível mesmo quando não há evento severo no momento da apresentação.

Como evolução futura, o projeto poderia integrar bases reais com controles de privacidade, geolocalização mais precisa, alertas oficiais, canais de notificação e validação atuarial das regras.

## 15. Links de entrega

**GitHub:** https://github.com/maurojornalista/insurminds-desafio5  
**Aplicação:** https://insurminds-desafio-5.streamlit.app  
**Licença:** MIT
