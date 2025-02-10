from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# ✅ Incluir las rutas
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Microservicio UpdateProduct corriendo 🚀"}
