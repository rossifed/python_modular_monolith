This is an example of a modular monolith architecture in python. 
environement isin .venv folder
launcing configuration is oin .vscode launch.json

setting up teh env
1 in the root folder type poetry init
2 add the needed package ex. fastapi, uvicorn, pydantic
3 type poetry config virtualenvs.in-project true to set the environement in the .venv of the project
3 poetry install, this will setup the environment and install the depenenvies
4 if you are in VS code select the interpreter ctrl+shift+P an create new environement and select the .venv environement that we just created
5 to laucn the app uvicorn bootstrapper.bootstrapper:app --reload --app-dir src

The bootstrap is the entrypoint of the app.
shared containts the shared code of the modular monolith infrastructure (modules loading, communication, events, etc)
each modules are in the modules folder to add a module  addd that in the root pypoetry.toml
[tool.poetry]
packages = [
    { include = "bootstrapper", from = "src" },
    { include = "shared", from = "src" },
    { include = "my_module", from = "src/modules" }
]

each project must have its own __init__.py file


