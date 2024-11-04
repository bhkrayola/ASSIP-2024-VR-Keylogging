using System;
using System.IO;
using UnityEngine;

public static class FileWriter
{
    private static StreamWriter writer;

    public static void Initialize(string path)
    {
        if (writer == null)
        {
            writer = new StreamWriter(path, true);
            Debug.Log("[FileWriter] the path: " + path);
        }
    }

    public static void WriteLine(string text)
    {
        if (writer != null)
        {
            writer.WriteLine(text);
            writer.Flush();
            Debug.Log("[FileWriter] wrote: " + text);
        }
        else
        {
            Debug.LogError("[FileWriter] not initialized.");
        }
    }

    public static void Close()
    {
        if (writer != null)
        {
            writer.Close();
            writer = null;
            Debug.Log("[FileWriter] Writer closed.");
        }
    }
}
