let currentDebateData = null;
let charts = {};
let downloadInProgress = false;

function switchTab(tabName) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    // Add active class to selected tab
    document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const isVideo = file.type.startsWith('video/');
        const mediaType = isVideo ? 'vídeo' : 'áudio';
        document.querySelector('#file-tab .file-upload p').textContent = `${mediaType} selecionado: ${file.name}`;
    }
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
    })
    .catch(error => {
        alert(error.message || 'Erro ao baixar áudio');
        document.getElementById('loading').classList.add('hidden');
    });
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

function loadData() {
    currentDebateData = {
        duration: "45:30",
        totalWords: 8432,
        candidates: [
            {
                name: "Candidato A",
                speakingTime: 1250,
                wordCount: 3200,
                sentiment: 0.7,
                keywords: ["economia", "saúde", "educação", "segurança"],
                wordcloud: generateWordcloudData("economia saúde educação segurança desenvolvimento social política")
            },
            {
                name: "Candidato B",
                speakingTime: 1180,
                wordCount: 2950,
                sentiment: 0.6,
                keywords: ["trabalho", "moradia", "transporte", "meio ambiente"],
                wordcloud: generateWordcloudData("trabalho moradia transporte meio ambiente sustentabilidade")
            }
        ],
        transcript: `
<div class="speaker-name">Mediador:</div>
Boa noite e bem-vindos ao debate eleitoral. Vamos começar com o primeiro bloco sobre economia.

<div class="speaker-name">Candidato A:</div>
Obrigado. Nosso plano econômico foca no desenvolvimento sustentável, com investimentos em saúde e educação como pilares fundamentais para o crescimento...

<div class="speaker-name">Candidato B:</div>
Respeitosamente, discordo. O que precisamos é de políticas concretas para geração de empregos, moradia popular e melhoria do transporte público...
`,
        interestPoints: [
            "Proposta de reforma tributária",
            "Debate sobre sistema de saúde",
            "Discussão sobre segurança pública",
            "Políticas para juventude",
            "Sustentabilidade ambiental"
        ],
        topics: {
            "Economia": 28,
            "Saúde": 22,
            "Educação": 20,
            "Segurança": 15,
            "Meio Ambiente": 10,
            "Outros": 5
        }
    };

    displayResults();
}

function displayResults() {
    document.getElementById('results').classList.remove('hidden');

    // Estatísticas gerais
    document.getElementById('totalDuration').textContent = currentDebateData.duration;
    document.getElementById('totalWords').textContent = currentDebateData.totalWords.toLocaleString();
    document.getElementById('candidateCount').textContent = currentDebateData.candidates.length;

    // Pontos de interesse
    const keywordsList = document.getElementById('keywordsList');
    keywordsList.innerHTML = '';
    currentDebateData.interestPoints.forEach(point => {
        const tag = document.createElement('div');
        tag.className = 'keyword-tag';
        tag.textContent = point;
        keywordsList.appendChild(tag);
    });

    // Nuvem de palavras geral
    createWordcloud('generalWordcloud', generateGeneralWordcloud());

    // Gráfico de tempo de fala
    createSpeakingTimeChart();

    // Análise por candidato
    createCandidateAnalysis();

    // Transcrição
    document.getElementById('transcriptContent').innerHTML = currentDebateData.transcript;
}

function generateWordcloudData(text) {
    const words = text.split(' ');
    return words.map(word => [word, Math.floor(Math.random() * 50) + 10]);
}

function generateGeneralWordcloud() {
    const words = [
        ['economia', 45], ['saúde', 40], ['educação', 38], ['segurança', 35],
        ['trabalho', 32], ['moradia', 28], ['transporte', 25], ['tecnologia', 22],
        ['meio ambiente', 20], ['juventude', 18], ['cultura', 15], ['inovação', 12]
    ];
    return words;
}

function createWordcloud(containerId, data) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    // Criar representação visual simples da nuvem de palavras
    data.forEach(([word, weight]) => {
        const span = document.createElement('span');
        span.textContent = word;
        span.style.fontSize = `${Math.max(weight / 3, 12)}px`;
        span.style.color = `hsl(${Math.random() * 360}, 70%, 50%)`;
        span.style.margin = '5px';
        span.style.display = 'inline-block';
        span.style.fontWeight = weight > 30 ? 'bold' : 'normal';
        container.appendChild(span);
    });
}

function createSpeakingTimeChart() {
    const ctx = document.getElementById('speakingTimeChart').getContext('2d');

    if (charts.speakingTime) {
        charts.speakingTime.destroy();
    }

    charts.speakingTime = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: currentDebateData.candidates.map(c => c.name),
            datasets: [{
                data: currentDebateData.candidates.map(c => c.speakingTime),
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
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
    <div>
        <strong>Tempo de fala:</strong> ${Math.floor(candidate.speakingTime / 60)}:${(candidate.speakingTime % 60).toString().padStart(2, '0')}
        <br><strong>Palavras:</strong> ${candidate.wordCount.toLocaleString()}
        <br><strong>Sentimento:</strong> ${(candidate.sentiment * 100).toFixed(0)}% Positivo
    </div>
    <div>
        <strong>Palavras-chave:</strong>
        <div style="margin-top: 10px;">
            ${candidate.keywords.map(keyword =>
            `<span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; margin-right: 5px; display: inline-block; margin-bottom: 5px;">${keyword}</span>`
        ).join('')}
        </div>
    </div>
    <div>
        <strong>Nuvem de palavras:</strong>
        <div id="candidate-wordcloud-${index}" style="height: 100px; border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-top: 10px; background: white;"></div>
    </div>
</div>
`;

        container.appendChild(candidateDiv);

        // Criar nuvem de palavras do candidato
        createWordcloud(`candidate-wordcloud-${index}`, candidate.wordcloud);
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

    // Detectar tipo de plataforma e sugerir qualidade
    urlInput.addEventListener('blur', function () {
        const url = this.value.trim();
        const qualitySelect = document.getElementById('qualitySelect');

        if (url.includes('youtube.com') || url.includes('youtu.be')) {
            // Para YouTube, sugerir qualidade baseada no tipo de conteúdo
            if (url.includes('podcast') || url.includes('entrevista') || url.includes('debate')) {
                qualitySelect.value = 'audio';
            }
        }
    });
});