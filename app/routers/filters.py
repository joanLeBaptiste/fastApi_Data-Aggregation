def appliquer_filtres_heatmap(requete_de_base, type_infrastructure, operateur_compteur_infra, nombre_infra, score_min,
                              score_max):
    """
    Applique des filtres sur la requête de la heatmap en fonction des paramètres fournis.

    - `requete_de_base` : La requête SQL de base à laquelle les filtres seront appliqués.
    - `type_infrastructure` : Le type d'infrastructure à filtrer.
    - `operateur_compteur_infra` : L'opérateur pour comparer le nombre d'infrastructures (ex: '>', '<', '=' etc.)
    - `nombre_infra` : Le nombre d'infrastructures à utiliser pour la comparaison.
    - `score_min` : Le score minimum à appliquer comme filtre (si fourni).
    - `score_max` : Le score maximum à appliquer comme filtre (si fourni).

    Retourne la requête de base avec les filtres ajoutés.
    """
    filtres = []

    # Ajouter un filtre pour le score minimum si fourni
    if score_min is not None:
        filtres.append("T.score >= :score_min")

    # Ajouter un filtre pour le score maximum si fourni
    if score_max is not None:
        filtres.append("T.score <= :score_max")

    # Ajouter un filtre pour le nombre d'infrastructures si les trois paramètres sont fournis
    if type_infrastructure and operateur_compteur_infra and nombre_infra:
        filtres.append(
            f"(SELECT COUNT(*) FROM infrastructures WHERE type_infra = :type_infra) {operateur_compteur_infra} :infra_count")

    # Construire la requête finale avec les filtres appliqués
    if filtres:
        return requete_de_base + (" WHERE " + " AND ".join(filtres))
    return requete_de_base
