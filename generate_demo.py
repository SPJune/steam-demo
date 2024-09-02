import os
import json

def generate_html():
    # 프로젝트 폴더 내의 모든 하위 폴더 찾기
    model_folders = [f for f in os.listdir('.') if os.path.isdir(f) and f != '.git']

    # sex.txt 파일 읽기
    sex_dict = {}
    with open('sex.txt', 'r') as f:
        for line in f:
            num, spk1_sex, spk2_sex = line.strip().split()
            sex_dict[int(num)] = (spk1_sex, spk2_sex)
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Speaker Separation Demo</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { max-width: 800px; margin: 0 auto; padding: 20px; }
            select { margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            audio { width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Speaker Separation Demo</h1>
            <select id="modelSelect" onchange="loadAudioSamples()">
                <option value="audio_files">audio_files</option>
                """ + ''.join([f'<option value="{folder}">{folder}</option>' for folder in model_folders if folder != 'audio_files']) + """
            </select>
            <div id="audioSamples"></div>
        </div>
        <script>
        function loadAudioSamples() {
            const modelName = document.getElementById('modelSelect').value;
            const audioSamples = document.getElementById('audioSamples');
            audioSamples.innerHTML = '';

            if (!modelName) return;

            const table = document.createElement('table');
            const headerRow = table.insertRow();
            ['Num', 'Spk1 Sex', 'Spk2 Sex', 'Mixture', 'Recon1', 'Spk1', 'Recon2', 'Spk2'].forEach(text => {
                const th = document.createElement('th');
                th.textContent = text;
                headerRow.appendChild(th);
            });

            for (let i = 0; i < 10; i++) {
                const row = table.insertRow();
                const sexInfo = sexDict[i];
                [
                    i,
                    sexInfo[0],
                    sexInfo[1],
                    `${modelName}/batch${i}_mix.wav`,
                    `${modelName}/batch${i}_recon1.wav`,
                    `${modelName}/batch${i}_spk1.wav`,
                    `${modelName}/batch${i}_recon2.wav`,
                    `${modelName}/batch${i}_spk2.wav`
                ].forEach((content, index) => {
                    const cell = row.insertCell();
                    if (index < 3) {
                        cell.textContent = content;
                    } else {
                        const audio = document.createElement('audio');
                        audio.controls = true;
                        audio.src = content;
                        cell.appendChild(audio);

                        // 오디오를 원터치로 재생 가능하도록 설정
                        audio.addEventListener('canplaythrough', () => audio.play());
                    }
                });
            }

            audioSamples.appendChild(table);
        }

        // 페이지 로드 시 기본 폴더 선택 및 오디오 샘플 로드
        window.onload = function() {
            loadAudioSamples();
        };

        const sexDict = """ + json.dumps(sex_dict) + """;
        </script>
    </body>
    </html>
    """

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_html()
    print("index.html file has been generated successfully.")
