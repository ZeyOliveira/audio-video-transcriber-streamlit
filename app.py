from openai.types import Video
from openai.types.audio import transcription
import streamlit as st
import openai
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv, find_dotenv
import os
import hashlib

_ = load_dotenv(find_dotenv())
openai = openai.Client()

folder_temp = "temp"
folder_audio = f"{folder_temp}/audio.mp3"
folder_video = f"{folder_temp}/video.mp4"

os.makedirs(folder_temp, exist_ok=True)

# ------------ UTILITÁRIOS --------------

def hash_file(file):
    """Cria um hash do arquivo para evitar transcrições repetidas."""
    file.seek(0)
    content = file.read()
    file.seek(0)
    return hashlib.md5(content).hexdigest()

def safe_remove(path):
    """Remove arquivos temporários sem quebrar a execução."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except:
        pass


# --------------- BACK-END -----------------

def transcreve_audio(file_audio, prompt=None):
    """Transcreve áudio usando a API da OpenAI, com melhora de erros."""
    try:
        if not file_audio:
            return None

        with st.spinner("Transcrevendo áudio..."):
            transcription = openai.audio.transcriptions.create(
                model='whisper-1',
                language='pt',
                response_format='text',
                file=file_audio,
                prompt=prompt
            )
            return transcription
    except Exception as e:
        st.error(f"Erro ao transcrever áudio: {e}")
        return None


def transcreve_video(file_video, prompt=None):
    """Extrai o áudio do vídeo e transcreve usando a API da OpenAI."""
    if not file_video:
        return None

    try:
        with st.spinner("Processando vídeo..."):
            with open(folder_video, "wb") as f:
                f.write(file_video.read())

            video_clip = VideoFileClip(folder_video)

            # Verifica se o vídeo tem áudio
            if video_clip.audio is None:
                st.error("O vídeo não contém faixa de áudio.")
                return None

            
            video_clip.audio.write_audiofile(folder_audio, logger=None)

        with open(folder_audio, "rb") as audio_file:
            with st.spinner("Transcrevendo áudio extraído..."):
                transcription = openai.audio.transcriptions.create(
                    model='whisper-1',
                    language='pt',
                    response_format='text',
                    file=audio_file,
                    prompt=prompt
                )

        return transcription

    except Exception as e:
        st.error(f"Erro ao processar vídeo: {e}")
        return None

    finally:
        # Limpa arquivos temporários
        safe_remove(folder_video)
        safe_remove(folder_audio)


# ---------------- FRONT-END -------------

def main():
    st.header("🎙️ App Transcript", divider=True)
    st.subheader("Transcreva áudios e vídeos")

    tabs = ["Vídeo", "Áudio"]
    tab_video, tab_audio = st.tabs(tabs)

    st.markdown("Use prompts curtos para orientar a transcrição (opcional).")

    # ---------------- Aba Vídeo -----------------------
    with tab_video:
        st.markdown("### Transcrição de Vídeo (.mp4)")
        prompt_video = st.text_input("Prompt para transcrição", key="prompt_video")
        file_video = st.file_uploader("Envie um vídeo .mp4", type=["mp4"])

        if file_video:
            st.info(f"Tamanho do arquivo: {round(file_video.size / 1024 / 1024, 2)} MB")

            file_hash = hash_file(file_video)

            if f"video_{file_hash}" not in st.session_state:
                transcription_video = transcreve_video(file_video, prompt_video)
                st.session_state[f"video_{file_hash}"] = transcription_video
            else:
                transcription_video = st.session_state[f"video_{file_hash}"]

            if transcription_video:
                st.success("Transcrição concluída com sucesso.")
                st.text_area("Resultado", transcription_video, height=300)


    # ------------ Aba Audio -----------------------
    with tab_audio:
        st.markdown("### Transcrição de Áudio (.mp3)")
        prompt_audio = st.text_input("Prompt para transcrição", key="prompt_audio")
        file_audio = st.file_uploader("Envie um áudio .mp3", type=["mp3"])

        if file_audio:
            st.info(f"Tamanho do arquivo: {round(file_audio.size / 1024 / 1024, 2)} MB")

            file_hash = hash_file(file_audio)

            if f"audio_{file_hash}" not in st.session_state:
                transcription_audio = transcreve_audio(file_audio, prompt_audio)
                st.session_state[f"audio_{file_hash}"] = transcription_audio
            else:
                transcription_audio = st.session_state[f"audio_{file_hash}"]

            if transcription_audio:
                st.success("Transcrição concluída com sucesso.")
                st.text_area("Resultado", transcription_audio, height=300)



if __name__ == "__main__":
    main()
