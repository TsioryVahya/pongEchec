package com.pongechec.service;

import com.pongechec.entity.GameConfiguration;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.util.List;

/**
 * Session Bean Stateless (EJB) pour gérer la logique métier des configurations.
 */
@Stateless
public class GameConfigurationService {
    
    @PersistenceContext(unitName = "PongEchecPU")
    private EntityManager em;
    
    /**
     * Crée une nouvelle configuration.
     */
    public GameConfiguration createConfiguration(GameConfiguration config) {
        em.persist(config);
        em.flush();
        return config;
    }
    
    /**
     * Récupère une configuration par son ID.
     */
    public GameConfiguration getConfiguration(Long id) {
        return em.find(GameConfiguration.class, id);
    }
    
    /**
     * Récupère toutes les configurations.
     */
    public List<GameConfiguration> getAllConfigurations() {
        return em.createNamedQuery("GameConfiguration.findAll", GameConfiguration.class)
                 .getResultList();
    }
    
    /**
     * Met à jour une configuration existante.
     */
    public GameConfiguration updateConfiguration(GameConfiguration config) {
        return em.merge(config);
    }
    
    /**
     * Supprime une configuration.
     */
    public void deleteConfiguration(Long id) {
        GameConfiguration config = em.find(GameConfiguration.class, id);
        if (config != null) {
            em.remove(config);
        }
    }
    
    /**
     * Recherche une configuration par nom.
     */
    public GameConfiguration findByName(String name) {
        List<GameConfiguration> results = em.createNamedQuery("GameConfiguration.findByName", GameConfiguration.class)
                .setParameter("name", name)
                .getResultList();
        return results.isEmpty() ? null : results.get(0);
    }
}
