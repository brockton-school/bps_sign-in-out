# 🚪 BPS Paperless Sign In/Out Tool

This is a Flask-based web form app that allows users to select their role (Student or Staff), input their name, and log whether they are signing in or signing out. The app records this information in a Google Sheet 📊.

## ✨ Features

- 👥 **User Type Selection**: Choose between "Student" and "Staff."
- 📝 **Name Input**: Enter your name.
- 🔄 **Sign In/Sign Out**: Choose whether you're signing in or out. If the user is a Student, they will need to provide a sign out reason.
- 📅 **Daily Logs**: Each day gets a new sheet in Google Sheets, and all activity for that day is recorded there.

## ⚙️ Setup

### 📋 Prerequisites

- 🐳 **Docker**: Installed on your machine.
- 📄 **Google Sheets API credentials JSON file**.
- 📝 **Google Sheet**: Created for storing the data.

### 🌐 Google Sheets API Setup

1. 🧑‍💻 Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. 🌟 Create a new project (or use an existing one).
3. 🔌 Enable the **Google Sheets API** and **Google Drive API**.
4. 🛠 Create credentials as a **Service Account** and download the JSON key file.
5. ✅ Share the Google Sheet with the service account's email to give access.
6. 💾 Save the `credentials.json` file on your machine.

### 🔑 Environment Variables

You need to set the following environment variables:

- `GOOGLE_SHEET_ID`: The ID of the Google Sheet (found in the sheet's URL).
- `GOOGLE_CREDENTIALS_PATH`: The path to your Google Sheets API credentials JSON file within the container.
- `LOCAL_GOOGLE_CREDENTIALS_PATH`: The absolute path to your Google Sheets API credentials JSON file on your system.

### 📁 .env File (Optional for Local Development)

You can create a `.env` file in the project root to store your environment variables locally:

```bash
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_CREDENTIALS_PATH=/app/credentials.json
LOCAL_GOOGLE_CREDENTIALS_PATH=/system-path/to/your-credentials.json
```

⚠️ **Warning:** This repository is public, ensure secrets, keys, and anything identifiable are not commited to the code base. 

### 🚀 Running the App

#### 1. 🏗 Build and Run with Docker

1. Clone the repository:
    ```bash
    git clone https://github.com/alanross17/bps_sigin-in-out.git
    ```

2. Build the Docker container:
    ```bash
    docker build -t webform-app .
    ```

3. Run the Docker container, passing in the environment variables:
    ```bash
    docker run -p 5000:5000 \
        --env GOOGLE_SHEET_ID=$GOOGLE_SHEET_ID \
        --env GOOGLE_CREDENTIALS_PATH=/path/to/your-credentials.json \
        webform-app
    ```

Alternatively, you can use Docker Compose for running the app:

```bash
docker-compose up
```

#### 2. 🌐 Access the App

Once the app is running, you can access it by navigating to:

```
http://localhost:5000
```

### 🛠 Development Notes

- Ensure that the `credentials.json` file is mounted as a volume in the container so that the Flask app can access it.
- The app creates a new sheet for each day and records the user’s data, including name, user type, sign-in/out status, and timestamp.

## 📄 License

This project is licensed under the MIT License.


# 📝 TODO
- Staff reason and return time
- students grade and prefilled names
- Add visitor options