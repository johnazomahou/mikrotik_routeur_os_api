import csv
import routeros_api

# Configuration MikroTik
router_ip = "192.168.162.9"  # IP locale de MikroTik
username = "admin"
password = "qwerty"  # mot de passe admin MikroTik

# Fichier CSV
csv_file = "user.csv"

# Définition des profils avec leurs limites
profile_limits = {
    'Forfait 1': {'data_limit': '0'},          # Illimité
    'Forfait 2': {'data_limit': '0'},          # Illimité
    'Forfait 3': {'data_limit': '1073741824'},  # 1 Go en octets
    'Forfait 4': {'data_limit': '2147483648'},  # 2 Go en octets
    'Forfait 5': {'data_limit': '3221225472'},  # 3 Go en octets
    'Forfait 6': {'data_limit': '4294967296'}   # 4 Go en octets
}


# Connexion au routeur
try:
    connection = routeros_api.RouterOsApiPool(router_ip, username=username, password=password, plaintext_login=True)
    api = connection.get_api()
    print("Connexion établie avec succès.")

    # Vérifiez les profils existants (à des fins de débogage)
    profiles = api.get_resource('/ip/hotspot/user/profile').get()
    print("Profils Hotspot disponibles :")
    for profile in profiles:
        print(profile['name'])

    # Lecture et import
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:  # utf-8-sig pour gérer BOM
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Vérifiez si l'utilisateur existe déjà
                existing_users = api.get_resource('/ip/hotspot/user').get(name=row["Username"])
                if existing_users:
                    print(f"⚠️ Utilisateur existe déjà: {row['Username']}")
                    continue  # Passer à l'utilisateur suivant

                # Convertir la durée en secondes (ex: "1h" → 3600)
                duration = row["Hours/Duration"]
                if duration.endswith('h'):
                    uptime_limit = str(int(duration[:-1]) * 3600)
                elif duration.endswith('d'):
                    uptime_limit = str(int(duration[:-1]) * 86400)
                else:
                    uptime_limit = duration  # suppose que c'est déjà en secondes


                forfait_type = row["Plan"]
                data_limit = profile_limits[forfait_type]['data_limit']

                user_data = {
                    "name": row["Username"],
                    "password": row["Password"],
                    "profile": row["Plan"],  # profil à utiliser
                    "limit-uptime": uptime_limit,
                    "limit-bytes-total": data_limit
                   
                }

                # Ajouter l'utilisateur via l'API RouterOS
                response = api.get_resource('/ip/hotspot/user').add(**user_data)
                print(f"✅ Ajouté: {row['Username']}")

            except KeyError as e:
                print(f"Erreur: Colonne manquante dans le fichier CSV pour {row}: {e}")
            except Exception as e:
                print(f"Erreur lors de l'ajout de l'utilisateur {row['Username']}: {e}")

except FileNotFoundError:
    print(f"Erreur: Le fichier {csv_file} n'a pas été trouvé.")
except Exception as e:
    print(f"Une erreur inattendue s'est produite: {e}")
