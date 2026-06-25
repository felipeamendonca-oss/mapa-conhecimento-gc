import pandas as pd
import re
import os
import requests

# Link oficial da sua planilha do Google Sheets
URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4JPkCXKpbzBTYDTi-dAWNKfEyH0NFQfUCpwNHVxL441BMh8JUOVRX_NR6MD7zHQ/pub?gid=316961322&single=true&output=csv"

output_dir = "content/autores" 
os.makedirs(output_dir, exist_ok=True)

print("\n--- 🔍 INICIANDO DIAGNÓSTICO DA PLANILHA ---")

# Teste de leitura bruta para detetar bloqueios do Google
try:
    r = requests.get(URL_GOOGLE_SHEETS, timeout=10)
    texto_inicial = r.text[:300].lower()
    print(f"📍 Resposta do servidor Google: Status {r.status_code}")
    if "<html" in texto_inicial or "doctype html" in texto_inicial:
        print("🚨 ALERTA CRÍTICO: O link não está a enviar os dados da planilha!")
        print("Ele está a retornar uma página de login. Isto acontece porque a sua conta Google é institucional")
        print("e as regras da organização bloqueiam o acesso externo de robôs. Tente usar uma conta @gmail.com pessoal.")
except Exception as e:
    print(f"Aviso no pré-teste: {e}")

# Tentativa de leitura inteligente dos dados
df = None
for separador in [',', ';']:
    try:
        temp_df = pd.read_csv(URL_GOOGLE_SHEETS, sep=separador)
        if temp_df.shape[1] >= 2:
            df = temp_df
            print(f"✅ Sucesso ao ler dados com o separador: '{separador}'")
            print(f"📊 Dimensões encontradas: {df.shape[0]} linhas e {df.shape[1]} colunas.")
            break
    except:
        continue

if df is None:
    print("🚨 ERRO: O robô não conseguiu estruturar nenhuma tabela com este link.")
    exit(1)

# Mapeamento dinâmico de colunas por posição para evitar erros de nomes (KeyError)
num_cols = df.shape[1]
nomes_padrao = ['Autor_Col', 'Area_Col', 'Inst_Col', 'Link_Col', 'Ref_Col']
df.columns = [nomes_padrao[i] if i < len(nomes_padrao) else f"Col_{i}" for i in range(num_cols)]

current_category = "Geral"

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()

# Geração das notas Markdown
if 'Autor_Col' in df.columns:
    for idx, row in df.iterrows():
        autor_raw = str(row['Autor_Col']).strip()
        
        if autor_raw.lower() in ['autor', 'nan', '']:
            continue
            
        if autor_raw.startswith('—') and autor_raw.endswith('—'):
            current_category = autor_raw.replace('—', '').strip()
            continue
        
        # Coleta segura mesmo se faltarem colunas no arquivo original
        area = str(row['Area_Col']).replace('"', "'") if 'Area_Col' in df.columns and pd.notna(row['Area_Col']) else ""
        inst = str(row['Inst_Col']).replace('"', "'") if 'Inst_Col' in df.columns and pd.notna(row['Inst_Col']) else ""
        link = str(row['Link_Col']).strip() if 'Link_Col' in df.columns and pd.notna(row['Link_Col']) else ""
        ref = str(row['Ref_Col']).replace('"', "'") if 'Ref_Col' in df.columns and pd.notna(row['Ref_Col']) else ""
        
        if area.lower() == 'nan': area = ""
        if inst.lower() == 'nan': inst = ""
        if link.lower() == 'nan': link = ""
        if ref.lower() == 'nan': ref = ""
        
        filename = clean_filename(autor_raw) + ".md"
        filepath = os.path.join(output_dir, filename)
        
        md_content = f"""---
title: "{autor_raw}"
tags:
  - autor
categoria: "{current_category}"
---
# {autor_raw}

- **Área Principal:** {area}
- **Instituição:** {inst}
- **Currículo:** [Link]({link})

## Referência
> {ref}

---
Eixo: [[Eixo - {current_category}]]
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

print("✨ Notas de autores atualizadas com sucesso!")
