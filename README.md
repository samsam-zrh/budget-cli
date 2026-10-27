# Budget CLI

J’ai fait cet outil pour suivre mes dépenses dans le terminal. Tout est enregistré dans un CSV, avec un total par catégorie et un filtre par mois.

Python 3.10 minimum, sans dépendance.

## Utilisation

```sh
python3 budget.py add 12,50 courses "Marché du samedi"
python3 budget.py list
python3 budget.py list --month 2026-10
python3 budget.py summary --month 2026-10
```

Le fichier est dans `~/.budget-cli/expenses.csv`. Pour en choisir un autre, ajouter `--file ./expenses.csv` avant la commande.

## Tests

```sh
python3 -m unittest -v
```

Pas de synchronisation ni de suppression de dépense pour le moment.
