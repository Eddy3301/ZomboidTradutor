import json
import os
import time
from deep_translator import GoogleTranslator

def iniciar_projeto():
    pasta_entrada = "Entrada"
    pasta_saida = "Saida"
    arquivo_nome = "ItemName.json"

    input_path = os.path.join(pasta_entrada, arquivo_nome)
    output_path = os.path.join(pasta_saida, arquivo_nome)

    if not os.path.exists(input_path):
        print(f"Erro: Arquivo não encontrado em {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        dados_originais = json.load(f)

    print(f"--- Sucesso! Lendo {len(dados_originais)} itens ---")

    dados_traduzidos = {}

    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                dados_traduzidos = json.load(f)
            print(f"--- Resumindo de {len(dados_traduzidos)} itens já traduzidos ---")
        except Exception as e:
            print(f"Atenção: falha ao carregar checkpoint '{output_path}': {e}")
            print("Reiniciando traduções do zero.")
            dados_traduzidos = {}

    tradutor = GoogleTranslator(source='en', target='pt')

    def _salvar_checkpoint():
        tmp_path = output_path + '.tmp'
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(dados_traduzidos, f, indent=4, ensure_ascii=False)

        os.replace(tmp_path, output_path)

    total = len(dados_originais)
    processed = 0

    for i, (chave, valor_ingles) in enumerate(dados_originais.items(), 1):
        if chave in dados_traduzidos:
            continue

        try:
            valor_portugues = tradutor.translate(valor_ingles)
            dados_traduzidos[chave] = valor_portugues
            print(f"[{i}/{total}] {valor_ingles} -> {valor_portugues}")
            time.sleep(0.2)
        except Exception as e:
            print(f"Erro no item {chave}: {e}")
            dados_traduzidos[chave] = valor_ingles

        processed += 1

        if processed % 50 == 0:
            _salvar_checkpoint()
            print(f"--- Checkpoint: {processed} itens salvos em disco ---")

    _salvar_checkpoint()

    print(f"\n--- Finalizado com sucesso! (total traduzido: {len(dados_traduzidos)}/{total}) ---")

if __name__ == "__main__":
    iniciar_projeto()