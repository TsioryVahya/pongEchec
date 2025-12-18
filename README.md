# 🎮 PongEchec - Jeu Hybride Python + Java EE

Un jeu de **Pong** combiné avec des **Échecs**, développé en Python (Pygame) avec un backend Java EE pour la gestion des configurations.

## 📋 Description

PongEchec est un jeu innovant qui mélange :
- 🏓 **Pong** : Mécanique de rebond de balle
- ♟️ **Échecs** : Pièces d'échecs servant d'obstacles
- 🎯 **Stratégie** : Détruire le roi adverse pour gagner

### Fonctionnalités principales :
- ✅ Mode **Local** (2 joueurs sur le même PC)
- ✅ Mode **Multijoueur en réseau** (Client-Serveur)
- ✅ **Configuration personnalisable** (vitesse, dégâts, vies, points)
- ✅ **Sauvegarde/Chargement** de parties (JSON)
- ✅ **Backend Java EE** avec EJB pour stocker les configurations
- ✅ **Barre de navigation** avec score en temps réel
- ✅ **Système de pause** (Espace)
- ✅ **Tir puissant** vers le roi (Touche P)
- ✅ **Système de visée** pour le service de balle

## 🏗️ Architecture

```
┌─────────────────────────┐
│   Jeu Python (Pygame)   │
│   - Interface graphique │
│   - Logique de jeu      │
│   - Multijoueur réseau  │
└───────────┬─────────────┘
            │ HTTP/REST
            │ (JSON)
┌───────────▼─────────────┐
│   Backend Java EE       │
│   - EJB (Stateless)     │
│   - JAX-RS (REST API)   │
│   - JPA/Hibernate       │
└───────────┬─────────────┘
            │ JDBC
┌───────────▼─────────────┐
│   PostgreSQL            │
│   - Configurations      │
└─────────────────────────┘
```

## 🚀 Installation Rapide

### Prérequis

#### Pour le jeu (Python)
- **Python 3.8+** : https://www.python.org/downloads/
- **pip** (inclus avec Python)

#### Pour le backend (Java EE) - Optionnel
- **Java JDK 11+** : https://adoptium.net/
- **Maven 3.6+** : https://maven.apache.org/
- **PostgreSQL 13+** : https://www.postgresql.org/
- **WildFly 27+** : https://www.wildfly.org/downloads/

### Installation du jeu

```bash
# Cloner le projet
git clone https://github.com/votre-repo/pongEchec.git
cd pongEchec

# Installer les dépendances Python
pip install -r requirements.txt

# Lancer le jeu
python -m paddle_chess_game.main
```

### Installation du backend (optionnel)

Voir le guide détaillé dans [`backend/README.md`](backend/README.md)

```bash
# 1. Créer la base de données PostgreSQL
psql -U postgres
CREATE DATABASE pongechec_db;
CREATE USER pongechec_user WITH PASSWORD 'votre_password';
GRANT ALL PRIVILEGES ON DATABASE pongechec_db TO pongechec_user;

# 2. Exécuter le script d'initialisation
psql -U pongechec_user -d pongechec_db -f backend/database/init.sql

# 3. Configurer WildFly (voir backend/README.md)

# 4. Déployer l'application
deploy.bat
```

## 🎮 Contrôles

### En jeu

#### Joueur 1 (Haut)
- **Flèches Gauche/Droite** : Déplacer le paddle
- **W/S** ou **Haut/Bas** : Viser lors du service
- **Espace** : Servir la balle / Pause
- **P** : Tir puissant vers le roi adverse

#### Joueur 2 (Bas)
- **Flèches Gauche/Droite** : Déplacer le paddle
- **Haut/Bas** : Viser lors du service
- **Espace** : Servir la balle / Pause
- **P** : Tir puissant vers le roi adverse

### Générales
- **R** : Redémarrer la partie
- **ESC** : Quitter

## 📁 Structure du Projet

```
pongEchec/
├── paddle_chess_game/          # Code du jeu Python
│   ├── objects/                # Objets du jeu (Balle, Paddle, Pièces)
│   ├── network/                # Code réseau (Client/Serveur)
│   ├── services/               # Services (API Backend)
│   ├── game.py                 # Logique principale
│   ├── main.py                 # Point d'entrée
│   ├── config_menu.py          # Menu de configuration
│   ├── network_menu.py         # Menu réseau
│   └── settings.py             # Paramètres
├── backend/                    # Backend Java EE
│   ├── src/main/java/          # Code Java
│   │   └── com/pongechec/
│   │       ├── entity/         # Entités JPA
│   │       ├── service/        # EJB (logique métier)
│   │       ├── rest/           # API REST (JAX-RS)
│   │       └── filter/         # Filtres (CORS)
│   ├── src/main/resources/     # Ressources
│   │   └── META-INF/
│   │       └── persistence.xml # Config JPA
│   ├── database/               # Scripts SQL
│   ├── config/                 # Fichiers de configuration
│   ├── pom.xml                 # Maven
│   └── README.md               # Guide de déploiement
├── test_backend.py             # Tests du backend
├── deploy.bat                  # Script de déploiement
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

## 📖 Guides

- [Guide de déploiement Backend](backend/README.md)
- [Test du Backend](test_backend.py)

## 🔧 Configuration

### Menu de configuration du jeu

Au lancement, vous pouvez configurer :
- Vitesse de la balle (1-20)
- Dégâts de la balle (1-10)
- Largeur de l'échiquier (2, 4, 6, 8)
- Joueur qui débute (1 ou 2)
- Vies des pièces (1-10 par type)
- Points des pièces (0-1000 par type)

### Backend (configurations persistantes)

Si le backend est déployé, les configurations peuvent être :
- Sauvegardées dans PostgreSQL
- Partagées entre plusieurs joueurs
- Récupérées via l'API REST

## 🌐 API REST (Backend)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/configurations` | Liste des configurations |
| GET | `/api/configurations/{id}` | Une configuration |
| POST | `/api/configurations` | Créer une configuration |
| PUT | `/api/configurations/{id}` | Modifier une configuration |
| DELETE | `/api/configurations/{id}` | Supprimer une configuration |

### Exemple de requête

```bash
# Lister les configurations
curl http://localhost:8080/pongechec/api/configurations

# Créer une configuration
curl -X POST http://localhost:8080/pongechec/api/configurations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ma Config",
    "ballSpeed": 5,
    "ballDamage": 2,
    "roiLives": 5
  }'
```

## 🐛 Dépannage

### Le jeu ne démarre pas
```bash
# Vérifier les dépendances
pip install -r requirements.txt

# Lancer avec verbose
python -m paddle_chess_game.main
```

### Erreur réseau multijoueur
- Vérifier le pare-feu Windows
- Autoriser Python sur le port 5555
- Vérifier que l'IP est correcte

### Backend inaccessible
- Vérifier que WildFly est démarré
- Vérifier que PostgreSQL est démarré
- Consulter les logs : `WILDFLY_HOME/standalone/log/server.log`

## 🎓 Technologies Utilisées

### Frontend (Jeu)
- **Python 3.x**
- **Pygame-CE** : Interface graphique et boucle de jeu
- **Pickle / JSON** : Sérialisation
- **Socket** : Réseau multijoueur
- **Requests** : Communication HTTP avec backend

### Backend
- **Java 11+**
- **Jakarta EE 9** : Framework entreprise
- **EJB 3.x** : Session Beans (Stateless)
- **JPA 3.0 / Hibernate** : Persistance
- **JAX-RS** : API REST
- **PostgreSQL** : Base de données
- **WildFly 27** : Serveur d'application
- **Maven** : Build

## 👥 Auteurs

Projet développé dans le cadre d'un cours sur les architectures distribuées.

## 📄 Licence

Ce projet est sous licence à définir.

## 🎯 Améliorations futures

- [ ] Interface web (React/Vue.js)
- [ ] Authentification JWT
- [ ] Matchmaking en ligne
- [ ] Replay de parties
- [ ] IA pour jouer seul
- [ ] Classement des joueurs
- [ ] Statistiques de jeu

---

**Bon jeu ! 🎮**
