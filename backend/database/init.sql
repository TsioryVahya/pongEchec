-- Script SQL pour initialiser la base de données PongEchec
-- PostgreSQL

-- Créer la base de données (exécuter en tant que superuser)
-- CREATE DATABASE pongechec_db;
-- GRANT ALL PRIVILEGES ON DATABASE pongechec_db TO votre_user;

-- Se connecter à la base de données pongechec_db
\c pongechec_db;

-- Supprimer la table si elle existe (pour un nouveau départ)
DROP TABLE IF EXISTS game_configurations;

-- Créer la table game_configurations
CREATE TABLE game_configurations (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    
    -- Paramètres généraux
    ball_speed INTEGER NOT NULL DEFAULT 3,
    ball_damage INTEGER NOT NULL DEFAULT 1,
    board_width INTEGER NOT NULL DEFAULT 8,
    starting_player INTEGER NOT NULL DEFAULT 1,
    
    -- Vies des pièces
    roi_lives INTEGER NOT NULL DEFAULT 3,
    reine_lives INTEGER NOT NULL DEFAULT 2,
    fou_lives INTEGER NOT NULL DEFAULT 2,
    tour_lives INTEGER NOT NULL DEFAULT 2,
    chevalier_lives INTEGER NOT NULL DEFAULT 2,
    pion_lives INTEGER NOT NULL DEFAULT 1,
    
    -- Points des pièces
    roi_points INTEGER NOT NULL DEFAULT 100,
    reine_points INTEGER NOT NULL DEFAULT 50,
    fou_points INTEGER NOT NULL DEFAULT 30,
    tour_points INTEGER NOT NULL DEFAULT 30,
    chevalier_points INTEGER NOT NULL DEFAULT 30,
    pion_points INTEGER NOT NULL DEFAULT 10,
    
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Ajouter un index sur le nom
CREATE INDEX idx_config_name ON game_configurations(name);

-- Insérer quelques configurations par défaut
INSERT INTO game_configurations (
    name, ball_speed, ball_damage, board_width, starting_player,
    roi_lives, reine_lives, fou_lives, tour_lives, chevalier_lives, pion_lives,
    roi_points, reine_points, fou_points, tour_points, chevalier_points, pion_points
) VALUES 
    ('Configuration Standard', 3, 1, 8, 1, 3, 2, 2, 2, 2, 1, 100, 50, 30, 30, 30, 10);

-- Afficher les configurations
SELECT * FROM game_configurations;
