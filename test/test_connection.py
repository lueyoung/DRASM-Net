import requests

def test_connection(host, port):
    url = f"http://{host}:{port}/switches"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Successfully connected to SDN controller at {host}:{port}")
        print(f"Switches: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to SDN controller at {host}:{port}: {e}")

if __name__ == "__main__":
    test_connection("localhost", 8080)
