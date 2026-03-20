import json
import os
import time
from deep_translator import GoogleTranslator # Nova biblioteca

def iniciar_projeto():
    pasta_entrada = "Entrada"
    pasta_saida = "Saida"
    arquivo_nome = "ItemName.json"

    input_path = os.path.join(pasta_entrada, arquivo_nome)
    output_path = os.path.join(pasta_saida, arquivo_nome)

    if not os.path.exists(input_path):
        print(f"Erro: Arquivo não encontrado em {input_path}")
        return

    # LEITURA
    with open(input_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    print(f"--- Sucesso! Lendo {len(dados)} itens ---")

    dados_traduzidos = {}
    
    # Configura o tradutor (Inglês para Português)
    tradutor = GoogleTranslator(source='en', target='pt')

    for i, (chave, valor_ingles) in enumerate(dados.items(), 1):
        try:
            # Tradução
            valor_portugues = tradutor.translate(valor_ingles)
            dados_traduzidos[chave] = valor_portugues
            
            print(f"[{i}/{len(dados)}] {valor_ingles} -> {valor_portugues}")
            
            # Delay curto (0.2s) para ser rápido mas seguro
            time.sleep(0.2)
        except Exception as e:
            print(f"Erro no item {chave}: {e}")
            dados_traduzidos[chave] = valor_ingles

    # ESCRITA
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dados_traduzidos, f, indent=4, ensure_ascii=False)

    print(f"\n--- Finalizado com sucesso! ---")

if __name__ == "__main__":
    iniciar_projeto()