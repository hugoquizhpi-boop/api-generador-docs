import os
from fastapi import FastAPI, HTTPException, Security
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
 
from models import DocumentoRequest
from generator import generar_documento
 
# ── Cargar variables del archivo .env ─────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("API_KEY")
 
# ── Seguridad: esperar el header "x-api-key" en cada petición ─────────────────
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
 
def verificar_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida o no proporcionada.")
    return key
 
# ── Crear la app ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="API Generador de Documentos",
    description="Recibe texto y devuelve un archivo .docx descargable.",
    version="1.0.0"
)
 
# ── CORS ──────────────────────────────────────────────────────────────────────
# Esto permite que el frontend de tu compañero pueda llamar a la API
# desde el navegador sin errores de seguridad.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # En producción, cambia "*" por la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
# ── Ruta de prueba ────────────────────────────────────────────────────────────
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando ✅", "version": "1.0.0"}
 
 
# ── Ruta principal ────────────────────────────────────────────────────────────
@app.post("/generate-doc")
def generar_doc(datos: DocumentoRequest, api_key: str = Security(verificar_api_key)):
    """
    Recibe un título y contenido, y devuelve un archivo .docx descargable.
 
    - **titulo**: Título principal del documento
    - **contenido**: Cuerpo del documento (acepta saltos de línea con \\n)
    """
 
    # Validaciones básicas
    if not datos.titulo.strip():
        raise HTTPException(status_code=400, detail="El título no puede estar vacío.")
    if not datos.contenido.strip():
        raise HTTPException(status_code=400, detail="El contenido no puede estar vacío.")
 
    # Generar el documento en memoria
    buffer = generar_documento(datos.titulo, datos.contenido)
 
    # Nombre del archivo: título sin espacios + .docx
    nombre_archivo = datos.titulo.strip().replace(" ", "_") + ".docx"
 
    # Devolver el archivo como descarga
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"}
    )