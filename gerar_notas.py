import pandas as pd
import re
import os

# Agora o robô lê a planilha local, eliminando qualquer bloqueio do Google!
file_path = "autores_gc_educacao.xlsx"

output_dir = "content/autores" 
os.makedirs(output_dir, exist_ok=True)

# Lendo o arquivo Excel diretamente
df = pd.read_excel(file_path, sheet_name="Autores")

# Remove espaços em branco invisíveis das colunas
df.columns = df.columns.str.strip()

# Mapeia as colunas pela ordem de posição
if df.shape[1] >= 5:
    novas_colunas = ['Autor_Col', 'Area_Col', 'Inst_Col', 'Link_Col', 'Ref_Col']
    df.columns = novas_colunas + list(df.columns[len(novas_colunas):])

current_category = "Geral"

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()

for idx, row in df.iterrows():
    autor_raw = str(row['Autor_Col']).strip()
    
    if autor_raw.lower() in ['autor', 'nan', '']:
        continue
        
    if autor_raw.startswith('—') and autor_raw.endswith('—'):
        current_category = autor_raw.replace('—', '').strip()
        continue
        
    area = str(row['Area_Col']).replace('"', "'") if pd.notna(row['Area_Col']) else ""
    inst = str(row['Inst_Col']).replace('"', "'") if pd.notna(row['Inst_Col']) else ""
    link = str(row['Link_Col']).strip() if pd.notna(row['Link_Col']) else ""
    ref = str(row['Ref_Col']).replace('"', "'") if pd.notna(row['Ref_Col']) else ""
    
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

print("✨ Notas de autores atualizadas com sucesso localmente!")
