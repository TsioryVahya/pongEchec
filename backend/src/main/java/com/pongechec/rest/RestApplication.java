package com.pongechec.rest;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

/**
 * Configuration de l'application JAX-RS.
 * Définit le chemin de base de l'API : /api
 */
@ApplicationPath("/api")
public class RestApplication extends Application {
    // La classe peut rester vide, JAX-RS scannera automatiquement les ressources
}
