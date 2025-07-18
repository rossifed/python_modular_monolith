from fastapi import FastAPI
from shared.infrastructure import load_modular_infrastructure


def create_app() -> FastAPI:
    app = FastAPI(
        title="Modular Monolith API",
        description="A modular FastAPI monolith",
        version="0.1.0",
    )

    # Chargement dynamique des modules via entry points
    load_modular_infrastructure(app)

    return app


app = create_app()
