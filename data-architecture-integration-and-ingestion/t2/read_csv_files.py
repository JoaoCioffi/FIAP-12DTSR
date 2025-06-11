from params import params
import pandas as pd
import json

filesPath,_=params()

def readFiles():
    print('\n','-='*32)
    print("\n⏳ Carregando a base de dados (.csv)...")

    """Carrega os arquivos num dataframe pandas e converte os DTypes"""
    df_clientes=pd.read_csv(filesPath["original_db"]["customers"]).astype({
        'cpf':'string',
        'nome':'string',
        'endereco':'string',
        'cep':'string',
        'email':'string',
        'telefones':'string'})
    df_produtos=pd.read_csv(filesPath["original_db"]["products"]).astype({
        'codigo':'string',
        'nome':'string',
        'modelo':'string',
        'fabricante':'string',
        'cor':'string',
        'tam':'string'})
    df_pedidos=pd.read_csv(filesPath["original_db"]["orders"]).astype({
        'id_cliente':'string',
        'cliente':'string',
        'endereco':'string',
        'cep':'string',
        'itens':'string',
        'qtdes':'string',
        'valor_pago':'string'})
    df_clientes_concorrente=pd.read_csv(filesPath["imported_db"]["customers"]).astype({
        'cpf':'string',
        'nome':'string',
        'endereco':'string',
        'cep':'string',
        'email':'string',
        'telefones':'string'})
    df_produtos_concorrente=pd.read_csv(filesPath["imported_db"]["products"]).astype({
        'codigo':'string',
        'nome':'string',
        'modelo':'string',
        'fabricante':'string',
        'cor':'string',
        'tam':'string'})
    
    print(f"\n[INFO] Dados carregados com sucesso:\n\n{json.dumps(filesPath,indent=2)}")

    return df_clientes, df_produtos, df_pedidos, df_clientes_concorrente, df_produtos_concorrente