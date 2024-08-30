import os

project_folder = '.'

def load_sex_info():
    sex_info = {}
    with open(os.path.join(project_folder, 'sex.txt'), 'r') as f:
        for line in f:
            parts = line.strip().split()
            num = int(parts[0])
            sex_info[num] = (parts[1], parts[2])
    return sex_info

# 모델 폴더 탐색
def get_model_folders():
    return [f for f in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, f))]

# index.html 생성
def create_index_html():
    sex_info = load_sex_info()
    model_folders = get_model_folders()

    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speaker Separation Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        select {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Speaker Separation Demo</h1>
    <label for="modelSelect">Select Model:</label>
    <select id="modelSelect" onchange="updateTable()">
        <option value="">Select a model</option>'''

    # 모델 옵션 추가
    for model in model_folders:
        html_content += f'\n        <option value="{model}">{model}</option>'

    html_content += '''
    </select>

    <table id="audioTable">
        <thead>
            <tr>
                <th>Num</th>
                <th>Spk1 Sex</th>
                <th>Spk2 Sex</th>
                <th>Mixture</th>
                <th>Recon1</th>
                <th>Spk1</th>
                <th>Recon2</th>
                <th>Spk2</th>
            </tr>
        </thead>
        <tbody>'''

    for i in range(10):
        spk1_sex, spk2_sex = sex_info[i]
        html_content += f'''
            <tr class="model-row" id="model-{i}" style="display:none">
                <td>{i}</td>
                <td>{spk1_sex}</td>
                <td>{spk2_sex}</td>
                <td><audio controls><source src="" id="mix-{i}">Your browser does not support the audio element.</audio></td>
                <td><audio controls><source src="" id="recon1-{i}">Your browser does not support the audio element.</audio></td>
                <td><audio controls><source src="" id="spk1-{i}">Your browser does not support the audio element.</audio></td>
                <td><audio controls><source src="" id="recon2-{i}">Your browser does not support the audio element.</audio></td>
                <td><audio controls><source src="" id="spk2-{i}">Your browser does not support the audio element.</audio></td>
            </tr>'''

    html_content += '''
        </tbody>
    </table>

    <script>
        const modelFolders = ''' + str(model_folders) + ''';

        function updateTable() {
            const modelSelect = document.getElementById("modelSelect");
            const selectedModel = modelSelect.value;

            document.querySelectorAll(".model-row").forEach(row => {
                row.style.display = selectedModel ? "" : "none";
            });

            if (selectedModel) {
                for (let i = 0; i < 10; i++) {
                    document.getElementById(`mix-${i}`).src = `${selectedModel}/batch${i}_mix.wav`;
                    document.getElementById(`recon1-${i}`).src = `${selectedModel}/batch${i}_recon1.wav`;
                    document.getElementById(`spk1-${i}`).src = `${selectedModel}/batch${i}_spk1.wav`;
                    document.getElementById(`recon2-${i}`).src = `${selectedModel}/batch${i}_recon2.wav`;
                    document.getElementById(`spk2-${i}`).src = `${selectedModel}/batch${i}_spk2.wav`;
                }
            }
        }
    </script>
</body>
</html>'''

    # index.html 파일로 저장
    with open(os.path.join(project_folder, 'index.html'), 'w') as f:
        f.write(html_content)

# 스크립트 실행
if __name__ == "__main__":
    create_index_html()
