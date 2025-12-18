# Backend PongEchec - Guide de Déploiement

Ce guide explique comment déployer le backend Java EE avec EJB pour gérer les configurations du jeu PongEchec.

## 📋 Prérequis

### Logiciels nécessaires :
1. **Java JDK 11+** : https://adoptium.net/
2. **Maven 3.6+** : https://maven.apache.org/download.cgi
3. **PostgreSQL 13+** : https://www.postgresql.org/download/
4. **Serveur d'application** (choisir un) :
   - **WildFly 27+** (recommandé) : https://www.wildfly.org/downloads/
   - GlassFish 7+ : https://glassfish.org/download
   - Payara 6+ : https://www.payara.fish/downloads/

## 🗄️ Configuration de la Base de Données

### 1. Installer PostgreSQL

```bash
# Windows : Télécharger l'installeur depuis postgresql.org
# Lors de l'installation, notez le mot de passe du superuser 'postgres'
```

### 2. Créer la base de données

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Dans le shell PostgreSQL :
CREATE DATABASE pongechec_db;
CREATE USER pongechec_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE pongechec_db TO pongechec_user;
\q
```

### 3. Exécuter le script d'initialisation

```bash
psql -U pongechec_user -d pongechec_db -f backend/database/init.sql
```

## 🚀 Déploiement sur WildFly

### 1. Télécharger et extraire WildFly

```bash
# Télécharger WildFly 27 (ou plus récent)
# Extraire dans C:\wildfly (ou autre emplacement)
```

### 2. Configurer le driver PostgreSQL

```bash
# Télécharger le driver JDBC PostgreSQL
# https://jdbc.postgresql.org/download.html

# Copier postgresql-42.x.x.jar dans :
# C:\wildfly\standalone\deployments\
```

### 3. Configurer la DataSource

Éditer `C:\wildfly\standalone\configuration\standalone.xml` :

```xml
<!-- Ajouter dans <datasources> (ATTENTION: syntaxe WildFly 27+) -->
<datasource jndi-name="java:/PongEchecDS" 
            pool-name="PongEchecDS" 
            enabled="true" 
            use-java-context="true">
    <connection-url>jdbc:postgresql://localhost:5432/pongechec_db</connection-url>
    <driver>postgresql</driver>
    <pool>
        <min-pool-size>5</min-pool-size>
        <max-pool-size>25</max-pool-size>
    </pool>
    <security>
        <user-name>postgres</user-name>
        <password>admin</password>
    </security>
    <validation>
        <valid-connection-checker class-name="org.jboss.jca.adapters.jdbc.extensions.postgres.PostgreSQLValidConnectionChecker"/>
        <exception-sorter class-name="org.jboss.jca.adapters.jdbc.extensions.postgres.PostgreSQLExceptionSorter"/>
    </validation>
</datasource>

<!-- Ajouter dans <drivers> -->
<driver name="postgresql" module="org.postgresql">
    <driver-class>org.postgresql.Driver</driver-class>
</driver>
```

**OU** utiliser la CLI de WildFly (RECOMMANDÉ) :

```bash
# Démarrer WildFly
cd C:\wildfly\bin
standalone.bat

# Dans un autre terminal
cd C:\wildfly\bin
jboss-cli.bat --connect

# Ajouter le module PostgreSQL
module add --name=org.postgresql --resources=C:\chemin\vers\postgresql-42.x.x.jar --dependencies=javax.api,javax.transaction.api

# Ajouter le driver
/subsystem=datasources/jdbc-driver=postgresql:add(driver-name=postgresql,driver-module-name=org.postgresql,driver-class-name=org.postgresql.Driver)

# Créer la datasource
data-source add --name=PongEchecDS --jndi-name=java:/PongEchecDS --driver-name=postgresql --connection-url=jdbc:postgresql://localhost:5432/pongechec_db --user-name=pongechec_user --password=votre_mot_de_passe --enabled=true

# Tester la connexion
/subsystem=datasources/data-source=PongEchecDS:test-connection-in-pool
```

### 4. Compiler le projet

```bash
cd backend
mvn clean package
```

Cela crée `target/pongechec.war`

### 5. Déployer sur WildFly

**Option 1 : Copie manuelle**
```bash
copy target\pongechec.war C:\wildfly\standalone\deployments\
```

**Option 2 : Maven plugin** (ajouter dans pom.xml)
```xml
<plugin>
    <groupId>org.wildfly.plugins</groupId>
    <artifactId>wildfly-maven-plugin</artifactId>
    <version>4.1.0.Final</version>
</plugin>
```

```bash
mvn wildfly:deploy
```

### 6. Vérifier le déploiement

```bash
# L'application est accessible sur :
# http://localhost:8080/pongechec/api/configurations

# Tester avec curl :
curl http://localhost:8080/pongechec/api/configurations
```

## 🐍 Configuration côté Python

### 1. Installer les dépendances

```bash
cd ..  # Retour à la racine du projet
pip install -r requirements.txt
```

### 2. Tester la connexion

Créer un fichier `test_backend.py` :

```python
from paddle_chess_game.services.config_service import ConfigurationService

# Créer le service
service = ConfigurationService("http://localhost:8080/pongechec/api")

# Tester la connexion
if service.test_connection():
    print("✓ Connexion au backend réussie!")
    
    # Récupérer les configurations
    configs = service.get_all_configurations()
    print(f"Configurations disponibles : {len(configs)}")
    
    for config in configs:
        print(f"  - {config.get('name', 'Sans nom')}")
else:
    print("✗ Impossible de se connecter au backend")
```

```bash
python test_backend.py
```

## 🔧 Dépannage

### Erreur : "Cannot find datasource"
- Vérifier que la datasource est configurée dans standalone.xml
- Redémarrer WildFly

### Erreur : "Connection refused"
- Vérifier que PostgreSQL est démarré
- Vérifier les credentials dans la datasource

### Erreur CORS
- Vérifier que le CorsFilter est bien déployé
- Vérifier les logs WildFly

### Voir les logs WildFly
```bash
tail -f C:\wildfly\standalone\log\server.log
```

## 📚 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/configurations` | Liste toutes les configurations |
| GET | `/api/configurations/{id}` | Récupère une configuration |
| POST | `/api/configurations` | Crée une configuration |
| PUT | `/api/configurations/{id}` | Met à jour une configuration |
| DELETE | `/api/configurations/{id}` | Supprime une configuration |

### Exemple de requête POST (curl)

```bash
curl -X POST http://localhost:8080/pongechec/api/configurations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ma Config",
    "ballSpeed": 5,
    "ballDamage": 2,
    "boardWidth": 8,
    "startingPlayer": 1,
    "roiLives": 3,
    "reineLives": 2,
    "fouLives": 2,
    "tourLives": 2,
    "chevalierLives": 2,
    "pionLives": 1,
    "roiPoints": 100,
    "reinePoints": 50,
    "fouPoints": 30,
    "tourPoints": 30,
    "chevalierPoints": 30,
    "pionPoints": 10
  }'
```

## 🎯 Structure du Projet

```
backend/
├── src/
│   └── main/
│       ├── java/
│       │   └── com/pongechec/
│       │       ├── entity/
│       │       │   └── GameConfiguration.java    # Entité JPA
│       │       ├── service/
│       │       │   └── GameConfigurationService.java  # EJB
│       │       ├── rest/
│       │       │   ├── RestApplication.java      # Config JAX-RS
│       │       │   └── GameConfigurationResource.java  # REST API
│       │       └── filter/
│       │           └── CorsFilter.java           # CORS
│       └── resources/
│           └── META-INF/
│               └── persistence.xml               # Config JPA
├── database/
│   └── init.sql                                  # Script SQL
└── pom.xml                                       # Maven
```

## ✅ Checklist de déploiement

- [ ] PostgreSQL installé et démarré
- [ ] Base de données créée
- [ ] Script init.sql exécuté
- [ ] WildFly téléchargé et extrait
- [ ] Driver PostgreSQL copié
- [ ] DataSource configurée
- [ ] Projet compilé (`mvn clean package`)
- [ ] WAR déployé sur WildFly
- [ ] API accessible (test curl)
- [ ] Python peut se connecter

## 🎓 Ressources

- [Documentation WildFly](https://docs.wildfly.org/)
- [Jakarta EE Tutorial](https://eclipse-ee4j.github.io/jakartaee-tutorial/)
- [JPA avec Hibernate](https://hibernate.org/orm/documentation/)
