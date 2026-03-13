# 📄 API Generador de Documentos Word

API construida con **FastAPI + python-docx** que recibe texto y devuelve un archivo `.docx` descargable.

---

## 🚀 Cómo ejecutar la API

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Iniciar el servidor
```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### 3. Ver documentación interactiva
Abre en tu navegador: `http://localhost:8000/docs`
(FastAPI genera esta página automáticamente — puedes probar la API desde ahí)

---

## 📡 Cómo usar la API (para el compañero de frontend)

### Endpoint principal

| Campo | Valor |
|---|---|
| **Método** | `POST` |
| **URL** | `http://localhost:8000/generate-doc` |
| **Body** | JSON |
| **Respuesta** | Archivo `.docx` descargable |

### Body (JSON)
```json
{
  "titulo": "Mi Documento",
  "contenido": "Este es el contenido.\nEste es otro párrafo."
}
```

> 💡 Usa `\n` para separar párrafos dentro del contenido.

---

## 💻 Ejemplo en JavaScript (fetch)

```javascript
async function descargarDocumento(titulo, contenido) {
  const response = await fetch("http://localhost:8000/generate-doc", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titulo, contenido })
  });

  if (!response.ok) {
    const error = await response.json();
    console.error("Error:", error.detail);
    return;
  }

  // Convertir respuesta a blob y forzar descarga
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${titulo}.docx`;
  a.click();
  window.URL.revokeObjectURL(url);
}

// Uso:
descargarDocumento("Reporte Enero", "Línea 1\nLínea 2\nLínea 3");
```

---

## ⚠️ Errores posibles

| Código | Motivo |
|---|---|
| `400` | El título o contenido están vacíos |
| `422` | El JSON enviado tiene campos incorrectos o faltantes |
| `500` | Error interno del servidor |

---

## 📁 Estructura del proyecto

```
mi-api/
├── main.py          # App principal, rutas de la API
├── generator.py     # Lógica para crear el .docx
├── models.py        # Estructura del JSON que recibe la API
├── requirements.txt # Dependencias
└── README.md        # Este archivo
```
