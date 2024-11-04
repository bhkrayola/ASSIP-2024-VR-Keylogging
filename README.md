# Keylogging in Virtual Reality: Assessing Data Vulnerabilities via Motion-Position Sensors
**Abstract**: [Read the published abstract here](https://journals.gmu.edu/index.php/jssr/article/view/4361)

## Project Overview
This project investigates the potential for privacy leakage in Virtual Reality (VR) environments by logging motion and orientation data from VR controllers. By using a K-Nearest Neighbors (KNN) model, we were able to classify keystrokes with high accuracy, showcasing the vulnerabilities of VR systems to keylogging attacks.

This study was aimed as a replication study for the following research: [Privacy Leakage via Unrestricted Motion-Position Sensors in the Age of Virtual Reality: A Study of Snooping Typed Input on Virtual Keyboards](https://www.winlab.rutgers.edu/~yychen/papers/Privacy%20Leakage%20via%20Unrestricted%20Motion-Position%20Sensors%20in%20the%20Age%20of%20Virtual%20Reality.pdf)



![Zhang_Brian_Ho_2024ASSIP_Poster](https://github.com/user-attachments/assets/1f1efebd-c158-4bec-9f05-5492af79f0ac)

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

### `XRTriggerDataLogger.cs`
- **Purpose**: Captures motion and trigger data from VR controllers.
- **Functionality**: 
  - **Sensor Monitoring**: Continuously logs the position, orientation, and trigger states of VR controllers in real-time.
  - **Data Relay**: Sends collected sensor data to `FileWriter` for centralized logging.

### `KeyboardInput.cs`
- **Purpose**: Handles virtual keyboard interactions and sends keypress data for logging.
- **Functionality**: 
  - **Key Press Detection**: Captures user keystrokes in the VR environment, including the specific keys pressed and their timing.
  - **Data Relay**: Sends keystroke information to the `FileWriter`

### `FileWriter.cs`
- **Purpose**: Serves as a centralized class to write data from multiple sources to a single log file.
- **Functionality**: 
  - **Centralized Data Logging**: Collects data from both the `XR Sensor Data Logger` and the `Keyboard Input`.
  - **Data Management**: Manages writing timestamped entries of sensor data and keyboard input consistently to a log file, ensuring all interactions are captured for analysis.

---

## How to Use
1. **Data Logging**: Deploy the VR application on a compatible device to collect sensor data while interacting with a virtual keyboard.
2. **Data Compilation**: Run `compileData.py` to parse, process, and compile sensor data into a structured format for KNN model training.
3. **Model Training**: Use `knn.py` to train and evaluate the KNN model, saving the trained model for future use.
4. **Testing**: Run `testingData.py` to test the model on new datasets and analyze its accuracy and performance.

---
