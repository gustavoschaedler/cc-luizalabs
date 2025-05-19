from apiluizalabs.models import mem_clients, mem_products


class ClientRepository:
    def get_all(self):
        """Retorna todos os clientes"""
        return list(mem_clients.values())

    def get_by_email(self, email, product_source="mock"):
        """Retorna um cliente pelo email e monta os favoritos corretamente"""
        client = mem_clients.get(email)
        if client:
            if "favorites" not in client:
                client["favorites"] = []
            elif client["favorites"]:
                # Se favoritos são IDs, buscar os dados completos
                if isinstance(client["favorites"][0], str):
                    if product_source == "mock":
                        client["favorites"] = [
                            mem_products[fav_id] for fav_id in client["favorites"] if fav_id in mem_products
                        ]
                    elif product_source == "api":
                        api_auth = os.getenv("PRODUCTS_API_AUTHORIZATION")
                        api_url = os.getenv("PRODUCTS_API_URL")
                        headers = {}

                        if all([api_url, api_auth]):
                            headers["Authorization"] = f"Bearer {api_auth}"
                        else:
                            raise Exception("API de produtos não configurada")

                        favoritos = []
                        for product_id in client["favorites"]:
                            url = f"{api_url}/products/{product_id}"
                            try:
                                resp = httpx.get(url, headers=headers)
                                if resp.status_code == 200:
                                    favoritos.append(resp.json())
                            except Exception:
                                continue
                        client["favorites"] = favoritos
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
