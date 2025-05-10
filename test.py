import routeros_api

try:
    print("Tentative de connexion au routeur...")
    connection = routeros_api.RouterOsApiPool('192.168.162.9', username='admin', password='qwerty', plaintext_login=True)
    api = connection.get_api()
    print("Connexion établie avec succès.")

    # Tester une simple commande pour vérifier la connexion
    print("Récupération des interfaces du routeur...")
    interfaces = api.get_resource('/interface')
    response = interfaces.get()  # Utilisez .get() pour obtenir les interfaces
    print("Interfaces récupérées avec succès :")
    print(response)  # Affiche la liste des interfaces du routeur

except Exception as e:
    print(f"Erreur : {e}")
