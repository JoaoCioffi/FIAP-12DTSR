from tqdm import tqdm
import numpy as np
import time

def awaitsService(start=0,stop=15,step=0.5):
    """
    Função criada para aguardar a estabilização dos serviços rodando na docker. Verificou-se que mesmo com os logs do 
    docker-compose exibindo o status de 'running' individualmente para cada container, ainda sim não foi possível estabelecer
    conexão direta sem aguardar alguns segundos para isso. Portanto, esta função visa colocar esse 'gap' ao usuário para que
    os seviços estejam disponíveis e que o script principal possa executar o ETL sem erros relacionados à indisponibilidade.
    """
    print("\n[INFO] Aguardando porta e estabilização do container...")
    for _ in tqdm(np.arange(start=start,stop=stop,step=step),desc="Running",colour='green'):
        time.sleep(1)