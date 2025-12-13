package com.pongechec.rest;

import com.pongechec.entity.GameConfiguration;
import com.pongechec.service.GameConfigurationService;
import jakarta.ejb.EJB;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.util.List;

/**
 * REST API pour gérer les configurations de jeu.
 * 
 * Endpoints disponibles :
 * - GET    /api/configurations       : Liste toutes les configurations
 * - GET    /api/configurations/{id}  : Récupère une configuration
 * - POST   /api/configurations       : Crée une nouvelle configuration
 * - PUT    /api/configurations/{id}  : Met à jour une configuration
 * - DELETE /api/configurations/{id}  : Supprime une configuration
 */
@Path("/configurations")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class GameConfigurationResource {
    
    @EJB
    private GameConfigurationService configService;
    
    /**
     * GET /api/configurations
     * Récupère toutes les configurations.
     */
    @GET
    public Response getAllConfigurations() {
        try {
            List<GameConfiguration> configs = configService.getAllConfigurations();
            return Response.ok(configs).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("{\"error\": \"" + e.getMessage() + "\"}")
                    .build();
        }
    }
    
    /**
     * GET /api/configurations/{id}
     * Récupère une configuration spécifique.
     */
    @GET
    @Path("/{id}")
    public Response getConfiguration(@PathParam("id") Long id) {
        try {
            GameConfiguration config = configService.getConfiguration(id);
            if (config == null) {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity("{\"error\": \"Configuration not found\"}")
                        .build();
            }
            return Response.ok(config).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("{\"error\": \"" + e.getMessage() + "\"}")
                    .build();
        }
    }
    
    /**
     * POST /api/configurations
     * Crée une nouvelle configuration.
     */
    @POST
    public Response createConfiguration(GameConfiguration config) {
        try {
            // Validation basique
            if (config.getName() == null || config.getName().trim().isEmpty()) {
                return Response.status(Response.Status.BAD_REQUEST)
                        .entity("{\"error\": \"Name is required\"}")
                        .build();
            }
            
            GameConfiguration created = configService.createConfiguration(config);
            return Response.status(Response.Status.CREATED).entity(created).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("{\"error\": \"" + e.getMessage() + "\"}")
                    .build();
        }
    }
    
    /**
     * PUT /api/configurations/{id}
     * Met à jour une configuration existante.
     */
    @PUT
    @Path("/{id}")
    public Response updateConfiguration(@PathParam("id") Long id, GameConfiguration config) {
        try {
            GameConfiguration existing = configService.getConfiguration(id);
            if (existing == null) {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity("{\"error\": \"Configuration not found\"}")
                        .build();
            }
            
            config.setId(id);
            config.setCreatedAt(existing.getCreatedAt()); // Conserver la date de création
            GameConfiguration updated = configService.updateConfiguration(config);
            return Response.ok(updated).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("{\"error\": \"" + e.getMessage() + "\"}")
                    .build();
        }
    }
    
    /**
     * DELETE /api/configurations/{id}
     * Supprime une configuration.
     */
    @DELETE
    @Path("/{id}")
    public Response deleteConfiguration(@PathParam("id") Long id) {
        try {
            GameConfiguration config = configService.getConfiguration(id);
            if (config == null) {
                return Response.status(Response.Status.NOT_FOUND)
                        .entity("{\"error\": \"Configuration not found\"}")
                        .build();
            }
            
            configService.deleteConfiguration(id);
            return Response.noContent().build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity("{\"error\": \"" + e.getMessage() + "\"}")
                    .build();
        }
    }
}
