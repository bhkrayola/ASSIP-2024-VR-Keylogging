using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;
using System.IO;
using System;

public class XRTriggerDataLogger : MonoBehaviour
{
    private string filePath;
    private StreamWriter writer;

    private InputDevice _rightController;
    private InputDevice _leftController;

    private bool _rightTriggerPressed = false;
    private bool _leftTriggerPressed = false;
    private string filePathString; 

    void Awake()
    {
        DontDestroyOnLoad(gameObject);
    }

    void Start()
    {
        Debug.Log("[SensorLogger] Start() called.");
        string timestamp = DateTime.Now.ToString("yyyyMMdd_HHmm");
        string fileName = $"XRSensorDataLog_{timestamp}.txt";

        filePath = Path.Combine(Application.persistentDataPath, fileName);
        filePathString = filePath;
        Debug.Log("[SensorLogger] Log file path: " + filePath);

        FileWriter.Initialize(filePath);
        FileWriter.WriteLine("Timestamp, Controller, Position, Orientation, TriggerPressed");
        FileWriter.Close();
        InitializeInputDevices();
    }

    void Update()
    {
        InitializeInputDevices();  // Continuously update input devices

        LogControllerData(_rightController, "RightController", ref _rightTriggerPressed);
        LogControllerData(_leftController, "LeftController", ref _leftTriggerPressed);
    }

    private void InitializeInputDevices()
    {
        List<InputDevice> devices = new List<InputDevice>();
        InputDevices.GetDevicesWithCharacteristics(InputDeviceCharacteristics.Controller | InputDeviceCharacteristics.Right, devices);
        if (devices.Count > 0)
        {
            _rightController = devices[0];
        }

        devices.Clear();
        InputDevices.GetDevicesWithCharacteristics(InputDeviceCharacteristics.Controller | InputDeviceCharacteristics.Left, devices);
        if (devices.Count > 0)
        {
            _leftController = devices[0];
        }
    }

    private void LogControllerData(InputDevice controller, string controllerName, ref bool triggerPressed)
    {
        if (controller.isValid)
        {
            Vector3 position;
            Quaternion orientation;
            bool isTriggerPressed;

            controller.TryGetFeatureValue(CommonUsages.devicePosition, out position);
            controller.TryGetFeatureValue(CommonUsages.deviceRotation, out orientation);
            controller.TryGetFeatureValue(CommonUsages.triggerButton, out isTriggerPressed);

            if (isTriggerPressed && !triggerPressed)
            {
                string logEntry = string.Format("{0},{1},{2},{3},{4}",
                    Time.time,
                    controllerName,
                    position,
                    orientation,
                    isTriggerPressed);
                FileWriter.Initialize(filePathString);
                FileWriter.WriteLine(logEntry);
                FileWriter.Close();
                Debug.Log("[SensorLogger] Time: " + Time.time.ToString() + ", Controller: " + controllerName +
                          ", Position: " + position.ToString() + ", Orientation: " + orientation.ToString() +
                          ", TriggerPressed: " + isTriggerPressed.ToString());
            }

            triggerPressed = isTriggerPressed;
        }
        else
        {
            Debug.LogWarning("[SensorLogger] Controller is not valid: " + controllerName);
        }
    }

    void OnApplicationQuit()
    {
        Debug.Log("[SensorLogger] Application quitting, closing writer.");
        writer.Close();
    }
}
