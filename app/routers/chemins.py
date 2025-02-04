from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import text
import json
import os
from fastapi.responses import HTMLResponse, JSONResponse


# Couleurs pour les différents types d'infrastructures
couleurs_infrastructures = {
    "Médecin": "red",
    "Pharmacie": "green",
    "Pompiers": "blue",
    "Bibliothèque": "yellow",
    "Santé": "purple"
}

router = APIRouter()


@router.get("/get_center_color/{id_zone}")
def obtenir_couleur_centre(id_zone: str, db: Session = Depends(get_db)):
    try:
        query = """
            SELECT AVG(distance_m)
            FROM chemins
            WHERE id_zone = :id_zone
        """
        result = db.execute(text(query), {'id_zone': id_zone}).fetchone()

        if not result or result[0] is None:
            raise HTTPException(status_code=404, detail="Aucune distance trouvée pour cette zone")

        avg_distance = result[0] / 1000  # Convertir en km

        max_distance = 20  # Limite à 20 km
        if avg_distance > max_distance:
            color = 'red'
        else:
            normalized_distance = avg_distance / max_distance
            color = interpoler_couleur(normalized_distance)

        return JSONResponse(content={"id_zone": id_zone, "color": color})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")


def interpoler_couleur(value):
    """
    Retourne une couleur en fonction de la valeur normalisée [0..1]
    Dégradé simple entre le vert (#00FF00) et le rouge (#FF0000).
    """
    red = int(255 * value)
    green = int(255 * (1 - value))
    return f"rgb({red}, {green}, 0)"


@router.get("/get_infrastructure_by_paths/{id_zone}")
def obtenir_infrastructures_par_chemins(id_zone: str, db: Session = Depends(get_db)):
    try:
        query = """
            SELECT infra.id_infra, infra.nom, infra.type_infra, infra.latitude, infra.longitude
            FROM infrastructures infra
            JOIN chemins c ON c.id_infra = infra.id_infra
            WHERE c.id_zone = :id_zone
        """
        result = db.execute(text(query), {'id_zone': id_zone}).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="Aucune infrastructure trouvée pour cette zone")

        infrastructures = [
            {
                "id_infra": row[0],
                "nom": row[1],
                "type_infra": row[2],
                "latitude": row[3],
                "longitude": row[4]
            }
            for row in result
        ]

        return JSONResponse(content=infrastructures)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")


@router.get("", response_class=HTMLResponse)
def page_heatmap(db: Session = Depends(get_db)):
    """
    Affiche une carte interactive avec les chemins et infrastructures associées aux centres.
    """
    try:
        print("Accès à la route /heatmap_with_scores")  # Log de débogage

        # Charger le fichier GeoJSON des chemins
        geojson_file_path = '../asset/GeoJson_chemin_voiture.geojson'
        try:
            print("Accès à la route /heatmap_with_scores")  # Log de débogage

            # Chemin interne vers le fichier GeoJSON
            geojson_file_path = os.path.join("app", "asset", "GeoJson_chemin_voiture.geojson")

            # Lire le fichier GeoJSON directement depuis le disque
            with open(geojson_file_path, "r", encoding="utf-8") as f:
                geojson_data = json.load(f)
            print(f"Fichier GeoJSON chargé depuis {geojson_file_path}")  # Log de succès

        except FileNotFoundError as e:
            print(f"Fichier introuvable : {geojson_file_path}")  # Log de l'erreur
            raise HTTPException(status_code=404, detail=f"Fichier introuvable : {geojson_file_path}")

        except Exception as e:
            print(f"Erreur lors du chargement du fichier GeoJSON : {str(e)}")  # Log de l'erreur
            raise HTTPException(status_code=500, detail=f"Erreur lors du chargement du fichier GeoJSON : {str(e)}")

        # Récupérer les données des centres
        query = """
            SELECT id_zone, latitude_centre, longitude_centre FROM angers_cadrillage
        """
        zones = db.execute(text(query)).fetchall()
        print("Données des zones récupérées de la base de données")  # Log de succès

        zones_list = [
            {
                "id_zone": zone[0],
                "latitude_centre": zone[1],
                "longitude_centre": zone[2]
            }
            for zone in zones
        ]

        # Générer le HTML
        print("Génération du HTML pour la carte")  # Log de débogage
        map_html = generer_html_carte(zones_list, geojson_data)
        return HTMLResponse(content=map_html)

    except Exception as e:
        print(f"Erreur dans la fonction page_heatmap: {str(e)}")  # Log de l'erreur
        error_html = f"""
        <html>
            <head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            </head>
            <body>
                <h1 style="color:red;">Erreur !</h1>
                <p>{str(e)}</p>
            </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)


def generer_html_carte(zones_list, geojson_data):
    """
    Génère le contenu HTML pour la carte Leaflet.
    On ajoute un header, un footer, une info-box (explications), et on garde la logique existante.
    """
    content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chemins et Infrastructures</title>

        <!-- Leaflet CSS -->
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <!-- Leaflet JS -->
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

        <!-- Google Font (Poppins) -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="stylesheet"
              href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap">

        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }}

            body {{
                background: #f9f9f9;
                color: #333;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }}

            header {{
                width: 100%;
                background: #444;
                color: #fff;
                padding: 1rem 2rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            header h1 {{
                font-weight: 600;
                font-size: 1.5rem;
            }}

            footer {{
                background: #444;
                color: #fff;
                text-align: center;
                padding: 0.5rem 2rem;
                font-size: 0.8rem;
            }}

            #map {{
                flex-grow: 1;
                width: 100%;
                min-height: 600px;
            }}

            /* Info-box en haut à droite */
            .info-box {{
                position: absolute;
                top: 80px;
                right: 20px;
                background: rgba(255,255,255,0.95);
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                z-index: 1000;
                max-width: 300px;
                font-size: 0.9rem;
            }}
            .info-box h3 {{
                margin-bottom: 0.5rem;
                font-size: 1rem;
            }}
            .info-box p {{
                line-height: 1.4;
                margin-bottom: 0.5rem;
            }}

            .legend {{
                background-color: white;
                padding: 10px;
                font-size: 12px;
                line-height: 1.5;
                position: absolute;
                bottom: 20px;
                left: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}

            .gradient-legend-container {{
                background-color: white;
                padding: 10px;
                position: absolute;
                bottom: 250px;
                left: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                z-index: 1000;
                display: flex;
                flex-direction: row;
            }}

            .gradient-labels {{
                padding-left: 10px;
                font-size: 12px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}

            .gradient-legend {{
                background: linear-gradient(to top, rgb(0, 255, 0), rgb(255, 165, 0), rgb(255, 0, 0));
                height: 150px;
                width: 18px;
                border-radius: 5px;
            }}

            .gradient-labels div {{
                margin: 5px 0;
            }}
            .legend-title {{
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Chemins et Infrastructures</h1>
        </header>

        <!-- Boîte d'explications en haut à droite -->
        <div class="info-box">
            <h3>Carte des centres et chemins</h3>
            <p>
                Cette carte représente chaque centre de zone, coloré en fonction de sa distance 
                (en voiture) à l’infrastructure la plus proche, pour chaque type. 
            </p>
            <p>
                <strong>Astuce :</strong> Cliquez sur un point pour afficher le chemin 
                jusqu’aux infrastructures liées à ce centre.
            </p>
            <p>
                Les zones éloignées des infrastructures sont mises en évidence 
                par des couleurs plus chaudes (rouge), indiquant des distances plus importantes.
            </p>
        </div>

        <div id="map"></div>

        <footer>
            &copy; 2025 | Projet FastAPI &mdash; Visualisation des Chemins vers Infrastructures
        </footer>

        <script>
            var zones = {json.dumps(zones_list)};
            var couleurs_infrastructures = {json.dumps(couleurs_infrastructures)};

            // Initialisation de la carte
            var map = L.map('map').setView([47.478419, -0.563166], 13);

            // Fond de carte OSM
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

            var displayedPaths = [];
            var displayedInfra = [];

            function togglePaths(id_zone) {{
                // On retire d'abord tout chemin/infrastructure déjà affiché
                if (displayedPaths.length > 0) {{
                    for (var i = 0; i < displayedPaths.length; i++) {{
                        map.removeLayer(displayedPaths[i]);
                    }}
                    displayedPaths = [];
                }}
                if (displayedInfra.length > 0) {{
                    for (var i = 0; i < displayedInfra.length; i++) {{
                        map.removeLayer(displayedInfra[i]);
                    }}
                    displayedInfra = [];
                }}

                // On affiche les chemins pour ce centre
                var geojson_file_path = '/asset/GeoJson_chemin_voiture.geojson';
                fetch(geojson_file_path)
                    .then(response => response.json())
                    .then(data => {{
                        data.features.forEach(function(feature) {{
                            if (feature.properties.id_zone == id_zone) {{
                                var path = L.geoJSON(feature, {{
                                    style: {{
                                        color: 'blue',
                                        weight: 3
                                    }}
                                }}).addTo(map);
                                displayedPaths.push(path);

                                // On affiche aussi les infrastructures associées
                                fetch('/chemins/get_infrastructure_by_paths/' + id_zone)
                                    .then(response => response.json())
                                    .then(infrastructures => {{
                                        infrastructures.forEach(function(inf) {{
                                            var color = couleurs_infrastructures[inf.type_infra] || 'black';
                                            var marker = L.marker([inf.latitude, inf.longitude], {{
                                                icon: L.divIcon({{
                                                    className: 'leaflet-div-icon',
                                                    html: '<div style="background-color:' + color + '; width: 12px; height: 12px; border-radius: 50%;"></div>'
                                                }})
                                            }}).addTo(map);
                                            displayedInfra.push(marker);
                                        }});
                                    }});
                            }}
                        }}); 
                    }}); 
            }}

            // Récupérer la couleur de chaque centre (distance moyenne)
            zones.forEach(function(zone) {{
                fetch('/chemins/get_center_color/' + zone.id_zone)
                    .then(response => response.json())
                    .then(data => {{
                        var color = data.color;
                        L.circle([zone.latitude_centre, zone.longitude_centre], {{
                            color: color,
                            fillColor: color,
                            fillOpacity: 1,
                            radius: 100
                        }}).addTo(map).on('click', function() {{
                            togglePaths(zone.id_zone);
                        }});
                    }}); 
            }});

            // Légende des types d'infrastructures
            var legend = L.control({{position: 'bottomleft'}});
            legend.onAdd = function(map) {{
                var div = L.DomUtil.create('div', 'legend');
                div.innerHTML = '<b>Légende des Infrastructures</b><br>';
                for (var type in couleurs_infrastructures) {{
                    div.innerHTML += '<i style="background:' + couleurs_infrastructures[type] + '; width: 18px; height: 18px; display:inline-block;"></i> ' + type + '<br>';
                }}
                return div;
            }};
            legend.addTo(map);

            // Légende pour le gradient de couleurs
            var gradientLegend = L.control({{position: 'bottomleft'}});
            gradientLegend.onAdd = function(map) {{
                var div = L.DomUtil.create('div', 'gradient-legend-container');
                div.innerHTML = '<div class="gradient-legend"></div>';
                div.innerHTML += '<div class="gradient-labels">' +
                    '<div>0 km</div>' +
                    '<div>20 km</div>' +
                '</div>';
                return div;
            }};
            gradientLegend.addTo(map);
        </script>
    </body>
    </html>
    """

    return content
