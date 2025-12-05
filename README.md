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

 Étape 1 : Frontend UI V0 (1 champ texte + 1 bouton)
 Étape 2 : IA - Transformation du texte en JSON structuré
 Étape 3 : Backend - Génération de main.tf à partir du JSON
Étape 4 : Règle de sécurité de base (tags requis)

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

## Références

### Backend (Python/Flask)

- **Flask - Application et routes**
  - https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
  - https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask

- **Flask-CORS** - `CORS(app)`
  - https://flask-cors.readthedocs.io/en/latest/api.html#flask_cors.CORS
  - https://flask-cors.readthedocs.io/en/latest/

- **Flask request.json**
  - https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.json

- **Flask jsonify**
  - https://flask.palletsprojects.com/en/3.0.x/api/#flask.json.jsonify

- **Python regex `re.findall()`**
  - https://docs.python.org/3/library/re.html#re.findall
  - https://docs.python.org/3/library/re.html#regular-expression-syntax

- **Python os.path.join()**
  - https://docs.python.org/3/library/os.path.html#os.path.join

### Terraform Resources

- **Terraform AWS VPC** - `aws_vpc`
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc

- **Terraform AWS Subnet** - `aws_subnet`
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet

- **Terraform AWS Security Group** - `aws_security_group`
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group
  - Ingress/Egress rules : https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group#ingress

- **Terraform AWS Instance (EC2)** - `aws_instance`
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance

- **Terraform AWS DB Instance (RDS)** - `aws_db_instance`
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance

- **Terraform Provider Configuration** - `provider "aws"`
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration

- **Terraform Outputs**
  - https://www.terraform.io/docs/language/values/outputs.html

- **Terraform Required Providers**
  - https://www.terraform.io/docs/language/providers/requirements.html

### Frontend (HTML/CSS/JavaScript)

- **Fetch API** - `fetch('http://localhost:5000/generate')`
  - https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  - https://developer.mozilla.org/en-US/docs/Web/API/fetch

- **CSS Flexbox** - `display: flex; justify-content: center; align-items: center;`
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox

- **CSS Linear Gradient** - `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
  - https://developer.mozilla.org/en-US/docs/Web/CSS/gradient/linear-gradient

- **CSS Box Shadow** - `box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3)`
  - https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow

- **JavaScript async/await** - `async function generateInfrastructure()`
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function

- **JavaScript JSON.stringify()**
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify

- **JavaScript addEventListener**
  - https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener

### Concepts AWS/Terraform

- **CIDR Blocks** - `"10.0.0.0/16"`, `"10.0.1.0/24"`
  - https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html

- **Security Group Rules (Ports 80, 443)**
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules-reference.html

- **AWS AMI** - `"ami-0c55b159cbfafe1f0"`
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html

- **AWS Instance Types** - `"t2.micro"`
  - https://aws.amazon.com/ec2/instance-types/

- **RDS Engine Types** - `engine = "mysql"`
  - https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html

