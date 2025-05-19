from apiluizalabs.models import mem_clients


class ClientRepository:
    def get_all(self):
        """Retorna todos os clientes"""
        return list(mem_clients.values())

    def get_by_email(self, email):
        """Retorna um cliente pelo email"""
        client = mem_clients.get(email)
        if client:
            if "favorites" not in client:
                client["favorites"] = []
            # Favoritos: busca os dados completos dos produtos em mem_products
            elif client["favorites"] and isinstance(client["favorites"][0], str):
                from apiluizalabs.models import mem_products

                client["favorites"] = [
                    mem_products[fav_id]
                    for fav_id in client["favorites"]
                    if fav_id in mem_products
                ]
        return client

    def create(self, client_data):
        """Cria um novo cliente"""
        email = client_data["email"]

        # Garantir que o cliente tenha uma lista de favorites
        if "favorites" not in client_data:
            client_data["favorites"] = []

        mem_clients[email] = client_data
        return client_data

    def update(self, email, client_data):
        """Atualiza um cliente existente"""
        if email not in mem_clients:
            return None

        # Se estiver atualizando o email, mover o cliente
        new_email = client_data.get("email")
        if new_email and new_email != email and new_email in mem_clients:
            # Se email ja existente, nao permitir atualizacao
            return None

        # Atualiza os campos fornecidos
        for key, value in client_data.items():
            mem_clients[email][key] = value

        if new_email and new_email != email:
            client = mem_clients[email]
            del mem_clients[email]
            mem_clients[new_email] = client
            return client

        return mem_clients[email]

    def delete(self, email):
        """Remove um cliente pelo email"""
        if email in mem_clients:
            client = mem_clients[email]
            del mem_clients[email]
            return client
        return None

    def email_exists(self, email):
        """Verifica se um email ja existe"""
        return email in mem_clients
