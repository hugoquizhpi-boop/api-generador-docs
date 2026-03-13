from pydantic import BaseModel

class DocumentoRequest(BaseModel):
    titulo: str
    contenido: str

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Mi Documento",
                "contenido": "Este es el contenido del documento. Puede ser tan largo como necesites."
            }
        }
