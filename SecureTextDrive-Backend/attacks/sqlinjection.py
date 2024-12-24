import requests

# URL of the backend server
server_url = 'http://localhost:8000/api/delete_all_filecon'

# Function to send the delete request
def delete_all_filecon():
    try:
        # Send a DELETE request to the server
        response = requests.delete(server_url)

        # Check the response status
        if response.status_code == 200:
            print("Success:", response.json()["message"])  # Successfully deleted
        elif response.status_code == 403:
            print("Error:", response.json()["error"])  # Safe mode is enabled
        else:
            print("Error:", response.json().get("error", "Failed to delete contents."))

    except requests.exceptions.RequestException as e:
        print("Request error:", str(e))

# Run the function
if __name__ == '__main__':
    delete_all_filecon()
