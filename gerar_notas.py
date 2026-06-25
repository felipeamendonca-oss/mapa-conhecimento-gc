import pandas as pd
import re
import os

# SUBSTUIE ESTE LINK pelo link do CSV que copiaste do Google Sheets
URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4JPkCXKpbzBTYDTi-dAWNKfEyH0NFQfUCpwNHVxL441BMh8JUOVRX_NR6MD7zHQ/pub?gid=316961322&single=true&output=csv"

# Pasta onde as notas vão ficar guardadas para o site
output_dir = "content/autores" 
os.makedirs(output_dir, exist_ok=True)

# Lendo o CSV direto da Web
df = pd.read_csv(URL_GOOGLE_SHEETS)

current_category = "Geral"

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()

for idx, row in df.iterrows():
    autor_raw = str(row['Autor']).strip()
    
    if autor_raw.startswith('—') and autor_raw.endswith('—'):
        current_category = autor_raw.replace('—', '').strip()
        continue
    
    if pd.isna(row['Área principal']) and pd.isna(row['Trabalho de referência / mais recente']):
        continue
        
    autor = autor_raw
    area = str(row['Área principal']).replace('"', "'") if pd.notna(row['Área principal']) else ""
    inst = str(row['Nacionalidade / Instituição']).replace('"', "'") if pd.notna(row['Nacionalidade / Instituição']) else ""
    link = row['Link currículo'] if pd.notna(row['Link currículo']) else ""
    ref = str(row['Trabalho de referência / mais recente']).replace('"', "'") if pd.notna(row['Trabalho de referência / mais recente']) else ""
    
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
