# Budget CLI

Un petit gestionnaire de dépenses dans le terminal, écrit uniquement avec la bibliothèque standard de Python.

Je l'ai créé pour pratiquer :

- la lecture et l'écriture d'un fichier CSV ;
- les arguments en ligne de commande avec `argparse` ;
- les calculs monétaires avec `Decimal` ;
- les tests unitaires avec `unittest`.

## Utilisation

Python 3.10 ou plus récent suffit. Aucune dépendance n'est nécessaire.

```bash
# Ajouter une dépense
python3 budget.py add 12,50 courses "Marché du samedi"

# Afficher toutes les dépenses
python3 budget.py list

# Filtrer un mois
python3 budget.py list --month 2026-10

# Voir le total et la répartition par catégorie
python3 budget.py summary --month 2026-10
```

Les données sont enregistrées par défaut dans `~/.budget-cli/expenses.csv`. Pour tester avec un autre fichier :

```bash
python3 budget.py --file ./expenses.csv add 4.20 transport "Ticket de bus"
```

## Tests

```bash
python3 -m unittest -v
```

## Limites actuelles

Le projet reste volontairement simple : pas de compte utilisateur, pas de synchronisation et pas d'interface graphique. Une prochaine amélioration possible serait de permettre la suppression d'une dépense saisie par erreur.
