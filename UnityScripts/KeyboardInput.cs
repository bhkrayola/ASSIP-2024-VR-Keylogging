using UnityEngine;
using TMPro;
using Oculus.Platform;

public class VRKeyboardInput : MonoBehaviour
{
    private TouchScreenKeyboard keyboard;
    public TMP_InputField inputField;

    void Start()
    {
        Oculus.Platform.Core.Initialize();
        if (inputField != null)
        {
            inputField.onSelect.AddListener(ShowKeyboard);
        }
        else
        {
            Debug.LogError("TMP_InputField is not assigned.");
        }
    }

    public void ShowKeyboard(string text)
    {
        Debug.Log("Showing Oculus Keyboard");
        keyboard = TouchScreenKeyboard.Open("", TouchScreenKeyboardType.Default);
    }

    void Update()
    {
        if (keyboard != null && keyboard.status == TouchScreenKeyboard.Status.Done)
        {
            inputField.text = keyboard.text;
        }
    }
}
