
# 🎙️ App Transcript

Aplicação em **Streamlit** para **transcrição de áudio e vídeo** utilizando a API **OpenAI Whisper**.
Permite enviar arquivos `.mp3` ou `.mp4`, aplicar um *prompt de correção/contexto* e receber a transcrição em texto.

---

![Demonstração do App](demo.gif)


## 🚀 Funcionalidades

* Transcrição de **áudios (.mp3)** usando o modelo `whisper-1`.
* Transcrição de **vídeos (.mp4)** com extração automática do áudio.
* Suporte a **prompts opcionais** para orientar correções de nomes, contexto ou domínio.
* Evita transcrições repetidas usando **hash MD5** do arquivo enviado.
* Limpeza automática de arquivos temporários.
* Interface simples e amigável em Streamlit.
* Processamento robusto com tratamento de erros.

---

## 🧰 Tecnologias Utilizadas

* Python 3.10+
* Streamlit
* OpenAI Python SDK
* MoviePy
* dotenv
* hashlib
* ffmpeg (necessário para MoviePy extrair áudio)

---

## 📦 Instalação

Clone o repositório:

```bash
https://github.com/ZeyOliveira/audio-video-transcriber-streamlit.git
```

Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔑 Variáveis de Ambiente

O projeto utiliza `.env`.
Crie um arquivo `.env` na raiz com:

```
OPENAI_API_KEY=coloque_sua_chave_aqui
```

O código carrega automaticamente via:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## ▶️ Como Executar

Inicie o app Streamlit:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em:

```
http://localhost:8501
```

---

## 📁 Estrutura do Projeto

```
├── app.py               # Código principal
├── requirements.txt     # Dependências
├── README.md            # Este arquivo
├── .env.example         # Exemplo de configuração
└── temp/                # Arquivos temporários (gerados em runtime)
```

---

## 📝 Como Funciona

### 1. Upload

O usuário envia um arquivo `.mp3` ou `.mp4`.

### 2. Hash do arquivo

O app gera:

```python
hashlib.md5(content).hexdigest()
```

Isso evita transcrições repetidas enquanto a aplicação está aberta.

### 3. Processamento

* Para vídeos: MoviePy extrai o áudio para `temp/audio.mp3`.
* Para áudios: o arquivo vai direto para a API.

### 4. Transcrição

A chamada à API é feita assim:

```python
openai.audio.transcriptions.create(
    model='whisper-1',
    language='pt',
    response_format='text',
    file=file_audio,
    prompt=prompt
)
```

### 5. Exibição

O texto final aparece em um `st.text_area()`.

---

## ⚠️ Observações Importantes

* Certifique-se de ter o **FFmpeg** instalado:

  * Windows: https
  * Linux/macOS: geralmente já vem ou pode ser instalado via pacote (`apt`, `brew` etc.)
* O projeto **não armazena registros** das transcrições de forma persistente.
* A extração de áudio pode falhar caso o arquivo `.mp4` esteja corrompido.

---

## Autor

**Zeygler Oliveira**
*   Estudante de Ciência de Dados
*   Foco em Ciência de dados, MLOps, LLMOps.
*   Buscando oportunidades na área de TI.
  
Conecte-se comigo! Estou sempre aberto a discussões sobre dados, projetos e oportunidades na área de TI.

*   **LinkedIn:** https://www.linkedin.com/in/zeygleroliveira/
*   **GitHub:** https://github.com/ZeyOliveira
