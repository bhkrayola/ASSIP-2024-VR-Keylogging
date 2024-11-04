# Keylogging in Virtual Reality: Assessing Data Vulnerabilities via Motion-Position Sensors

## Project Overview
This project investigates the potential for privacy leakage in Virtual Reality (VR) environments by logging motion and orientation data from VR controllers. By using a K-Nearest Neighbors (KNN) model, we were able to classify keystrokes with high accuracy, showcasing the vulnerabilities of VR systems to keylogging attacks.
This study was aimed as a replication study for the following research: [Privacy Leakage via Unrestricted Motion-Position Sensors in the Age of Virtual Reality: A Study of Snooping Typed Input on Virtual Keyboards](https://www.winlab.rutgers.edu/~yychen/papers/Privacy%20Leakage%20via%20Unrestricted%20Motion-Position%20Sensors%20in%20the%20Age%20of%20Virtual%20Reality.pdf)

**Abstract**: [Read the abstract here](https://journals.gmu.edu/index.php/jssr/article/view/4361)

---

## Code Summaries

### `compileData.py`
- **Purpose**: A comprehensive script for processing raw VR sensor data and preparing it for model training and analysis.
- **Functionality**: 
  - **Data Parsing**: Reads multiple CSV files containing raw sensor data, extracting timestamps, positions, orientations, and trigger states.
  - **Typing Window Detection**: Implements algorithms to identify when typing occurs based on trigger press frequency and duration.
  - **3D Cursor Position Estimation**: Uses orientation data to compute the 3D position of the cursor relative to the VR controller.
  - **Data Organization**: Compiles processed keystrokes and their associated 3D coordinates into a structured dataset, ready for KNN model training.
  - **Output**: Writes the formatted data to `output.csv` for subsequent use in model training and testing.

### `knn.py`
- **Purpose**: Implements the K-Nearest Neighbors (KNN) algorithm to classify keystrokes based on 3D cursor positions.
- **Functionality**: 
  - **Model Training**: Trains a KNN model using the compiled 3D position data from `output.csv`.
  - **Prediction**: Uses the trained model to predict keystrokes for new data and evaluates the model's performance.

### `output.csv`
- **Purpose**: Contains the compiled 3D position data and associated keystrokes used for training and testing the KNN model.
- **Content**: Each row includes a keystroke label and its corresponding x, y, and z coordinates.

### `testingData.py`
- **Purpose**: Tests the KNN model on separate datasets to evaluate its performance.
- **Functionality**: 
  - **Model Testing**: Loads testing data and uses the saved KNN model to make predictions.
  - **Performance Metrics**: Outputs the accuracy and generates a report of the model's effectiveness in keystroke prediction.

### `FileWriter.cs`
- **Purpose**: Handles writing sensor data to a text file in the VR application.
- **Functionality**: 
  - **Data Collection**: Collects real-time data such as timestamps, positions, orientations, and trigger states from VR controllers.
  - **File Writing**: Writes this data to a local file on the device for later analysis.

### `KeyboardInput.cs`
- **Purpose**: Manages user keyboard input within the VR environment.
- **Functionality**: 
  - **Keystroke Detection**: Detects and logs key presses, including their timestamps and associated sensor data.
  - **Data Logging**: Ensures all keystroke events are accurately recorded for use in data analysis.

### `XRTriggerDataLogger.cs`
- **Purpose**: Logs VR controller trigger events and additional sensor data.
- **Functionality**: 
  - **Continuous Monitoring**: Monitors VR controller inputs, capturing positions, orientations, and trigger states.
  - **Data Storage**: Logs all captured data to a file, providing a detailed record of user interactions for later analysis.

---

## How to Use
1. **Data Logging**: Deploy the VR application on a compatible device to collect sensor data while interacting with a virtual keyboard.
2. **Data Compilation**: Run `compileData.py` to parse, process, and compile sensor data into a structured format for KNN model training.
3. **Model Training**: Use `knn.py` to train and evaluate the KNN model, saving the trained model for future use.
4. **Testing**: Run `testingData.py` to test the model on new datasets and analyze its accuracy and performance.

---
