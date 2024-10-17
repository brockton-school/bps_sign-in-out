# 🚪 BPS Paperless Sign In/Out Tool

This is a Flask-based web form app that allows users to select their role (Student or Staff), input their name, and log whether they are signing in or signing out. The app records this information in a Google Sheet 📊.

## ✨ Features

- 👥 **User Type Selection**: Choose between "Student", "Staff", and "Visitor"
- 📝 **Name Input**: Provides name and grade autofill for internal users.
- 🔄 **Sign In/Sign Out**: Choose whether you're signing in or out, in addtion, sign out reason and estimated return time are requested.
- ☎️ **Visitor Data**: Tracks visitor activity, contact information, and organizational affilitation.
- 📅 **Daily Logs**: Each day gets a new sheet in Google Sheets, and all activity for that day is recorded there.
- 💾 **Local Data Backup**: Stores local copies of data in `.xlsx` format for emergency use.

## ⚙️ Setup

### 📋 Prerequisites

- 🐳 **Docker**: Installed on your machine (including Docker Compose).
- 📄 **Google Sheets API credentials JSON file**.
- 📝 **Google Sheet**: Created for storing the data.
- 👥 **Personnel File For Autofill**: [Instructions to generate this file are here](./docs/personnel-setup.md), and [instructions for subsequent updates are here](./docs/personnel-updates.md).

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
- `LOCAL_DATA_PATH`: Absolute path to local data archive.

### 📁 .env File

An example `.env` file is provided in the project root to store your environment variables locally:

```bash
GOOGLE_SHEET_ID="ID FOR GOOGLE SHEET - FOUND IN URL"
LOCAL_GOOGLE_CREDENTIALS_PATH="FULL SYSTEM PATH TO GOOGLE SERVICE ACCOUNT CREDENTIALS JSON FILE"
GOOGLE_CREDENTIALS_PATH=/app/credentials.json
LOCAL_DATA_PATH="FULL SYSTEM PATH TO LOCAL DATA STORE"
```

⚠️ **Warning:** This repository is public, ensure secrets, keys, and anything identifiable are not commited to the code base. 

### 🚀 Running the App

#### 1. 🏗 Build and Run with Docker

1. Clone the repository:
    ```bash
    git clone https://github.com/alanross17/bps_sigin-in-out.git
    ```

2. Configure your build environment:
    ```bash
    cd bps_sigin-in-out
    cp .env.example .env
    ```
3. Update `.env` file with your credentials and paths. Here you will also need to create a `env/` directory where you can store `personnel.csv` file ([instructions to create this file here](./docs/personnel-setup.md)), it is best practice to also use this directory for your Google Credentials JSON.

3. Update `docker-compose.yml` if needed to suit your production/development environment. This is where auto-restart, reverse proxies, etc. can be configured.

4. Build the Docker container using the custom build script:
    ```bash
    chmod +x build.sh ## May not be required
    ./build.sh
    ```

Once built, you can use Docker Compose for running the app:

```bash
docker-compose up # Run actively in command line
docker-compose up -d # Run in background
```

📝 **NOTE/TODO**: Comfirm exact functionality, and test to find best practice for build and run.
⚠️ **WARNING**: The initial build when cloning new versions must be completed using the `build.sh` script and not directly in Docker Compose. This ensures custom build process is completed properly.

#### 2. 🌐 Access the App

Once the app is running, you can access it by navigating to:

```
http://localhost:5000
```

### 🛠 Development Notes

- Ensure that the `credentials.json` file is mounted as a volume in the container so that the app can access it.
- The app creates a new sheet for each day and records the user’s data, including name, user type, sign-in/out status, and timestamp.
- The app relies on a list of personnel names to autofill name input. This is stored as `personnel.csv`.
- Check the `config.py` file for easy configuration options and centralised variables.

## 📄 License

This project is licensed under the MIT License.


## 📝 TODO
- Add Branding (Logo, and stuff)
- ~~Add Footer Identifying Build Version~~
- ~~⚠️ Prevent blank submissions~~
- Edit visitor sign out so user can select a previous entry and mark themselves as "out"
- Track activity in the app to allow for "Sign Out" activity to be marked as "complete" when the user returns
- ~~Create a config page for easy name updating, and other details~~
- ~~Make reason text feild more promient~~
- ~~Visitor name and organization~~
