import sys
import random
import requests
from faker import Faker


# Configurações
BASE_URL = "http://localhost:8989"
AUTH = ("admin", "admin123")
fake = Faker("pt_BR")


def create_clients(num_clients=50):
    print(f"Criando {num_clients} clientes...")

    created = 0
    for _ in range(num_clients):
        client_data = {"name": fake.name(), "email": fake.email()}

        try:
            response = requests.post(
                f"{BASE_URL}/clients/", json=client_data, auth=AUTH
            )

            if response.status_code == 200:
                created += 1
                print(f"Cliente criado: {client_data['email']}")
            else:
                print(f"Erro ao criar cliente: {response.json()}")
        except Exception as e:
            print(f"Erro de conexão: {str(e)}")

    print(f"Total de clientes criados: {created}")
    return created


def get_clients_list():
    try:
        response = requests.get(f"{BASE_URL}/clients/", auth=AUTH)
        if response.status_code != 200:
            print(f"Erro ao obter clientes: {response.json()}")
            return None

        clients_list = response.json()

        if not clients_list:
            print("Nenhum cliente encontrado p/ adicionar favoritos.")
            return None

        return clients_list
    except Exception as e:
        print(f"Erro ao obter clientes: {str(e)}")
        return None


def verify_api_status():
    try:
        response = requests.get(f"{BASE_URL}/", auth=AUTH)
        if response.status_code != 200:
            print(f"Erro: verificar API: {response.json()}")
            return False
        return True
    except Exception as e:
        print(f"Erro: verificar API: {str(e)}")
        return False


def add_favorites_for_client(email, num_to_add, product_ids):
    favs_added = 0

    products_to_try = random.sample(product_ids, min(num_to_add * 2, len(product_ids)))

    while favs_added < num_to_add and products_to_try:
        product_id = products_to_try.pop()

        try:
            response = requests.post(
                f"{BASE_URL}/favorites/{email}",
                json={"product_id": product_id},
                auth=AUTH,
            )

            if response.status_code == 200:
                favs_added += 1
                print(f"Favorito adicionado: {email} -> {product_id}: Sucesso.")
            else:
                print(f"Erro ao add favorito: {response.json()}")
        except Exception as e:
            print(f"Erro ao add favorito: {str(e)}")

    print(f"Adicionados {favs_added}/{num_to_add} favoritos p/ {email}")
    return favs_added


def add_random_favorites(num_favorites_min=0, num_favorites_max=5):
    print(
        f"Adicionando de {num_favorites_min} a {num_favorites_max} produtos favoritos randomicos por cliente..."
    )

    clients_list = get_clients_list()
    if not clients_list:
        return 0

    if not verify_api_status():
        return 0

    product_ids = [f"prod-{i}" for i in range(1, 101)]
    total_added = 0

    for client in clients_list:
        email = client["email"]

        num_to_add = random.randint(num_favorites_min, num_favorites_max)

        if num_to_add == 0:
            print(f"Cliente {email} nao recebera produtos favoritos sorteado ZERO.")
            continue

        print(f"Tentando adicionar {num_to_add} favoritos para {email}")

        total_added += add_favorites_for_client(email, num_to_add, product_ids)

    print(f"Total de favoritos criados e adicionados: {total_added}")
    return total_added


if __name__ == "__main__":
    print("Iniciando carga de dados fake....")

    try:
        response = requests.get(f"{BASE_URL}", auth=AUTH)
    except requests.exceptions.ConnectionError:
        print("ERRO: A API não está rodando. Inicie a API antes de fazer a carga de dados.'")
        sys.exit(1)

    create_clients(50)
    add_random_favorites(0, 5)

    print("Carga de dados concluida - Sucesso!!!")
