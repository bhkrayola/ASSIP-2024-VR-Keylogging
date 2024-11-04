import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib

def parse_csv(file_path):
    timestamps = []
    positions = []
    orientations = []
    trigger_pressed = []
    keystrokes = []
    answer = ""

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if not row:
                continue
            if row[0].strip().lower() == 'answer':
                answer = row[1].strip()
                continue
            try:
                if row[0].startswith('Keystroke'):
                    keystrokes.append((row[1], float(row[2])))
                else:
                    timestamps.append(float(row[0]))
                    position_str = row[2] + ',' + row[3] + ',' + row[4]
                    positions.append(tuple(map(float, position_str.strip('()').split(','))))
                    orientation_str = row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8]
                    orientations.append(tuple(map(float, orientation_str.strip('()').split(','))))
                    trigger_pressed.append(row[9].strip().lower() == 'true')
            except ValueError:
                continue

    return timestamps, positions, orientations, trigger_pressed, keystrokes, answer

def pitchAndRoll(orientation):
    x, y, z, w = orientation
    pitch = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x**2 + y**2))
    roll = np.arcsin(2 * (w * y - z * x))
    return pitch, roll

def rotationMatrix(pitch, roll):
    R_pitch = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    R_roll = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])

    R = np.dot(R_pitch, R_roll)
    return R

def estimateCursor(position, orientation, initial, l):
    pitch, roll = pitchAndRoll(orientation)
    current = rotationMatrix(pitch, roll)
    relativePos = np.array([position[0], position[1], position[2] - l])
    cursorPos = np.dot(current, relativePos)
    return cursorPos

def find_typing_windows(timestamps, trigger_pressed, fmin=1, fmax=2, tmin=5):
    typing_windows = []
    max_window = None
    max_duration = 0
    n = len(timestamps)

    for ts in range(n):
        if not trigger_pressed[ts]:
            continue

        for te in range(ts + 1, n):
            if not trigger_pressed[te]:
                break

            duration = timestamps[te] - timestamps[ts]
            if duration >= tmin:
                press_count = sum(trigger_pressed[ts:te + 1])
                frequency = press_count / duration
                if fmin <= frequency <= fmax:
                    typing_windows.append((timestamps[ts], timestamps[te]))
                    if duration > max_duration:
                        max_duration = duration
                        max_window = (timestamps[ts], timestamps[te])

    return typing_windows, max_window

def detect_typing_mechanism(trigger_pressed):
    #For laser-based typing, we assume frequent trigger presses
    if any(trigger_pressed):
        return "Laser-based"
    else:
        return "Unknown"

def find_closest_timestamp(timestamps, target_time):
    closest_time = min(timestamps, key=lambda t: abs(t - target_time))
    return closest_time

def process_file(file_path, output_file, knn_model, int_to_keystroke):
    timestamps, positions, orientations, trigger_pressed, keystrokes, answer = parse_csv(file_path)
    typing_mechanism = detect_typing_mechanism(trigger_pressed)
    print(f"Typing Mechanism: {typing_mechanism}")

    if typing_mechanism == "Laser-based":
        typing_windows, max_window = find_typing_windows(timestamps, trigger_pressed)
        print(f"Estimated Typing Windows: {typing_windows}")
        print(f"Max Estimated Typing Window: {max_window}")

        first_keystroke_time = keystrokes[0][1]
        last_keystroke_time = keystrokes[-1][1]

        closest_start_time = find_closest_timestamp(timestamps, first_keystroke_time)
        closest_end_time = find_closest_timestamp(timestamps, last_keystroke_time)
        
        true_typing_window = (closest_start_time, closest_end_time)
        print(f"True Typing Window: {true_typing_window}")

        print(f"Answer: {answer}")
        total_keystrokes = len(keystrokes)
        print(f"Number of Keystrokes: {total_keystrokes}")

        estimated_keystrokes = [k for k in keystrokes if max_window and max_window[0] <= k[1] <= max_window[1]]
        estimated_keystrokes_count = len(estimated_keystrokes)
        print(f"Number of Keystrokes in Estimated Timing Window: {estimated_keystrokes_count}")

        fraction_keystrokes = estimated_keystrokes_count / total_keystrokes if total_keystrokes > 0 else 0
        print(f"Fraction of Keystrokes in Estimated vs True Timing Window: {fraction_keystrokes:.2f}")

        #Assume the first position and orientation as the initial stage
        initial_position = positions[0]
        initial_quaternion = orientations[0]
        initial_pitch, initial_roll = pitchAndRoll(initial_quaternion)
        initial_rotation_matrix = rotationMatrix(initial_pitch, initial_roll)

        keystrokes_with_positions = []

        #Calculate cursor positions using the rotation matrix from quaternions for keystroke times
        for keystroke, keystroke_time in keystrokes:
            closest_time = find_closest_timestamp(timestamps, keystroke_time)
            index = timestamps.index(closest_time)
            position = positions[index]
            quaternion = orientations[index]
            l = 2
            cursor_position = estimateCursor(position, quaternion, initial_rotation_matrix, l)
            keystrokes_with_positions.append((keystroke, cursor_position.tolist()))

        #Predict using the KNN model
        cursor_positions = np.array([kp[1] for kp in keystrokes_with_positions])
        predicted_keystrokes = knn_model.predict(cursor_positions)
        original_keystrokes = [kp[0] for kp in keystrokes_with_positions]
        predicted_keystrokes_labels = [int_to_keystroke[keystroke] for keystroke in predicted_keystrokes]

        filtered_original_keystrokes = [kp for kp in original_keystrokes if kp not in [' Start']]
        filtered_predicted_keystrokes_labels = [predicted_keystrokes_labels[i] for i in range(len(original_keystrokes)) if original_keystrokes[i] not in [' Start']]

        accuracy = accuracy_score(filtered_original_keystrokes, filtered_predicted_keystrokes_labels)

        with open('results.txt', 'a') as result_file:
            result_file.write(f"file {file_path}\n")
            result_file.write(f"original: {' '.join(filtered_original_keystrokes)}\n")
            result_file.write(f"predicted: {' '.join(filtered_predicted_keystrokes_labels)}\n")
            result_file.write(f"percent correct: {accuracy:.2f}\n")
            result_file.write("next file\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py directory_path output_file.csv")
    else:
        directory_path = sys.argv[1]
        output_file = sys.argv[2]

        knn_model = joblib.load('knn_model.joblib')

        int_to_keystroke = {0: ' Start', 1: ' q', 2: ' w', 3: ' e', 4: ' r', 5: ' t', 6: ' y', 7: ' u', 8: ' i', 9: ' o', 10: ' p', 11: ' a', 12: ' s', 13: ' d', 14: ' f', 15: ' g', 16: ' h', 17: ' j', 18: ' k', 19: ' l', 20: " '", 21: ' z', 22: ' x', 23: ' c', 24: ' v', 25: ' b', 26: ' n', 27: ' m', 28: ' .', 29: ' Space_Button', 30: ' Enter_Button', 31: ' Backspace', 32: ' close_button'}
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                process_file(file_path, output_file, knn_model, int_to_keystroke)
