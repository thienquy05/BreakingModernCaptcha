# BreakingModernCaptcha / AI Object Recognition

This project is a web application that performs object recognition on uploaded images. It is designed to identify specific objects within a 3x3 grid, similar to modern "select all images with..." CAPTCHAs.

The user uploads an image, specifies a target object (e.g., "Bicycle"), and the application uses a trained TensorFlow/Keras model to predict which of the 9 tiles in the image contain that object.

## Features

* **Simple Web Interface:** An easy-to-use frontend for uploading images and specifying a target object.
* **Image Preview:** Displays the uploaded image to the user.
* **AI-Powered Prediction:** Uses a TensorFlow/Keras model on the backend to identify objects in a 3x3 grid.
* **Targeted Detection:** Reports which specific tiles (1-9) in the grid match the user's target object.

## Technology Stack

* **Backend:**
    * Python
    * Flask (for the web server)
    * TensorFlow / Keras (for loading and running the AI model)
    * Pillow (PIL) (for image processing)
* **Frontend:**
    * HTML
    * CSS
    * JavaScript (for handling form submission and API calls)

## Setup and Installation

### 1. Backend

The backend server runs on Python and serves the prediction API.

1.  **Clone the repository.**
2.  **Install Python dependencies:**
    Navigate to the root directory and install the required packages using `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Get the Model File:**
    The backend requires the `best_model.keras` file to be present in the `backend/` directory. This file is tracked using Git LFS. Ensure you have Git LFS installed and pull the file correctly.
    ```bash
    git lfs pull
    ```
4.  **Run the Server:**
    Navigate to the `backend/` directory and run the main Python script.
    ```bash
    cd backend
    python main.py
    ```
    The server will start on `http://127.0.0.1:9000`.

### 2. Frontend

The frontend is a simple static website.

1.  **Open the HTML file:**
    Navigate to the `frontend/` directory and open the `index.html` file in your web browser.

## How to Use

1.  Ensure the backend server is running (see setup instructions).
2.  Open `frontend/index.html` in your browser.
3.  Click the "Choose File" button to select an image file.
4.  In the text box, enter the target object you want to find (e.g., "Car", "Bridge", "Traffic Light").
5.  Click the "Predict" button.
6.  The application will process the image and display the results below, indicating if the object was found and in which grid positions (1-9).

## Project Structure