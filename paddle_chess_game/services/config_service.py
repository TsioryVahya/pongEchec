"""
Service pour gérer les configurations via l'API REST du serveur Java EE.
"""
import requests
import json
from typing import Dict, List, Optional


class ConfigurationService:
    """Service pour communiquer avec le backend Java EE via REST API."""
    
    def __init__(self, base_url: str = "http://localhost:8080/pongechec/api"):
       
        self.base_url = base_url
        self.endpoint = f"{base_url}/configurations"
    
    def get_all_configurations(self) -> List[Dict]:
        """
        Récupère toutes les configurations depuis le serveur.
        
        Returns:
            Liste des configurations ou liste vide en cas d'erreur
        """
        try:
            response = requests.get(self.endpoint, timeout=5)
            response.raise_for_status()
            configs = response.json()
            # Convertir chaque config du format serveur vers Python
            return [self._convert_from_server_format(c) for c in configs]
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des configurations: {e}")
            return []
    
    def get_configuration(self, config_id: int) -> Optional[Dict]:
        """
        Récupère une configuration spécifique par son ID.
        
        Args:
            config_id: ID de la configuration
            
        Returns:
            Configuration ou None en cas d'erreur
        """
        try:
            response = requests.get(f"{self.endpoint}/{config_id}", timeout=5)
            response.raise_for_status()
            server_config = response.json()
            return self._convert_from_server_format(server_config)
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération de la configuration {config_id}: {e}")
            return None
    
    def save_configuration(self, config: Dict, name: str = "Configuration Standard") -> Optional[Dict]:
        """
        Sauvegarde la configuration. Si une configuration existe déjà, elle est mise à jour.
        Sinon, une nouvelle est créée.
        
        Args:
            config: Dictionnaire de configuration (format Python)
            name: Nom de la configuration (défaut: "Configuration Standard")
            
        Returns:
            Configuration sauvegardée ou None en cas d'erreur
        """
        try:
            # Vérifier s'il existe déjà une configuration
            existing_configs = self.get_all_configurations()
            
            if existing_configs:
                # Mise à jour de la première configuration trouvée
                existing_id = existing_configs[0].get('id')
                if existing_id:
                    print(f"Mise à jour de la configuration existante (ID: {existing_id})")
                    return self.update_configuration(existing_id, config, name)
            
            # Création d'une nouvelle configuration si aucune n'existe
            print("Création d'une nouvelle configuration")
            server_format = self._convert_to_server_format(config)
            server_format['name'] = name
            
            response = requests.post(
                self.endpoint,
                json=server_format,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
            saved_config = response.json()
            return self._convert_from_server_format(saved_config)
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return None
    
    def update_configuration(self, config_id: int, config: Dict, name: str = None) -> Optional[Dict]:
        """
        Met à jour une configuration existante.
        
        Args:
            config_id: ID de la configuration à mettre à jour
            config: Nouvelle configuration
            name: Nouveau nom (optionnel)
            
        Returns:
            Configuration mise à jour ou None en cas d'erreur
        """
        try:
            server_format = self._convert_to_server_format(config)
            if name:
                server_format['name'] = name
            
            response = requests.put(
                f"{self.endpoint}/{config_id}",
                json=server_format,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
            updated_config = response.json()
            return self._convert_from_server_format(updated_config)
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return None
    
    def delete_configuration(self, config_id: int) -> bool:
        """
        Supprime une configuration.
        
        Args:
            config_id: ID de la configuration à supprimer
            
        Returns:
            True si succès, False sinon
        """
        try:
            response = requests.delete(f"{self.endpoint}/{config_id}", timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test la connexion au serveur.
        
        Returns:
            True si le serveur est accessible, False sinon
        """
        try:
            response = requests.get(self.endpoint, timeout=2)
            return response.status_code in [200, 404]  # 404 OK si pas de configs
        except:
            return False
    
    def _convert_to_server_format(self, config: Dict) -> Dict:
        """
        Convertit le format Python (snake_case) vers le format serveur Java (camelCase).
        
        Args:
            config: Configuration au format Python
            
        Returns:
            Configuration au format serveur
        """
        return {
            'ballSpeed': config.get('ball_speed', 3),
            'ballDamage': config.get('ball_damage', 1),
            'boardWidth': config.get('board_width', 8),
            'startingPlayer': config.get('starting_player', 1),
            'roiLives': config.get('roi_lives', 3),
            'reineLives': config.get('reine_lives', 2),
            'fouLives': config.get('fou_lives', 2),
            'tourLives': config.get('tour_lives', 2),
            'chevalierLives': config.get('chevalier_lives', 2),
            'pionLives': config.get('pion_lives', 1),
            'roiPoints': config.get('roi_points', 100),
            'reinePoints': config.get('reine_points', 50),
            'fouPoints': config.get('fou_points', 30),
            'tourPoints': config.get('tour_points', 30),
            'chevalierPoints': config.get('chevalier_points', 30),
            'pionPoints': config.get('pion_points', 10),
            'specialBarMax': config.get('special_bar_max', 10),
            'specialBallDamage': config.get('special_ball_damage', 3)
        }
    
    def _convert_from_server_format(self, server_config: Dict) -> Dict:
        """
        Convertit le format serveur Java (camelCase) vers le format Python (snake_case).
        
        Args:
            server_config: Configuration au format serveur
            
        Returns:
            Configuration au format Python
        """
        config = {
            'ball_speed': server_config.get('ballSpeed', 3),
            'ball_damage': server_config.get('ballDamage', 1),
            'board_width': server_config.get('boardWidth', 8),
            'starting_player': server_config.get('startingPlayer', 1),
            'roi_lives': server_config.get('roiLives', 3),
            'reine_lives': server_config.get('reineLives', 2),
            'fou_lives': server_config.get('fouLives', 2),
            'tour_lives': server_config.get('tourLives', 2),
            'chevalier_lives': server_config.get('chevalierLives', 2),
            'pion_lives': server_config.get('pionLives', 1),
            'roi_points': server_config.get('roiPoints', 100),
            'reine_points': server_config.get('reinePoints', 50),
            'fou_points': server_config.get('fouPoints', 30),
            'tour_points': server_config.get('tourPoints', 30),
            'chevalier_points': server_config.get('chevalierPoints', 30),
            'pion_points': server_config.get('pionPoints', 10),
            'special_bar_max': server_config.get('specialBarMax', 10),
            'special_ball_damage': server_config.get('specialBallDamage', 3)
        }
        
        # Ajouter les métadonnées si présentes
        if 'id' in server_config:
            config['id'] = server_config['id']
        if 'name' in server_config:
            config['name'] = server_config['name']
        if 'createdAt' in server_config:
            config['created_at'] = server_config['createdAt']
            
        return config
