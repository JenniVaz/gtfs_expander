# Importando as bibliotecas necessárias
from copy import copy # Importa a função 'copy' para duplicar objetos como dicionários
import math # Importa a biblioteca math para trabalhar com números e verificar se é realmente um número ou se o valor é não númerico(Nan)


# Bibliotecas externas
from networkx.utils import pairwise
import numpy as np
import pandas as pd #biblioteca usada para manipulação de tabelas (DataFrames)
import partridge as ptg #biblioteca usada para ler e escrever arquivos GTFS


# Função para converter segundos no formato HH:MM:SS (padrão GTFS)
def seconds_to_gtfs_time(total_seconds):
    if math.isnan(total_seconds): # Verifica se o valor é NaN 
        return total_seconds  # TODO: What to do here? # Se o valor for NaN (não numérico), retorna o mesmo valor
     # Calculando minutos e segundos
    minutes, seconds = divmod(total_seconds, 60) # Divide segundos em minutos e segundos
    hours, minutes = divmod(minutes, 60)  # Divide minutos em horas e minutos
    # Formata o tempo para o formato HH:MM:SS
    time = list(map(lambda x: str(x).rjust(2, '0'), [int(hours), int(minutes), int(seconds)])) # Formatação com zeros à esquerda
    return f'{time[0]}:{time[1]}:{time[2]}'  # Retorna no formato HH:MM:SS

    # Caminho do arquivo de entrada (GTFS original - em formato .zip)
    inpath = "dados/entrada.zip"
    
    # Carrega o feed GTFS (todos os arquivos .txt dentro do zip) usando a biblioteca 'partridge'
    feed = ptg.load_feed(inpath)

    # Cria um dicionário para armazenar os detalhes de cada viagem (trip_id)
    trips_by_id = {}


for _, trip in feed.trips.iterrows(): # Percorre cada linha do  DataFrame feed.trips, que representa uma viagem do GTFS. Cada linha representa uma viagem), e o loop vai passar por todas essas viagens no arquivo GTFS retornando Índice(posição) e trip(Dados)
    trips_by_id[trip.trip_id] = dict(trip)  # Armazena os dados da viagem como dicionário
    #Exemplo esperado:{1: {'trip_id': 1, 'route_id': 'A', 'trip_headsign': 'Central', 'arrival_time': '08:00'}, 2: {'trip_id': 2, 'route_id': 'B', 'trip_headsign': 'Downtown', 'arrival_time': '08:15'}}


    #Armazena os dados da viagem como dicionário
    trip_patterns = {}

    # Agrupando os tempos de parada por viagem e criando os padrões
for trip_id, stop_times in feed.stop_times.sort_values("stop_sequence").groupby("trip_id"):
    stops = tuple(stop_times.stop_id) # Obtendo os IDs das paradas e gerando uma Lista ordenada 
    mintime = stop_times.arrival_time.min()   # Tempo de chegada minimo
    times = tuple(t - mintime for t in stop_times.arrival_time)  # Calculando os tempos relativos desde a primeira parada
    trip_patterns[trip_id] = (stops, times) # Armazenando o padrão de viagem no dicionário


    # Lista para armazenar as viagens com frequência encontradas em frequencies.txt
    freq_trips = []
for _, freq in feed.frequencies.iterrows():
    window_start = int(freq.start_time) # Pega o início da janela de operação
    window_end = int(freq.end_time) # Pega o Fim da janela de operação
    # Cria novas viagens a cada intervalo (headway_secs)
    for start in range(window_start, window_end, freq.headway_secs): # Gera horários com passo headway
        freq_trips.append({
            "trip_id": freq.trip_id,  # ID da viagem de referência
            "start": start, # Novo horário de partida gerado
        })

# Cria as novas viagens e seus tempos de parada e armazena em forma de lista
new_trips = []
new_stop_times = []
# Para cada nova viagem gerada por frequência vamos copiar a viagem original e alterar o trip_id para o novo identificador
for i, ftrip in enumerate(freq_trips, start=1):
    new_trips.append(copy(trips_by_id[ftrip["trip_id"]]))  #Copia os dados da viagem original
    new_trips[-1]["trip_id"] = i # override trip_id # Sobrescreva o trip_id para ser único

    
    # Obtendo os padrões de paradas e tempos de viagem originais
    stops, times = trip_patterns[ftrip["trip_id"]]  # Recupera padrão de parada/tempo da viagem original

    # Criando novos tempos de parada para cada viagem frequente
    for j in range(len(stops)):
        t = seconds_to_gtfs_time(times[j] + ftrip["start"]) # Converte para horário real da parada
        new_stop_times.append({ 
            "trip_id": i,
            "stop_id": stops[j],
            "arrival_time": t,
            "departure_time": t,
            "stop_sequence": j + 1, 
        }) # Sequência da parada

# Cria um DataFrame para as novas viagens e novos tempos de parada
trips_df = pd.DataFrame(new_trips) #novas_viagens
stop_times_df = pd.DataFrame(new_stop_times) #novos_tempos_de_parada
empty_frequencies_df = ptg.utilities.empty_df()

# Recarrega os dados brutos do feed para sobrescrever os arquivos
new_feed = ptg.load_raw_feed(inpath)  
new_feed.set("trips.txt", trips_df) # Substitui o arquivo trips.txt
new_feed.set("stop_times.txt", stop_times_df) # Substitui o arquivo stop_times.txt
new_feed.set("frequencies.txt", empty_frequencies_df) # we don't want frequencies.txt # # Remove o arquivo Frequencies


# Escreve o novo feed GTFS com viagens geradas explicitamente
ptg.writers.write_feed_dangerously(new_feed, "dados/saida.zip")

# Caminho do arquivo de saída gerado
"dados/saida.zip'