package com.pongechec.filter;

import jakarta.ws.rs.container.ContainerRequestContext;
import jakarta.ws.rs.container.ContainerResponseContext;
import jakarta.ws.rs.container.ContainerResponseFilter;
import jakarta.ws.rs.ext.Provider;
import java.io.IOException;

/**
 * Filtre CORS pour permettre les requêtes cross-origin depuis l'application Python.
 */
@Provider
public class CorsFilter implements ContainerResponseFilter {

    @Override
    public void filter(ContainerRequestContext requestContext,
                      ContainerResponseContext responseContext) throws IOException {
        
        // Permettre les requêtes depuis n'importe quelle origine (pour le développement)
        // En production, remplacer "*" par l'URL spécifique de votre application
        responseContext.getHeaders().add("Access-Control-Allow-Origin", "*");
        
        // Autoriser les méthodes HTTP
        responseContext.getHeaders().add("Access-Control-Allow-Methods", 
            "GET, POST, PUT, DELETE, OPTIONS, HEAD");
        
        // Autoriser les en-têtes
        responseContext.getHeaders().add("Access-Control-Allow-Headers",
            "Origin, Content-Type, Accept, Authorization");
        
        // Permettre les credentials
        responseContext.getHeaders().add("Access-Control-Allow-Credentials", "true");
        
        // Durée de validité du preflight (24h)
        responseContext.getHeaders().add("Access-Control-Max-Age", "86400");
    }
}
