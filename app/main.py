from fastapi import FastAPI

# Objek aplikasi — uvicorn akan mencari variabel bernama "app" ini
app = FastAPI(title="todo-api")


@app.get("/")
def root() -> dict[str, str]:
    # Endpoint sederhana untuk membuktikan app hidup dan bisa diakses
    return {"message": "hello from todo-api"}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    # Health check: SENGAJA tidak mengecek dependency apa pun (DB, API lain).
    # Hanya menjawab "proses ini hidup dan bisa melayani request".
    return {"status": "ok"}
