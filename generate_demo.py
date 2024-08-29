import os
import pandas as pd
from IPython.display import display, Audio, HTML

audio_dir = './audio_files/'
sex_file = 'sex.txt'

sex_info = pd.read_csv(sex_file, sep=' ', header=None, names=['num', 'spk1_sex', 'spk2_sex'])

rows = []

for i in range(10):  
    mix_file = os.path.join(audio_dir, f'batch{i}_mix.wav')
    recon_file = os.path.join(audio_dir, f'batch{i}_recon.wav')
    spk1_file = os.path.join(audio_dir, f'batch{i}_spk1.wav')
    
    spk1_sex_row = sex_info.loc[sex_info['num'] == i, 'spk1_sex']
    spk2_sex_row = sex_info.loc[sex_info['num'] == i, 'spk2_sex']
    
    if not spk1_sex_row.empty and not spk2_sex_row.empty:
        spk1_sex = spk1_sex_row.values[0]
        spk2_sex = spk2_sex_row.values[0]
    else:
        print(f"Warning: No gender information found for num={i}. Skipping this entry.")
        continue 
    
    row = f"""
    <tr>
        <td>{i}</td>
        <td>{spk1_sex}</td>
        <td>{spk2_sex}</td>
        <td>{Audio(mix_file).data}</td>
        <td>{Audio(recon_file).data}</td>
        <td>{Audio(spk1_file).data}</td>
    </tr>
    """
    rows.append(row)

table_html = f"""
<table border="1">
    <tr>
        <th>Num</th>
        <th>Spk1 Sex</th>
        <th>Spk2 Sex</th>
        <th>Mixture</th>
        <th>Predicted</th>
        <th>GT</th>
    </tr>
    {''.join(rows)}
</table>
"""

display(HTML(table_html))
with open('demo.html', 'w') as f:
    f.write(table_html)
