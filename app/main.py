from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware  # ✅ Importar CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# ✅ Incluir las rutas
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Microservicio UpdateProduct corriendo 🚀"}
