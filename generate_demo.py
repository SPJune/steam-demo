import os

# sex.txt 파일 읽기
def read_sex_file(file_path):
    sex_info = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                i, spk1_sex, spk2_sex = parts
                sex_info[int(i)] = (spk1_sex, spk2_sex)
    return sex_info

# index.html 생성하기
def create_html(sex_info, output_file='index.html'):
    with open(output_file, 'w') as file:
        # HTML 헤더 작성
        file.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speaker Separation Demo</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
        audio {
            width: 200px;
        }
    </style>
</head>
<body>
    <h1>Speaker Separation Demo</h1>
    <table>
        <thead>
            <tr>
                <th>Num</th>
                <th>Speaker 1 Sex</th>
                <th>Speaker 2 Sex</th>
                <th>Mixture</th>
                <th>Predicted</th>
                <th>Ground Truth</th>
            </tr>
        </thead>
        <tbody>
''')

        # 각각의 row 작성
        for i in range(10):
            spk1_sex, spk2_sex = sex_info.get(i, ('N/A', 'N/A'))
            mix_file = f'batch{i}_mix.wav'
            recon_file = f'batch{i}_recon.wav'
            spk1_file = f'batch{i}_spk1.wav'
            
            file.write(f'''
            <tr>
                <td>{i}</td>
                <td>{spk1_sex}</td>
                <td>{spk2_sex}</td>
                <td><audio controls><source src="{mix_file}" type="audio/wav"></audio></td>
                <td><audio controls><source src="{recon_file}" type="audio/wav"></audio></td>
                <td><audio controls><source src="{spk1_file}" type="audio/wav"></audio></td>
            </tr>
            ''')

        # HTML 푸터 작성
        file.write('''
        </tbody>
    </table>
</body>
</html>
''')

# 메인 실행 함수
if __name__ == "__main__":
    sex_info = read_sex_file('sex.txt')
    create_html(sex_info)
    print("index.html has been created.")
