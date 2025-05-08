Documentação Técnica – Expansão de Viagens Frequenciais (GTFS)

📄 Objetivo

Este script tem como objetivo converter viagens definidas por frequências (`frequencies.txt`) em viagens explícitas no formato tradicional do GTFS, populando os arquivos `trips.txt` e `stop_times.txt` com todas as ocorrências dessas viagens ao longo do tempo de operação.

Essa transformação é útil para sistemas que não suportam o modelo de frequências do GTFS e precisam de todos os horários gerados previamente.

🚌 🧒 Explicação simples
Imagine que temos um ônibus escolar e um mapa com os horários e paradas dele. Esse código faz o seguinte:

📦 Abre o pacote com os horários do ônibus.
--- Imagina que tem uma pasta com informações dos ônibus e suas paradas. A gente abre essa pasta pra olhar tudo.


🧠 Lembra como é cada viagem (paradas e horários).
-- Cada ônibus tem uma rota. É como se anotassemos cada informação dessa rota num caderno. Além disso 
-- Cada ônibus tem uma rota. É como se anotassemos cada informação dessa rota num caderno. Além disso cada Onibus para em vários lugares e nós tambem anotamos quais lugares e em que ordem eles passam nesse ponto.


🕒 Para ônibus que funcionam de tempo em tempo (ex: a cada 15 minutos), ele cria várias viagens iguais, só mudando a hora que começam.
-- Tem ônibus que não diz a hora certa que vai sair, só diz: “Esse ônibus passa de 8h até 10h, a cada 10 minutos.”
Então a gente faz isso: Cria horários padrões de saída. 


📜 Criar uma nova lista com todas essas viagens.
--Para cada um desses horários, a gente faz um "novo ônibus" igual ao antigo, mas com o horário certo de saída. E calcula quando ele vai chegar e sair em sair em cada ponto.


📁 Guarda essa nova lista em um novo arquivo com todos os horários já prontos, sem precisar de cálculo depois.
--Agora temos uma lista completa com todos os ônibus e horários, e guardamos isso numa nova caixa para usar depois.

📦 Bibliotecas utilizadas
`copy` - Usada para clonar dicionários de viagens (`trip`) sem afetar o original 
`math` - Usada para verificar se valores são `NaN` (não númerico) antes de fazer cálculos  
`numpy` - Usada para a manipulação de dados numéricos
`pandas` -  Usada para a criação e manipulação de DataFrames (estrutura de dados tabular)
`partridge` - Usada para a leitura, modificação e escrita de arquivos GTFS 


✅ Requisitos de execução
- Python 3.8+
- Instalar dependências: ```bash
pip install pandas numpy partridge
