# Projet de gestion des assets des employées

Application web FastAPI utilisant le modèle MVC et une base de données SQLite.

## Installation

1. Créer un environnement virtuel Python
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\activate
   ```
2. Installer les dépendances
   ```bash
   pip install -r requirements.txt
   ```

## Exécution

```bash
uvicorn app.main:app --reload
```

## Fonctionnalités

- Liste des employées
- Création / modification / suppression d'employées
- Gestion des assets rattachés aux employées
- Interface HTML simple avec Jinja2
