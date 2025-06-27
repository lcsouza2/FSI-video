let currentDebateData = null;
let charts = {};
let downloadInProgress = false;
let selectedFile = null;

function switchTab(tabName) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    // Add active class to selected tab
    document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function showLoading(message, showProgress = false) {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('loadingText').textContent = message;

    const progressBar = document.getElementById('progressBar');
    if (showProgress) {
        progressBar.classList.remove('hidden');
    } else {
        progressBar.classList.add('hidden');
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        selectedFile = file; // Salva para processar depois
        const isVideo = file.type.startsWith('video/');
        const mediaType = isVideo ? 'vídeo' : 'áudio';
        document.querySelector('#file-tab .file-upload p').textContent = `${mediaType} selecionado: ${file.name}`;
    }
}

function processDebate() {
    if (!selectedFile) {
        alert('Por favor, selecione um arquivo de áudio ou vídeo primeiro.');
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    showLoading('Processando debate...', true);

    fetch("http://localhost:8000/process/fromfile?", {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (!response.ok) throw new Error('Erro ao transcrever arquivo');
            return response.json();
        })
        .then(data => {
            showLoading('Transcrição concluída!', false);
            setTimeout(() => {
                document.getElementById('loading').classList.add('hidden');
            }, 1500);

            currentDebateData = data;
            displayResults();

        })
        .catch(error => {
            alert(error.message || 'Erro ao transcrever arquivo');
            document.getElementById('loading').classList.add('hidden');
        });

}

function downloadFromUrl() {
    const url = document.getElementById('videoUrl').value.trim();
    const quality = document.getElementById('qualitySelect').value;

    if (!url) {
        alert('Por favor, insira uma URL válida.');
        return;
    }

    if (!isValidUrl(url)) {
        alert('Por favor, insira uma URL válida (deve começar com http:// ou https://).');
        return;
    }

    downloadInProgress = true;
    showLoading('Baixando áudio...', true);

    if (quality === 'audio') {
        endpoint = "http://localhost:8000/download/audio?url=" + encodeURIComponent(url);
    } else {
        endpoint = "http://localhost:8000/download/video?url=" + encodeURIComponent(url);
    }

    fetch(endpoint, {
        method: "POST"
    })
        .then(response => {
            if (!response.ok) throw new Error('Erro ao baixar áudio');
            return response.blob();
        })
        .then(blob => {
            // Cria um link para download do arquivo de áudio
            const downloadUrl = window.URL.createObjectURL(blob);
            selectedFile = downloadUrl;
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = "Audio_baixado.mp3";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(downloadUrl);

            showLoading('Áudio baixado com sucesso!', false);
            setTimeout(() => {
                document.getElementById('loading').classList.add('hidden');
            }, 1500);

            showLoading('Processando debate... Isso pode tomar um bom tempo', false);
            processDebate()
        })
        .catch(error => {
            alert(error.message || 'Erro ao baixar áudio');
            document.getElementById('loading').classList.add('hidden');
        });
}

function formatDuration(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return [
        h > 0 ? h.toString().padStart(2, '0') : '00',
        m.toString().padStart(2, '0'),
        s.toString().padStart(2, '0')
    ].join(':');
}

function displayResults() {
    document.getElementById('results').classList.remove('hidden');


    document.getElementById('totalDuration').textContent = formatDuration(currentDebateData.duration);
    document.getElementById('totalWords').textContent = currentDebateData.total_words.toLocaleString();
    document.getElementById('MostUsedWord').textContent = currentDebateData.most_used_word;

    createSpeakingTimeChart();

    createCandidateAnalysis();

    currentDebateData.interest_points.forEach((point, index) => {
        const pointDiv = document.createElement('div');
        pointDiv.className = 'interest-point';
        pointDiv.innerHTML = `
            <strong>Ponto de Interesse ${index + 1}:</strong> ${point}
        `;
        document.getElementById('interestPoints').appendChild(pointDiv);
    });

    document.getElementById('generalWordcloudImage').src = "http://localhost:8000/wordcloud?filename=" + encodeURIComponent(currentDebateData.wordcloud);
    document.getElementById('transcriptContent').innerText = currentDebateData.result;
}


function createSpeakingTimeChart() {
    const ctx = document.getElementById('speakingTimeChart').getContext('2d');

    if (charts.speakingTime) {
        charts.speakingTime.destroy();
    }

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: currentDebateData.candidates.map(c => c.name),
            datasets: [{
                data: currentDebateData.candidates.map(c => c.total_time),
                backgroundColor: ['#667eea', '#764ba2', '#f093fb'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createCandidateAnalysis() {
    const container = document.getElementById('candidateAnalysis');
    container.innerHTML = '';

    currentDebateData.candidates.forEach((candidate, index) => {
        const candidateDiv = document.createElement('div');
        candidateDiv.style.marginBottom = '30px';
        candidateDiv.style.padding = '20px';
        candidateDiv.style.border = '2px solid #ecf0f1';
        candidateDiv.style.borderRadius = '15px';
        candidateDiv.style.background = '#f8f9fa';

        candidateDiv.innerHTML = `
<h4 style="color: #2c3e50; margin-bottom: 15px; font-size: 1.3rem;">${candidate.name}</h4>
    <div class="grid"  style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">

        <div class="column-1">
            <div class="d-flex flex-column justify-content-between align-items-start gap-4 text-size-6">
                <div>
                    <strong>Tempo de fala:</strong> ${formatDuration(candidate.total_time)}
                    <br>
                </div>

                <div>
                    <strong>Palavras:</strong> ${candidate.word_count.toLocaleString()}
                    <br>
                </div>

                <div>
                    <strong>Palavra mais dita:</strong>
                    <br>${candidate.most_used_word.toLocaleString()}
                </div>
            </div>
        </div>

        <div class="column-2 d-flex flex-column align-items-center">
            <strong>Nuvem de palavras:</strong>
                <img class="image-fluid" id="candidate-wordcloud-${index}"
                    src="http://localhost:8000/wordcloud?filename=${encodeURIComponent(candidate.wordcloud)}"
                    style="max-height: 20vh; border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-top: 10px; background: white;">
        </div>

        <div class="column-3">
            <strong>Todas as falas</strong>
            <div
                style="max-height: 150px; overflow-y: auto; border: 1px solid #ddd; border-radius: 10px; padding: 10px; background: #fff;">
                ${candidate.full_text.map(speech => `<p>${speech}</p>`).join('')}
            </div>
        </div>
`;
        container.appendChild(candidateDiv);
    });
}

// Inicialização
document.addEventListener('DOMContentLoaded', function () {
    // Configurar drag and drop para ambas as abas
    const uploadArea = document.querySelector('.file-upload');

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#2980b9';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#3498db';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#3498db';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('audio/') || file.type.startsWith('video/')) {
                document.getElementById('mediaFile').files = files;
                handleFileUpload({ target: { files: files } });
            } else {
                alert('Por favor, selecione apenas arquivos de áudio ou vídeo.');
            }
        }
    });

    // Validação de URL em tempo real
    const urlInput = document.getElementById('videoUrl');
    urlInput.addEventListener('input', function () {
        const url = this.value.trim();
        if (url && !isValidUrl(url) && url.length > 10) {
            this.style.borderColor = '#e74c3c';
        } else if (url && isValidUrl(url)) {
            this.style.borderColor = '#27ae60';
        } else {
            this.style.borderColor = '#e3f2fd';
        }
    });
});
