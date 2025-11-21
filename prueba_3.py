import stable_whisper
import pysubs2
from pysubs2 import SSAEvent, SSAStyle

# --- Configuración ---
AUDIO_FILE = "audio.mp3"
MODEL_SIZE = "large"

print("Cargando el modelo...")
model = stable_whisper.load_model(MODEL_SIZE)

print(f"Transcribiendo '{AUDIO_FILE}' para formato de estilo alterno...")
result = model.transcribe(AUDIO_FILE, language='es', regroup=False)

# --- Creación del archivo de subtítulos ---
subs = pysubs2.SSAFile()

# 1. CONFIGURAR LA INFORMACIÓN DEL SCRIPT (CABECERA)
subs.info['ScriptType'] = 'v4.00+'
subs.info['Title'] = 'Generated Subtitles'
subs.info['PlayResX'] = 720
subs.info['PlayResY'] = 1280
subs.info['WrapStyle'] = 0

# 2. DEFINIR LOS ESTILOS
# Estilo 'Default'
subs.styles["Default"] = SSAStyle(
    fontname="Proxima Nova", fontsize=40,
    primarycolor=pysubs2.Color(241, 241, 241),
    secondarycolor=pysubs2.Color(241, 241, 241),
    outlinecolor=pysubs2.Color(29, 29, 29),
    backcolor=pysubs2.Color(241, 241, 241, 255), # Último valor es alpha (transparencia)
    bold=True, borderstyle=2, outline=2, shadow=2,
    alignment=pysubs2.Alignment.BOTTOM_CENTER,
    marginl=120, marginr=120, marginv=450, encoding=1
)

# Estilo 'Alternate'
subs.styles["Alternate"] = SSAStyle(
    fontname="Proxima Nova", fontsize=40,
    primarycolor=pysubs2.Color(29, 29, 29),
    secondarycolor=pysubs2.Color(29, 29, 29),
    outlinecolor=pysubs2.Color(241, 241, 241),
    backcolor=pysubs2.Color(241, 241, 241),
    bold=True, borderstyle=3, outline=2, shadow=2,
    alignment=pysubs2.Alignment.BOTTOM_CENTER,
    marginl=120, marginr=120, marginv=450, encoding=1
)

print("Generando eventos de diálogo...")

# 3. GENERAR LOS EVENTOS (LAS LÍNEAS DE DIÁLOGO)
for segment in result.segments:
    # Obtener una lista con el texto de todas las palabras de la frase
    all_words_in_segment = [word.word.strip() for word in segment.words]

    # Iterar por cada palabra para crear una línea de diálogo específica para ella
    for i, word in enumerate(segment.words):
        # Tomar los tiempos de inicio y fin de la palabra actual
        word_start_ms = int(word.start * 1000)
        word_end_ms = int(word.end * 1000)
        
        # Crear una copia de la lista de palabras para modificarla
        temp_words = list(all_words_in_segment)
        
        # En la copia, envolver la palabra actual con los tags de estilo
        temp_words[i] = f"{{\\rAlternate}}{temp_words[i]}{{\\r}}"
        
        # Unir la lista modificada para formar la línea de texto completa
        line_text = " ".join(temp_words)
        
        # Crear el evento de diálogo que dura solo lo que dura la palabra
        event = SSAEvent(
            start=word_start_ms,
            end=word_end_ms,
            text=line_text,
            style="Default" # El estilo base de la línea es Default
        )
        subs.append(event)

# Guarda el archivo final
output_ass_file = AUDIO_FILE.replace(".mp3", "_alternate_style_karaoke.ass")
subs.save(output_ass_file)

print(f"\n✅ ¡Listo! Archivo generado con el nuevo formato: {output_ass_file}")