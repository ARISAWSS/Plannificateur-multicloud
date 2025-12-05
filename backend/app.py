from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import os

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend

# Règle de sécurité de base : Vérifier que les ressources ont des tags de sécurité
SECURITY_RULE = {
    "name": "security_tags_required",
    "description": "Toutes les ressources doivent avoir des tags de sécurité",
    "required_tags": ["Environment", "SecurityLevel"]
}

def extract_infrastructure_from_text(description):
    """
    IA simple : Transforme le texte en JSON structuré
    Cette fonction analyse le texte et extrait les informations clés
    """
    description_lower = description.lower()
    
    # Détection du fournisseur cloud
    provider = "aws"  # par défaut
    if "azure" in description_lower:
        provider = "azure"
    elif "gcp" in description_lower or "google" in description_lower:
        provider = "gcp"
    elif "openstack" in description_lower:
        provider = "openstack"
    
    # Détection des composants
    infrastructure = {
        "provider": provider,
        "servers": 0,
        "databases": 0,
        "networks": 1,  # Par défaut, on a besoin d'un réseau
        "load_balancers": 0,
        "security_groups": 1  # Par défaut, on a besoin d'un groupe de sécurité
    }
    
    # Détection des serveurs
    server_keywords = ["serveur", "server", "instance", "vm", "machine virtuelle", "ec2"]
    for keyword in server_keywords:
        if keyword in description_lower:
            # Essayer d'extraire le nombre
            numbers = re.findall(r'\d+', description)
            infrastructure["servers"] = int(numbers[0]) if numbers else 1
            break
    
    # Détection des bases de données
    db_keywords = ["base de données", "database", "db", "mysql", "postgresql", "rds"]
    for keyword in db_keywords:
        if keyword in description_lower:
            infrastructure["databases"] = 1
            break
    
    # Détection des load balancers
    lb_keywords = ["load balancer", "équilibreur", "balanceur"]
    for keyword in lb_keywords:
        if keyword in description_lower:
            infrastructure["load_balancers"] = 1
            break
    
    # Détection de la sécurité
    security_keywords = ["sécurisé", "secure", "sécurité", "security"]
    if any(keyword in description_lower for keyword in security_keywords):
        infrastructure["security_groups"] = 2  # Plus de sécurité
    
    return infrastructure

def generate_terraform_code(infrastructure_json):
    """
    Génère le code Terraform à partir du JSON
    """
    provider = infrastructure_json.get("provider", "aws")
    servers = infrastructure_json.get("servers", 0)
    databases = infrastructure_json.get("databases", 0)
    networks = infrastructure_json.get("networks", 1)
    security_groups = infrastructure_json.get("security_groups", 1)
    
    terraform_code = f'''# Infrastructure générée automatiquement
# Provider: {provider.upper()}

terraform {{
  required_version = ">= 1.0"
  
  required_providers {{
    {provider} = {{
      source  = "hashicorp/{provider}"
      version = "~> 5.0"
    }}
  }}
}}

provider "{provider}" {{
  region = "us-east-1"
  # Configurez vos credentials ici
}}

'''
    
    # Génération des réseaux
    if networks > 0:
        terraform_code += f'''# Réseau VPC
resource "{provider}_vpc" "main" {{
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {{
    Name        = "main-vpc"
    Environment = "production"
    SecurityLevel = "high"
  }}
}}

# Subnet public
resource "{provider}_subnet" "public" {{
  vpc_id                  = {provider}_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  
  tags = {{
    Name        = "public-subnet"
    Environment = "production"
    SecurityLevel = "high"
  }}
}}

'''
    
    # Génération des groupes de sécurité
    for i in range(security_groups):
        terraform_code += f'''# Groupe de sécurité {i+1}
resource "{provider}_security_group" "main_{i+1}" {{
  name        = "main-sg-{i+1}"
  description = "Groupe de sécurité principal {i+1}"
  vpc_id      = {provider}_vpc.main.id
  
  ingress {{
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  ingress {{
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  tags = {{
    Name        = "main-sg-{i+1}"
    Environment = "production"
    SecurityLevel = "high"
  }}
}}

'''
    
    # Génération des serveurs
    for i in range(servers):
        terraform_code += f'''# Serveur {i+1}
resource "{provider}_instance" "server_{i+1}" {{
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type = "t2.micro"
  subnet_id     = {provider}_subnet.public.id
  
  vpc_security_group_ids = [{provider}_security_group.main_1.id]
  
  tags = {{
    Name        = "server-{i+1}"
    Environment = "production"
    SecurityLevel = "high"
  }}
}}

'''
    
    # Génération des bases de données
    for i in range(databases):
        terraform_code += f'''# Base de données {i+1}
resource "{provider}_db_instance" "database_{i+1}" {{
  identifier     = "db-{i+1}"
  engine         = "mysql"
  engine_version = "8.0"
  instance_class = "db.t2.micro"
  allocated_storage = 20
  storage_type   = "gp2"
  
  db_name  = "mydb"
  username = "admin"
  password = "ChangeMe123!"  # À changer en production
  
  vpc_security_group_ids = [{provider}_security_group.main_1.id]
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  tags = {{
    Name        = "database-{i+1}"
    Environment = "production"
    SecurityLevel = "high"
  }}
}}

'''
    
    # Outputs
    terraform_code += '''# Outputs
output "vpc_id" {
  value = ''' + f'{provider}_vpc.main.id' + '''
}

output "public_subnet_id" {
  value = ''' + f'{provider}_subnet.public.id' + '''
}
'''
    
    return terraform_code

def apply_security_rule(terraform_code):
    """
    Applique la règle de sécurité de base
    Vérifie que toutes les ressources ont les tags requis
    """
    # Vérification simple : on s'assure que les tags sont présents
    # Dans une version plus avancée, on pourrait parser le code Terraform
    required_tags = SECURITY_RULE["required_tags"]
    
    # Vérification basique
    has_environment_tag = "Environment" in terraform_code
    has_security_level_tag = "SecurityLevel" in terraform_code
    
    if not (has_environment_tag and has_security_level_tag):
        # Ajouter un commentaire de sécurité
        terraform_code = f"#  ATTENTION: Vérifiez que toutes les ressources ont les tags requis: {', '.join(required_tags)}\n\n" + terraform_code
    
    return terraform_code

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        description = data.get('description', '')
        
        if not description:
            return jsonify({'error': 'Description manquante'}), 400
        
        # Étape 2: IA - Transformer le texte en JSON
        infrastructure_json = extract_infrastructure_from_text(description)
        
        # Étape 3: Générer le code Terraform
        terraform_code = generate_terraform_code(infrastructure_json)
        
        # Étape 4: Appliquer la règle de sécurité
        terraform_code = apply_security_rule(terraform_code)
        
        # Sauvegarder le fichier main.tf
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'main.tf'), 'w', encoding='utf-8') as f:
            f.write(terraform_code)
        
        return jsonify({
            'success': True,
            'infrastructure': infrastructure_json,
            'terraform_code': terraform_code,
            'message': 'Infrastructure générée avec succès!'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

