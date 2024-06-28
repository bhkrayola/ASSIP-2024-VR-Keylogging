using UnityEngine;
using System.Collections;
using System.IO;
using Oculus.Platform;
using Oculus.Platform.Models;

public class OculusSensorDataLogger : MonoBehaviour
{
    private string filePath;
    private StreamWriter writer;

    void Start()
    {
        Debug.Log("[SensorLogger] it works!!!!!!!!");
        Oculus.Platform.Core.AsyncInitialize();

        filePath = Path.Combine(UnityEngine.Application.persistentDataPath, "SensorDataLog.txt");
        Debug.Log("[SensorLogger] file path: " + filePath);

        writer = new StreamWriter(filePath, true);
        writer.WriteLine("Timestamp, Controller, Position, Orientation, ButtonPressed");
    }

    void Update()
    {
        LogControllerData(OVRInput.Controller.LTouch);
        LogControllerData(OVRInput.Controller.RTouch);
    }

    void LogControllerData(OVRInput.Controller controller)
    {
        Vector3 position = OVRInput.GetLocalControllerPosition(controller);
        Quaternion orientation = OVRInput.GetLocalControllerRotation(controller);
        bool isButtonPressed = OVRInput.Get(OVRInput.Button.Any, controller);

        string logEntry = string.Format("{0},{1},{2},{3},{4}",
            Time.time,
            controller,
            position,
            orientation,
            isButtonPressed);
        writer.WriteLine(logEntry);
        Debug.Log("[SensorLogger] " + "Time: " + Time.time.ToString() + ", Controller: " + controller.ToString() + ", Position: " + position.ToString() + ", Orientation: " + orientation.ToString() + ", ButtonPressed: " + isButtonPressed.ToString());
    }

    void OnApplicationQuit()
    {
        Debug.Log("[SensorLogger] closing writer");
        writer.Close();
    }
}
