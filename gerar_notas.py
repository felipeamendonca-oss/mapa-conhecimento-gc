import pandas as pd
import re
import os

# Seu link do Google Sheets já configurado perfeitamente
URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4JPkCXKpbzBTYDTi-dAWNKfEyH0NFQfUCpwNHVxL441BMh8JUOVRX_NR6MD7zHQ/pub?gid=316961322&single=true&output=csv"

output_dir = "content/autores" 
os.makedirs(output_dir, exist_ok=True)

# Lendo o CSV direto da Web
df = pd.read_csv(URL_GOOGLE_SHEETS)

# O PULO DO GATO: Remove espaços em branco invisíveis do início e fim das colunas
df.columns = df.columns.str.strip()

# Identifica as colunas de forma inteligente, ignorando maiúsculas/minúsculas ou acentos
col_autor = [c for c in df.columns if 'autor' in c.lower()][0]
col_area = [c for c in df.columns if 'área' in c.lower() or 'area' in c.lower()][0]
col_inst = [c for c in df.columns if 'nacionalidade' in c.lower() or 'institu' in c.lower()][0]
col_link = [c for c in df.columns if 'link' in c.lower() or 'curr' in c.lower()][0]
col_ref = [c for c in df.columns if 'trabalho' in c.lower() or 'refer' in c.lower()][0]

current_category = "Geral"

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()

for idx, row in df.iterrows():
    autor_raw = str(row[col_autor]).strip()
    
    if autor_raw.startswith('—') and autor_raw.endswith('—'):
        current_category = autor_raw.replace('—', '').strip()
        continue
    
    if pd.isna(row[col_area]) and pd.isna(row[col_ref]):
        continue
        
    autor = autor_raw
    area = str(row[col_area]).replace('"', "'") if pd.notna(row[col_area]) else ""
    inst = str(row[col_inst]).replace('"', "'") if pd.notna(row[col_inst]) else ""
    link = row[col_link] if pd.notna(row[col_link]) else ""
    ref = str(row[col_ref]).replace('"', "'") if pd.notna(row[col_ref]) else ""
    
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