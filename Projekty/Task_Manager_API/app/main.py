from fastapi import FastAPI

# TODO: Zaimportuj Base i engine z database.py
# TODO: Zaimportuj routery

app = FastAPI(
    title="Task Manager API",
    description="REST API do zarzadzania zadaniami - projekt portfolio",
    version="1.0.0",
)


# TODO: Utworz tabele przy starcie
# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)


# TODO: Dolacz routery
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(projects.router, prefix="/projects", tags=["Projects"])
# app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
# app.include_router(tags.router, prefix="/tags", tags=["Tags"])
# app.include_router(stats.router, prefix="/stats", tags=["Stats"])


@app.get("/")
def root():
    return {"message": "Task Manager API", "docs": "/docs"}
