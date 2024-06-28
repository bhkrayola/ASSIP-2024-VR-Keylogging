using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;
using System.IO;

public class XRSensorDataLogger : MonoBehaviour
{
    private string filePath;
    private StreamWriter writer;

    private InputDevice _rightController;
    private InputDevice _leftController;

    void Start()
    {
        Debug.Log("[SensorLogger] it works!!!!!!");

        filePath = Path.Combine(Application.persistentDataPath, "XRSensorDataLog.txt");
        Debug.Log("[SensorLogger] file path: " + filePath);

        writer = new StreamWriter(filePath, true);
        writer.WriteLine("Timestamp, Controller, Position, Orientation, ButtonPressed");

        InitializeInputDevices();
    }

    void Update()
    {
        if (!_rightController.isValid || !_leftController.isValid)
            InitializeInputDevices();

        LogControllerData(_rightController, "RightController");
        LogControllerData(_leftController, "LeftController");
    }

    private void InitializeInputDevices()
    {
        if (!_rightController.isValid)
            InitializeInputDevice(InputDeviceCharacteristics.Controller | InputDeviceCharacteristics.Right, ref _rightController);
        if (!_leftController.isValid)
            InitializeInputDevice(InputDeviceCharacteristics.Controller | InputDeviceCharacteristics.Left, ref _leftController);
    }

    private void InitializeInputDevice(InputDeviceCharacteristics inputCharacteristics, ref InputDevice inputDevice)
    {
        List<InputDevice> devices = new List<InputDevice>();
        InputDevices.GetDevicesWithCharacteristics(inputCharacteristics, devices);

        if (devices.Count > 0)
        {
            inputDevice = devices[0];
        }
    }

    private void LogControllerData(InputDevice controller, string controllerName)
    {
        if (controller.isValid)
        {
            Vector3 position;
            Quaternion orientation;
            bool isButtonPressed;

            controller.TryGetFeatureValue(CommonUsages.devicePosition, out position);
            controller.TryGetFeatureValue(CommonUsages.deviceRotation, out orientation);
            controller.TryGetFeatureValue(CommonUsages.primaryButton, out isButtonPressed);

            string logEntry = string.Format("{0},{1},{2},{3},{4}",
                Time.time,
                controllerName,
                position,
                orientation,
                isButtonPressed);
            writer.WriteLine(logEntry);
            Debug.Log("[SensorLogger] Time: " + Time.time.ToString() + ", Controller: " + controllerName + ", Position: " + position.ToString() + ", Orientation: " + orientation.ToString() + ", ButtonPressed: " + isButtonPressed.ToString());
        }
    }

    void OnApplicationQuit()
    {
        Debug.Log("[SensorLogger] closing writer");
        writer.Close();
    }
}
