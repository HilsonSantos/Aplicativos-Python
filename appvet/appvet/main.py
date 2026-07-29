"""Ponto de entrada da API FastAPI do APPVET."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from appvet.database import init_db
from appvet.routers import agenda, estoque, financeiro, funcionarios, internacao, prontuario, tutores, vendas

app = FastAPI(
    title="APPVET",
    description="API de gestão para clínica veterinária",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok"}


app.include_router(tutores.router)
app.include_router(agenda.router)
app.include_router(prontuario.router)
app.include_router(internacao.router)
app.include_router(estoque.router)
app.include_router(financeiro.router)
app.include_router(funcionarios.router)
app.include_router(vendas.router)
