import routeros_api

# Configuration de connexion
router_ip = '192.168.162.9'
username = 'admin'
password = 'qwerty'

# Liste des profils à créer
profiles = [
    {'name': 'Forfait 1', 'timeout': '1h', 'rate_limit': '1M/1M'},
    {'name': 'Forfait 2', 'timeout': '2h', 'rate_limit': '2M/2M'},
    {'name': 'Forfait 3', 'timeout': '4d', 'rate_limit': '512k/512k'},
    {'name': 'Forfait 4', 'timeout': '4d', 'rate_limit': '1M/1M'},
    {'name': 'Forfait 5', 'timeout': '7d', 'rate_limit': '1536k/1536k'},  # 1.5M en kbps
    {'name': 'Forfait 6', 'timeout': '15d', 'rate_limit': '2M/2M'}
]

try:
    # Établir la connexion
    connection = routeros_api.RouterOsApiPool(
        router_ip,
        username=username,
        password=password,
        plaintext_login=True
    )
    api = connection.get_api()
    
    # Ressource pour les profils Hotspot
    hotspot_profile = api.get_resource('/ip/hotspot/user/profile')
    
    # Création des profils
    for profile in profiles:
        try:
            # Vérifier si le profil existe déjà
            existing = hotspot_profile.get(name=profile['name'])
            if existing:
                print(f"⚠️ Le profil {profile['name']} existe déjà (ID: {existing[0]['id']})")
                continue
                
            # Créer le nouveau profil
            hotspot_profile.add(
                name=profile['name'],
                session_timeout=profile['timeout'],
                rate_limit=profile['rate_limit'],
              
            )
            print(f"✅ Profil {profile['name']} créé avec succès")
            
        except routeros_api.exceptions.RouterOsApiCommunicationError as e:
            print(f"❌ Erreur lors de la création du profil {profile['name']}: {e}")
            
except Exception as e:
    print(f"🚫 Erreur de connexion: {e}")
finally:
    if 'connection' in locals():
        connection.disconnect()