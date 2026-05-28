import streamlit as st
import os
import re
import shutil
import subprocess
import json

# Verificar disponibilidad de ffmpeg local (bin/ffmpeg) y global en el sistema
BIN_DIR = os.path.abspath("bin")
LOCAL_FFMPEG_PATH = os.path.join(BIN_DIR, "ffmpeg")

FFMPEG_GLOBAL = shutil.which("ffmpeg")
FFMPEG_LOCAL_EXISTS = os.path.exists(LOCAL_FFMPEG_PATH) and os.access(LOCAL_FFMPEG_PATH, os.X_OK)

FFMPEG_AVAILABLE = (FFMPEG_GLOBAL is not None) or FFMPEG_LOCAL_EXISTS
FFMPEG_PATH = FFMPEG_GLOBAL if FFMPEG_GLOBAL is not None else (LOCAL_FFMPEG_PATH if FFMPEG_LOCAL_EXISTS else None)

# Verificar disponibilidad de yt-dlp local (bin/yt-dlp) y global en el sistema
LOCAL_YT_DLP_PATH = os.path.join(BIN_DIR, "yt-dlp")
YT_DLP_GLOBAL = shutil.which("yt-dlp")
YT_DLP_LOCAL_EXISTS = os.path.exists(LOCAL_YT_DLP_PATH) and os.access(LOCAL_YT_DLP_PATH, os.X_OK)

YT_DLP_AVAILABLE = (YT_DLP_GLOBAL is not None) or YT_DLP_LOCAL_EXISTS
YT_DLP_PATH = YT_DLP_GLOBAL if YT_DLP_GLOBAL is not None else (LOCAL_YT_DLP_PATH if YT_DLP_LOCAL_EXISTS else None)


# 1. Configuración de la página con estética limpia y favicon de descarga
st.set_page_config(
    page_title="Tubex - YouTube Downloader",
    page_icon="📥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Inyección de elementos HTML para el fondo brillante (Aura Glow Background)
st.markdown("""
<div class="glow-bg">
    <div class="glow-circle-1"></div>
    <div class="glow-circle-2"></div>
</div>
""", unsafe_allow_html=True)

# 3. CSS Personalizado completo para emular al 100% el diseño del Mockup Premium
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Ocultar elementos web nativos de Streamlit para un aspecto 100% de aplicación */
[data-testid="stHeader"] {
    display: none !important;
}
#MainMenu {
    visibility: hidden !important;
    display: none !important;
}
footer {
    visibility: hidden !important;
    display: none !important;
}
[data-testid="stDecoration"] {
    display: none !important;
}

/* Asegurar base negra premium directamente en el documento para evitar destellos o fondos blancos */
html, body {
    background-color: #07080c !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    overflow-x: hidden !important;
}

/* Hacer completamente transparente el fondo por defecto de los contenedores de Streamlit */
[data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .stApp {
    background-color: transparent !important;
    background-image: none !important;
    overflow-x: hidden !important;
    border: none !important;
}

/* Centrar el chasis de la aplicación en pantalla vertical y horizontalmente */
[data-testid="stAppViewContainer"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 100vh !important;
    padding: 20px !important;
    box-sizing: border-box !important;
}

/* Ajustar el bloque de visualización de Streamlit para alinearse en el centro */
[data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Aplicar fuente premium Outfit a toda la aplicación */
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Outfit', sans-serif !important;
    color: #e2e4ec !important;
}

/* Efectos de fondo brillante (Aura Glow) fijos detrás del contenedor */
.glow-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -2;
    overflow: hidden;
    background-color: #07080c !important; /* Base negra premium */
}
.glow-circle-1 {
    position: absolute;
    top: 15%;
    left: -8%;
    width: 480px;
    height: 480px;
    background: radial-gradient(circle, rgba(255, 30, 30, 0.20) 0%, rgba(255, 30, 30, 0) 70%) !important;
    border-radius: 50% !important;
    filter: blur(90px) !important;
    opacity: 0.8 !important;
}
.glow-circle-2 {
    position: absolute;
    top: -8%;
    right: -2%;
    width: 420px;
    height: 420px;
    background: radial-gradient(circle, rgba(162, 101, 255, 0.16) 0%, rgba(162, 101, 255, 0) 70%) !important;
    border-radius: 50% !important;
    filter: blur(80px) !important;
    opacity: 0.8 !important;
}

/* Contenedor principal estilo Tarjeta Flotante (Glassmorphism de alta fidelidad, SIN BORDES) */
.block-container {
    max-width: 530px !important;
    width: 100% !important;
    background: rgba(7, 8, 12, 0.93) !important; /* Cristal oscuro denso de alta gama */
    backdrop-filter: blur(40px) !important;
    -webkit-backdrop-filter: blur(40px) !important;
    border: none !important; /* ELIMINAR CUALQUIER BORDE */
    border-width: 0px !important;
    border-radius: 28px !important;
    padding: 38px 30px !important;
    margin: 0 !important;
    box-shadow: 0 35px 90px rgba(0, 0, 0, 0.9) !important; /* Sombra espectacular profunda */
    box-sizing: border-box !important;
}

/* Ajustar espaciado entre widgets verticales de Streamlit */
[data-testid="stVerticalBlock"] {
    gap: 15px !important;
}

/* Cabecera de la Aplicación */
.mockup-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    margin-bottom: 25px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    padding-bottom: 18px !important;
}
.header-left {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
}
.header-icon-box {
    background: rgba(255, 255, 255, 0.06) !important;
    padding: 7px 11px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.header-text {
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.04em !important;
}
.header-right-icon {
    display: flex !important;
}

/* Anular TODOS los bordes, fondos claros y sombras nativos de Streamlit */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlock"] > div,
[data-testid="element-container"],
[data-testid="stAppViewBlockContainer"],
.stVerticalBlock,
.element-container {
    border: none !important;
    border-width: 0px !important;
    box-shadow: none !important;
    background: transparent !important;
    background-color: transparent !important;
}

/* Etiquetas estilizadas para los inputs */
.label-styled {
    color: rgba(255, 255, 255, 0.65) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 8px !important;
}

/* Caja de entrada URL en NEGRO SÓLIDO (Cero bordes y texto blanco garantizado en Light/Dark Mode) */
div[data-testid="stTextInput"],
div[data-testid="stTextInput"] * {
    border: none !important;
    border-width: 0px !important;
    outline: none !important;
}

div[data-testid="stTextInput"] div[role="presentation"],
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="base-input"],
div[data-testid="stTextInput"] [data-baseweb="input"] > div,
div[data-testid="stTextInput"] input {
    background-color: #000000 !important; /* Forzar negro absoluto */
    background: #000000 !important;
    color: #ffffff !important; /* Forzar texto blanco brillante */
    border: none !important;
    border-width: 0px !important;
    border-radius: 14px !important;
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.85) !important;
}

div[data-testid="stTextInput"] input {
    box-shadow: none !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
    height: 48px !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(255, 255, 255, 0.35) !important;
}

div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {
    box-shadow: 0 0 15px rgba(255, 30, 30, 0.45), inset 0 2px 5px rgba(0, 0, 0, 0.85) !important; /* Resplandor interactivo */
}

/* Ocultar círculo selector nativo de Streamlit */
div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* Barra Segmentada de Formatos (Segmented Control en negro sólido sin bordes claros) */
div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    background: #000000 !important;
    border: none !important;
    border-width: 0px !important;
    border-radius: 16px !important;
    padding: 5px !important;
    margin-top: 18px !important;
    margin-bottom: 5px !important;
    gap: 5px !important;
    width: 100% !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.8) !important;
}

div[role="radiogroup"] label {
    flex: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    padding: 10px 16px !important;
    border-radius: 12px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: none !important;
    border-width: 0px !important;
    margin: 0 !important;
    background: transparent !important;
}

div[role="radiogroup"] label div {
    background-color: transparent !important;
    border: none !important;
    border-width: 0px !important;
}

div[role="radiogroup"] label p {
    color: rgba(255, 255, 255, 0.45) !important; /* Pestaña inactiva */
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    transition: all 0.25s ease !important;
    margin: 0 !important;
    padding: 0 !important;
}

div[role="radiogroup"] label:hover p {
    color: rgba(255, 255, 255, 0.85) !important;
}

/* Estado activo de la barra segmentada con degradado neón interactivo */
div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #FF1E1E 0%, #7E38B7 100%) !important;
    box-shadow: 0 4px 15px rgba(255, 30, 30, 0.3) !important;
}

div[role="radiogroup"] label:has(input:checked) p {
    color: #ffffff !important;
    font-weight: 600 !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

/* Botón principal "Procesar" con degradado neón dinámico */
div.stButton > button {
    background: linear-gradient(90deg, #FF1E1E 0%, #7E38B7 100%) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 13px 25px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    border-radius: 14px !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(255, 30, 30, 0.35) !important;
    margin-top: 15px !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(126, 56, 183, 0.5) !important;
    filter: brightness(1.08);
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Botón de descarga final con degradado azul neón a cian */
div.stDownloadButton > button {
    background: linear-gradient(135deg, #1C67E3 0%, #00C6FF 100%) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 14px 25px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    border-radius: 14px !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(28, 103, 227, 0.4) !important;
    margin-top: 15px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

div.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 198, 255, 0.5) !important;
    filter: brightness(1.1);
}

div.stDownloadButton > button:active {
    transform: translateY(0px) !important;
}

/* Imágenes con esquinas redondeadas y borde elegante */
img {
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Diseño responsivo de nivel de aplicación para celulares */
@media (max-width: 768px) {
    [data-testid="stAppViewContainer"] {
        padding: 12px !important;
    }
    .block-container {
        padding: 28px 20px !important;
        border-radius: 22px !important;
        background: rgba(15, 17, 26, 0.96) !important; /* Mayor opacidad en móvil para máxima claridad */
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6) !important;
    }
}

/* Tarjeta informativa de advertencia de FFmpeg */
.ffmpeg-warning {
    background: rgba(255, 165, 0, 0.08) !important;
    border: 1px solid rgba(255, 165, 0, 0.15) !important;
    border-radius: 14px !important;
    padding: 15px 18px !important;
    margin-top: 15px !important;
    font-size: 0.88rem !important;
    color: #ffd27f !important;
    line-height: 1.45 !important;
}

.code-install {
    display: inline-block !important;
    background: #000000 !important;
    padding: 3px 8px !important;
    border-radius: 6px !important;
    color: #FF1E1E !important;
    font-family: monospace !important;
    margin-top: 6px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border: 1px solid rgba(255, 30, 30, 0.15) !important;
}
</style>
""", unsafe_allow_html=True)

# 4. Directorio de descargas temporales y lógica de limpieza automática
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def clear_downloads():
    """Limpia todos los archivos dentro del directorio de descargas para optimizar espacio."""
    if os.path.exists(DOWNLOAD_DIR):
        for file in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                pass

def reset_state():
    """Limpia el estado de sesión si la URL cambia, ocultando el botón anterior."""
    if "downloaded_file" in st.session_state:
        del st.session_state["downloaded_file"]

def install_local_ffmpeg():
    """Descarga e instala localmente FFmpeg para macOS Apple Silicon (arm64)."""
    import urllib.request
    import zipfile
    
    bin_dir = os.path.abspath("bin")
    os.makedirs(bin_dir, exist_ok=True)
    zip_path = os.path.join(bin_dir, "ffmpeg.zip")
    ffmpeg_path = os.path.join(bin_dir, "ffmpeg")
    
    # URL estable notarizada oficial de Martin Riedl para Apple Silicon
    url = "https://ffmpeg.martin-riedl.de/download/macos/arm64/1778761665_8.1.1/ffmpeg.zip"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(bin_dir)
            
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        if os.path.exists(ffmpeg_path):
            os.chmod(ffmpeg_path, 0o755)
            return True, "¡FFmpeg se ha instalado localmente con éxito! Calidad de descarga desbloqueada."
        else:
            return False, "Error: No se encontró el ejecutable ffmpeg tras la extracción."
    except Exception as e:
        return False, f"Error durante la descarga o extracción de FFmpeg: {str(e)}"

def install_local_ytdlp():
    """Descarga e instala localmente el ejecutable yt-dlp para macOS o Linux."""
    import urllib.request
    import platform
    
    bin_dir = os.path.abspath("bin")
    os.makedirs(bin_dir, exist_ok=True)
    ytdlp_path = os.path.join(bin_dir, "yt-dlp")
    
    # Detectar el sistema operativo para descargar la versión correcta
    system = platform.system().lower()
    if "darwin" in system:
        url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
    else:
        # Fallback a Linux binary (Streamlit Cloud, Hugging Face, Render son Linux)
        url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as response, open(ytdlp_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        if os.path.exists(ytdlp_path):
            os.chmod(ytdlp_path, 0o755)
            return True, "¡yt-dlp se ha instalado localmente con éxito! Motor de descarga desbloqueado."
        else:
            return False, "Error: No se encontró el ejecutable yt-dlp tras la descarga."
    except Exception as e:
        return False, f"Error durante la descarga de yt-dlp: {str(e)}"

# Inicializar estados de sesión para retener la descarga dinámica
if "downloaded_file" not in st.session_state:
    st.session_state.downloaded_file = None


# 5. Renderizar Cabecera idéntica al Mockup con iconos SVG de alta fidelidad
SVG_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: white; display: block;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>'
SVG_ICON_MUTED = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display: block;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>'

st.markdown(f"""
<div class="mockup-header">
    <div class="header-left">
        <div class="header-icon-box">{SVG_ICON}</div>
        <span class="header-text">Tubex</span>
    </div>
    <span class="header-right-icon">{SVG_ICON_MUTED}</span>
</div>
""", unsafe_allow_html=True)

def get_safe_filename(title):
    """Sanitiza el título del video para evitar problemas con caracteres especiales."""
    safe = re.sub(r'[\\/*?:"<>|]', "", title)
    return safe[:100]

# 6. Contenedor principal de Entradas (Tarjeta Interna completamente sin bordes)
with st.container():
    # Label manual estilizada para el input de texto
    st.markdown('<p class="label-styled">Ingresa el enlace de YouTube aquí</p>', unsafe_allow_html=True)
    
    url_input = st.text_input(
        "url_label_hidden",
        placeholder="https://www.youtube.com/watch?v=...",
        on_change=reset_state,
        key="url_field",
        label_visibility="collapsed"  # Ocultamos la etiqueta nativa para usar nuestra clase estilizada
    )
    
    # Selector de formato horizontal estilizado como pestañas
    format_choice = st.radio(
        "format_label_hidden",
        options=["Video (MP4 - Alta Calidad)", "Audio (MP3)"],
        horizontal=True,
        label_visibility="collapsed"  # Ocultamos etiqueta nativa para diseño de barra de pestañas limpio
    )
    
    # Render de estado o tarjeta de instalación de FFmpeg y yt-dlp
    if FFMPEG_AVAILABLE and YT_DLP_AVAILABLE:
        st.markdown(f'<div style="text-align: center; font-size: 0.82rem; color: rgba(0, 230, 115, 0.7); margin-top: 10px; margin-bottom: 5px; font-weight: 500;">🟢 Motor de Descarga y FFmpeg Activos: Descargas en Ultra Alta Calidad (1080p, 4K) y MP3 habilitadas.</div>', unsafe_allow_html=True)
    else:
        if not YT_DLP_AVAILABLE:
            st.markdown("""
            <div class="ffmpeg-warning" style="background: rgba(255, 30, 30, 0.08) !important; border: 1px solid rgba(255, 30, 30, 0.15) !important; color: #ff8080 !important;">
                <strong>⚠️ Motor de Descarga (yt-dlp) Faltante</strong><br>
                Se requiere el motor de descarga ejecutable para extraer videos y audio de YouTube.<br>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⚡ Instalar Motor de Descarga en 1 Clic", use_container_width=True):
                with st.spinner("⏳ Descargando e instalando el motor yt-dlp (esto tomará unos segundos)..."):
                    success, msg = install_local_ytdlp()
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
        if not FFMPEG_AVAILABLE:
            st.markdown("""
            <div class="ffmpeg-warning">
                <strong>⚠️ Descargas de Alta Calidad Deshabilitadas</strong><br>
                YouTube sirve video de alta definición (1080p/4K) y audio por separado. Se requiere <strong>FFmpeg</strong> para fusionarlos.<br>
                <div style="margin-top: 6px; font-size: 0.8rem; opacity: 0.85;">Por ahora, las descargas se limitarán a calidad estándar (720p/360p).</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⚡ Instalar FFmpeg en esta App (1 Clic)", use_container_width=True):
                with st.spinner("⏳ Descargando e instalando FFmpeg localmente (esto tomará unos segundos)..."):
                    success, msg = install_local_ffmpeg()
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                    
    # Motor de descargas encapsulado utilizando el binario standalone yt-dlp
    def process_youtube_download(url, format_type):
        clear_downloads()
        
        if not YT_DLP_PATH:
            raise Exception("No se encontró el motor yt-dlp ejecutable. Por favor, instálalo usando el botón de la interfaz.")

        # Detección de cookies.txt para evadir bloqueos 403 en centros de datos
        COOKIES_FILE = "cookies.txt"
        COOKIES_PATH = os.path.join(os.path.abspath("."), COOKIES_FILE)
        COOKIES_PRESENT = os.path.exists(COOKIES_PATH)

        # 1. Obtener metadatos en formato JSON (excluyendo android/ios para evitar 403 Forbidden y SABR en la nube)
        info_cmd = [
            YT_DLP_PATH,
            "-J",
            "--no-playlist",
            "--extractor-args", "youtube:player_client=default,-android,-ios",
        ]
        if COOKIES_PRESENT:
            info_cmd += ["--cookies", COOKIES_PATH]
        info_cmd += [url]
        
        info_result = subprocess.run(info_cmd, capture_output=True, text=True)
        if info_result.returncode != 0:
            error_stderr = info_result.stderr if info_result.stderr else ""
            if "Unsupported URL" in error_stderr or "not a valid URL" in error_stderr:
                raise Exception("La URL ingresada no es válida. Por favor, verifica el enlace de YouTube.")
            elif "Private video" in error_stderr:
                raise Exception("Este video es privado o no está disponible.")
            elif "Sign in to confirm your age" in error_stderr:
                raise Exception("Este video requiere confirmación de edad y no permite extracciones automáticas.")
            else:
                raise Exception(f"Error al extraer información del video de YouTube: {error_stderr}")
                
        try:
            info = json.loads(info_result.stdout)
        except Exception as e:
            raise Exception(f"Error al procesar los metadatos del video: {str(e)}")
            
        title = info.get('title', 'archivo_descargado')
        safe_title = get_safe_filename(title)
        thumbnail = info.get('thumbnail')
        duration_sec = info.get('duration', 0)
        
        # Convertir duración a MM:SS
        minutes = duration_sec // 60
        seconds = duration_sec % 60
        duration_str = f"{minutes}:{seconds:02d}"
        
        # 2. Configurar argumentos de descarga (excluyendo android/ios para evitar 403 Forbidden y SABR en la nube)
        download_cmd = [
            YT_DLP_PATH,
            "--no-playlist",
            "--extractor-args", "youtube:player_client=default,-android,-ios",
        ]
        if COOKIES_PRESENT:
            download_cmd += ["--cookies", COOKIES_PATH]
        download_cmd += [url]
        
        # Directorio de descargas temporales
        base_outtmpl = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        download_cmd += ["-o", base_outtmpl]
        
        # Agregar ffmpeg location si está disponible
        if FFMPEG_AVAILABLE and FFMPEG_PATH:
            download_cmd += ["--ffmpeg-location", FFMPEG_PATH]
            
        if format_type == "Audio (MP3)":
            if FFMPEG_AVAILABLE:
                # Descargar el mejor audio, extraerlo a MP3 a 320kbps
                download_cmd += [
                    "-f", "bestaudio/best",
                    "-x",
                    "--audio-format", "mp3",
                    "--audio-quality", "320K"
                ]
            else:
                # Fallback sin ffmpeg: descargar audio nativo
                download_cmd += ["-f", "bestaudio/best"]
        else:
            if FFMPEG_AVAILABLE:
                # Descargar máxima calidad absoluta (1080p, 4K, 8K) y fusionar con ffmpeg en mp4
                download_cmd += [
                    "-f", "bestvideo+bestaudio/best",
                    "--merge-output-format", "mp4"
                ]
            else:
                # Fallback sin ffmpeg: descargar archivo pre-combinado (típicamente 720p/360p)
                download_cmd += ["-f", "best[ext=mp4]/best"]
                
        # 3. Ejecutar descarga
        download_result = subprocess.run(download_cmd, capture_output=True, text=True)
        if download_result.returncode != 0:
            error_stderr = download_result.stderr if download_result.stderr else ""
            if "ffmpeg" in error_stderr.lower() and not FFMPEG_AVAILABLE:
                raise Exception("FFmpeg no está configurado en tu servidor o máquina. Haz clic en el botón de instalación local en la interfaz para habilitar descargas en alta calidad y conversión de MP3.")
            else:
                raise Exception(f"Error al descargar el archivo: {error_stderr}")
                
        # 4. Ubicar archivo físico descargado
        downloaded_files = os.listdir(DOWNLOAD_DIR)
        if not downloaded_files:
            raise Exception("El archivo no se encontró en el directorio de descargas.")
            
        filename = downloaded_files[0]
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        
        # Determinar extensión y tipo mime reales
        if format_type == "Audio (MP3)":
            expected_mp3 = os.path.splitext(file_path)[0] + ".mp3"
            if os.path.exists(expected_mp3):
                file_path = expected_mp3
                filename = os.path.basename(expected_mp3)
                extension = "mp3"
                mime = "audio/mpeg"
            else:
                extension = os.path.splitext(filename)[1].replace(".", "")
                if extension == "m4a":
                    mime = "audio/mp4"
                elif extension in ["ogg", "opus"]:
                    mime = "audio/ogg"
                else:
                    mime = "audio/webm"
        else:
            extension = os.path.splitext(filename)[1].replace(".", "")
            if extension == "mp4":
                mime = "video/mp4"
            else:
                mime = f"video/{extension}"
                
        # 5. Cargar a memoria
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            
        # Borrar archivo físico de inmediato
        try:
            os.unlink(file_path)
        except:
            pass
            
        # Almacenar en st.session_state
        st.session_state.downloaded_file = {
            "data": file_bytes,
            "filename": f"{safe_title}.{extension}",
            "mime": mime,
            "title": title,
            "size_mb": round(len(file_bytes) / (1024 * 1024), 2),
            "thumbnail": thumbnail,
            "duration_str": duration_str
        }

    # Render del botón principal "Procesar" dentro de la misma tarjeta
    if url_input:
        if "youtube.com" in url_input.lower() or "youtu.be" in url_input.lower():
            if st.button("Procesar", use_container_width=True):
                with st.spinner("⚡ Procesando..."):
                    try:
                        process_youtube_download(url_input, format_choice)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("💡 Por favor, ingresa una URL válida de YouTube.")

# 7. Renderizado dinámico de la tarjeta de descarga (Tarjeta inferior completamente sin bordes)
if st.session_state.downloaded_file is not None:
    file_info = st.session_state.downloaded_file
    
    # Contenedor inferior sin bordes nativos grises/blancos
    with st.container():
        col1, col2 = st.columns([1, 2], gap="medium")
        
        with col1:
            # Mostrar la miniatura con esquinas redondeadas
            if file_info.get("thumbnail"):
                st.image(file_info["thumbnail"], use_container_width=True)
            else:
                st.markdown('<div style="background:rgba(255,255,255,0.05); border-radius:12px; height:90px; display:flex; align-items:center; justify-content:center;">🎬</div>', unsafe_allow_html=True)
                
        with col2:
            # Título y metadatos formateados exactamente como en el Mockup
            st.markdown(f'<div style="font-weight: 600; color: #ffffff; font-size: 1.1rem; line-height: 1.25; margin-bottom: 6px;">{file_info["title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #8b8f9e; font-size: 0.9rem; font-weight: 400;">{file_info["duration_str"]} &nbsp;•&nbsp; {file_info["size_mb"]} MB</div>', unsafe_allow_html=True)
            
        # Botón final de descarga en azul neón brillante
        st.download_button(
            label="📥 Descargar archivo a tu dispositivo",
            data=file_info["data"],
            file_name=file_info["filename"],
            mime=file_info["mime"],
            use_container_width=True
        )
        
        st.toast("¡El archivo se ha procesado con éxito!", icon="✨")

