# KnorozovAPI: A Multilingual Translation Management Platform

![image](https://github.com/user-attachments/assets/15abc9e2-970d-4bf3-97b3-8162a0391eaa)

KnorozovAPI is a comprehensive platform for managing multilingual translations, empowering you to effortlessly handle translations for your applications or websites. 

## Features:

- **Centralized Translation Management:** Store and manage all your translations in a single, organized location.
- **Multilingual Support:**  Add and manage translations for any number of languages.
- **User Roles and Permissions:**  Assign specific roles and permissions to users, controlling access to languages and translation editing capabilities.
- **Easy Translation Editing:** An intuitive interface simplifies the process of adding, modifying, and deleting translation entries.
- **Language Management:** Add, delete, and update languages supported by your application. 
- **Translation Download:** Download the entire translation database as a JSON file for offline use or integration with other tools.

## Technical Stack:

- **Backend:** FastAPI (Python)
- **Frontend:** Vue.js 
- **Database:** MongoDB

## Getting Started

### Prerequisites:

- Docker and Docker Compose installed.

### Running the Project:

1. **Clone the repository:** 
   ```bash
   git clone https://github.com/your-username/KnorozovAPI.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd KnorozovAPI 
   ```

3. **Start the application with Docker Compose:**
   ```bash
   docker compose up -d
   ```

   This will start the backend server, frontend client, and MongoDB database.

4. **Access the application:**
   -  The frontend will be accessible at: [http://localhost:3000](http://localhost:3000).

### Admin User:

- On the first startup, an admin user will be created based on the first user to sign up. 

## Using KnorozovAPI:

1. **Log in as admin:**
   - Access the login page and enter the default admin credentials.

2. **Manage languages:**
   - Navigate to the "Languages" tab to add, update, or delete languages.

3. **Manage users:**
   - Use the "Users" tab to create new users and assign them roles and language permissions.

4. **Edit translations:**
   - Go to the "Translation" tab to manage translations for different pages and languages.
   - Add new translation entries, modify existing ones, or delete unnecessary entries. 

5. **Download translations:**
   - Click the "Download translation" button to download the entire translation database as a JSON file.

## Contributing

Contributions to KnorozovAPI are welcome!  If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
