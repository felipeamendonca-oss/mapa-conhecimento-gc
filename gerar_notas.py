import pandas as pd
import re
import os

# Link oficial da sua planilha do Google Sheets
URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4JPkCXKpbzBTYDTi-dAWNKfEyH0NFQfUCpwNHVxL441BMh8JUOVRX_NR6MD7zHQ/pub?gid=316961322&single=true&output=csv"

output_dir = "content/autores" 
os.makedirs(output_dir, exist_ok=True)

# 1. Autodetecta o separador (suporta tanto o padrão americano ',' quanto o brasileiro ';')
try:
    df = pd.read_csv(URL_GOOGLE_SHEETS, sep=',')
    if df.shape[1] <= 1:
        df = pd.read_csv(URL_GOOGLE_SHEETS, sep=';')
except:
    df = pd.read_csv(URL_GOOGLE_SHEETS, sep=';')

# 2. Mapeia as colunas estritamente pela ordem de posição (1ª, 2ª, 3ª...) de forma blindada
if df.shape[1] >= 5:
    novas_colunas = ['Autor_Col', 'Area_Col', 'Inst_Col', 'Link_Col', 'Ref_Col']
    df.columns = novas_colunas + list(df.columns[len(novas_colunas):])

current_category = "Geral"

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()

# 3. Processamento das linhas
for idx, row in df.iterrows():
    autor_raw = str(row['Autor_Col']).strip()
    
    # Ignora linhas de cabeçalho repetidas ou vazias
    if autor_raw.lower() in ['autor', 'nan', '']:
        continue
        
    # Identifica a mudança de Eixo Temático
    if autor_raw.startswith('—') and autor_raw.endswith('—'):
        current_category = autor_raw.replace('—', '').strip()
        continue
    
    # Pula linhas sem conteúdo útil de pesquisa
    area_val = str(row['Area_Col']).strip()
    ref_val = str(row['Ref_Col']).strip()
    if (pd.isna(row['Area_Col']) or area_val.lower() == 'nan' or area_val == '') and \
       (pd.isna(row['Ref_Col']) or ref_val.lower() == 'nan' or ref_val == ''):
        continue
        
    autor = autor_raw
    area = str(row['Area_Col']).replace('"', "'") if pd.notna(row['Area_Col']) else ""
    inst = str(row['Inst_Col']).replace('"', "'") if pd.notna(row['Inst_Col']) else ""
    link = str(row['Link_Col']).strip() if pd.notna(row['Link_Col']) else ""
    ref = str(row['Ref_Col']).replace('"', "'") if pd.notna(row['Ref_Col']) else ""
    
    filename = clean_filename(autor) + ".md"
    filepath = os.path.join(output_dir, filename)
    
    md_content = f"""---
title: "{autor}"
tags:
  - autor
categoria: "{current_category}"
---
# {autor}

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

print("Notas de autores atualizadas com sucesso!")