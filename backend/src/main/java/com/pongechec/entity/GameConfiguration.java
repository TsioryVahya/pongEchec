package com.pongechec.entity;

import jakarta.persistence.*;
import java.io.Serializable;
import java.util.Date;

/**
 * Entité JPA représentant une configuration de jeu.
 */
@Entity
@Table(name = "game_configurations")
@NamedQueries({
    @NamedQuery(
        name = "GameConfiguration.findAll",
        query = "SELECT c FROM GameConfiguration c ORDER BY c.createdAt DESC"
    ),
    @NamedQuery(
        name = "GameConfiguration.findByName",
        query = "SELECT c FROM GameConfiguration c WHERE c.name = :name"
    )
})
public class GameConfiguration implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    // Paramètres généraux
    @Column(name = "ball_speed", nullable = false)
    private Integer ballSpeed = 3;
    
    @Column(name = "ball_damage", nullable = false)
    private Integer ballDamage = 1;
    
    @Column(name = "board_width", nullable = false)
    private Integer boardWidth = 8;
    
    @Column(name = "starting_player", nullable = false)
    private Integer startingPlayer = 1;
    
    // Vies des pièces
    @Column(name = "roi_lives", nullable = false)
    private Integer roiLives = 3;
    
    @Column(name = "reine_lives", nullable = false)
    private Integer reineLives = 2;
    
    @Column(name = "fou_lives", nullable = false)
    private Integer fouLives = 2;
    
    @Column(name = "tour_lives", nullable = false)
    private Integer tourLives = 2;
    
    @Column(name = "chevalier_lives", nullable = false)
    private Integer chevalierLives = 2;
    
    @Column(name = "pion_lives", nullable = false)
    private Integer pionLives = 1;
    
    // Points des pièces
    @Column(name = "roi_points", nullable = false)
    private Integer roiPoints = 100;
    
    @Column(name = "reine_points", nullable = false)
    private Integer reinePoints = 50;
    
    @Column(name = "fou_points", nullable = false)
    private Integer fouPoints = 30;
    
    @Column(name = "tour_points", nullable = false)
    private Integer tourPoints = 30;
    
    @Column(name = "chevalier_points", nullable = false)
    private Integer chevalierPoints = 30;
    
    @Column(name = "pion_points", nullable = false)
    private Integer pionPoints = 10;
    
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "created_at", nullable = false)
    private Date createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = new Date();
    }
    
    // Getters et Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public Integer getBallSpeed() {
        return ballSpeed;
    }
    
    public void setBallSpeed(Integer ballSpeed) {
        this.ballSpeed = ballSpeed;
    }
    
    public Integer getBallDamage() {
        return ballDamage;
    }
    
    public void setBallDamage(Integer ballDamage) {
        this.ballDamage = ballDamage;
    }
    
    public Integer getBoardWidth() {
        return boardWidth;
    }
    
    public void setBoardWidth(Integer boardWidth) {
        this.boardWidth = boardWidth;
    }
    
    public Integer getStartingPlayer() {
        return startingPlayer;
    }
    
    public void setStartingPlayer(Integer startingPlayer) {
        this.startingPlayer = startingPlayer;
    }
    
    public Integer getRoiLives() {
        return roiLives;
    }
    
    public void setRoiLives(Integer roiLives) {
        this.roiLives = roiLives;
    }
    
    public Integer getReineLives() {
        return reineLives;
    }
    
    public void setReineLives(Integer reineLives) {
        this.reineLives = reineLives;
    }
    
    public Integer getFouLives() {
        return fouLives;
    }
    
    public void setFouLives(Integer fouLives) {
        this.fouLives = fouLives;
    }
    
    public Integer getTourLives() {
        return tourLives;
    }
    
    public void setTourLives(Integer tourLives) {
        this.tourLives = tourLives;
    }
    
    public Integer getChevalierLives() {
        return chevalierLives;
    }
    
    public void setChevalierLives(Integer chevalierLives) {
        this.chevalierLives = chevalierLives;
    }
    
    public Integer getPionLives() {
        return pionLives;
    }
    
    public void setPionLives(Integer pionLives) {
        this.pionLives = pionLives;
    }
    
    public Integer getRoiPoints() {
        return roiPoints;
    }
    
    public void setRoiPoints(Integer roiPoints) {
        this.roiPoints = roiPoints;
    }
    
    public Integer getReinePoints() {
        return reinePoints;
    }
    
    public void setReinePoints(Integer reinePoints) {
        this.reinePoints = reinePoints;
    }
    
    public Integer getFouPoints() {
        return fouPoints;
    }
    
    public void setFouPoints(Integer fouPoints) {
        this.fouPoints = fouPoints;
    }
    
    public Integer getTourPoints() {
        return tourPoints;
    }
    
    public void setTourPoints(Integer tourPoints) {
        this.tourPoints = tourPoints;
    }
    
    public Integer getChevalierPoints() {
        return chevalierPoints;
    }
    
    public void setChevalierPoints(Integer chevalierPoints) {
        this.chevalierPoints = chevalierPoints;
    }
    
    public Integer getPionPoints() {
        return pionPoints;
    }
    
    public void setPionPoints(Integer pionPoints) {
        this.pionPoints = pionPoints;
    }
    
    public Date getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }
    
    @Override
    public String toString() {
        return "GameConfiguration{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", ballSpeed=" + ballSpeed +
                ", ballDamage=" + ballDamage +
                ", createdAt=" + createdAt +
                '}';
    }
}
