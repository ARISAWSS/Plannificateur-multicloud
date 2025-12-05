# Planificateur Multi-Cloud - V0

## Description
Application de planification et génération automatique d'infrastructures cloud via Terraform.

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. Installer les dépendances Python :
```bash
cd backend
pip install -r ../requirements.txt
```

2. Lancer le backend :
```bash
python app.py
```

3. Ouvrir le frontend :
Ouvrir `frontend/index.html` dans un navigateur web, ou utiliser un serveur local :
```bash
# Option 1: Python
cd frontend
python -m http.server 8000

# Option 2: Node.js
npx http-server frontend -p 8000
```

## Utilisation

1. Ouvrir l'interface web (frontend/index.html)
2. Décrire l'infrastructure souhaitée dans le champ texte
   - Exemple : "Je veux un serveur web avec une base de données sécurisée dans AWS"
3. Cliquer sur "Générer l'infrastructure"
4. Le fichier `main.tf` sera généré dans le dossier `output/`

## Fonctionnalités implémentées

✅ **Étape 1** : Frontend UI V0 (1 champ texte + 1 bouton)
✅ **Étape 2** : IA - Transformation du texte en JSON structuré
✅ **Étape 3** : Backend - Génération de main.tf à partir du JSON
✅ **Étape 4** : Règle de sécurité de base (tags requis)

## Structure du projet

```
planificateur-multicloud/
├── frontend/
│   └── index.html          # Interface utilisateur
├── backend/
│   └── app.py              # API Flask avec logique métier
├── output/                 # Fichiers Terraform générés
│   └── main.tf
├── requirements.txt        # Dépendances Python
└── README.md
```

