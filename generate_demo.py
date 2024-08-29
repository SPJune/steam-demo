import os
import pandas as pd
from IPython.display import display, Audio, HTML

# 파일 경로 설정
audio_dir = './audio_files/'
sex_file = 'sex.txt'

# 성별 정보를 불러오기
sex_info = pd.read_csv(sex_file, sep=' ', header=None, names=['num', 'spk1_sex', 'spk2_sex'])

# HTML 테이블 생성을 위한 리스트
rows = []

# 성별 정보와 오디오 파일을 매칭하여 데모 생성
for i in range(11):  # num은 0부터 10까지
    # 오디오 파일 경로
    mix_file = os.path.join(audio_dir, f'batch{i}_mix.wav')
    recon_file = os.path.join(audio_dir, f'batch{i}_recon.wav')
    spk1_file = os.path.join(audio_dir, f'batch{i}_spk1.wav')
    
    # 해당 num의 성별 정보
    spk1_sex = sex_info.loc[sex_info['num'] == i, 'spk1_sex'].values[0]
    spk2_sex = sex_info.loc[sex_info['num'] == i, 'spk2_sex'].values[0]
    
    # HTML row 생성
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

# 전체 HTML 테이블 구성
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

# HTML 페이지 출력
display(HTML(table_html))
