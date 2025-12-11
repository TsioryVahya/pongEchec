# Paddle + Chess (Python, Pygame)

Un jeu original mêlant Pong (paddles + balle) et des pièces d'échecs statiques qui servent d'obstacles avec des points de vie. Si le roi adverse perd toutes ses vies, vous gagnez .Enjoy!

## Lancer le jeu

1. Créez un environnement Python 3.10+ (recommandé).
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancez :

```bash
py -m paddle_chess_game.main
```

## Contrôles

- Joueur 1 (haut) : A / D (gauche / droite)
- Joueur 2 (bas) : Flèche Gauche / Flèche Droite
- R : Rejouer si la partie est terminée
- ESC : Quitter

## Structure

```
paddle_chess_game/
  main.py
  game.py
  settings.py
  objects/
    __init__.py
    paddle.py
    ball.py
    chess_piece.py
```

## Notes

- Les collisions balle/pièces infligent 1 dégât et provoquent un rebond suivant l'axe d'impact.
- Chaque type de pièce a un nombre de vies configurable dans `paddle_chess_game/settings.py`.
- Condition de victoire : si un "roi" tombe à 0 PV, l'autre joueur gagne.
