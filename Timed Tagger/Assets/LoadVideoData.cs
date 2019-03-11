using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using SimpleFileBrowser;
using System;

public class LoadVideoData : MonoBehaviour, IPointerClickHandler
{
    public ControlVideo videoController;

    double GetDoubleFromString(string theString)
    {
        double outputDouble;
        if (Double.TryParse(theString, out outputDouble))
        {
            return outputDouble;
        }
        else
        {
            Debug.LogError("Could not parse double from string " + theString);
        }

        return 0.0;
    }

    ControlVideo.StateNames GetStateFromString(string theString)
    {
        int outputInt;
        if (Int32.TryParse(theString, out outputInt))
        {
            return (ControlVideo.StateNames)outputInt;
        }
        else
        {
            Debug.LogError("Could not parse state from string " + theString);
        }

        return ControlVideo.StateNames.state0;
    }

    void LoadData(string filePath)
    {
        try
        {
            string line;

            List<TrackedItem> loadedItems = new List<TrackedItem>();

            bool TimeSet = false;
            // Read the file and display it line by line.  
            System.IO.StreamReader file = new System.IO.StreamReader(filePath);
            while ((line = file.ReadLine()) != null)
            {
                string[] splitLine = line.Split(',');

                if (splitLine.Length == 4)
                {
                    double currentSeconds = GetDoubleFromString(splitLine[1]);
                    ControlVideo.StateNames currentState = GetStateFromString(splitLine[2]);

                    if (!TimeSet)
                    {
                        videoController.SetStartingDateAndTime(DateTime.Parse(splitLine[0]) - new TimeSpan(0, 0, (int)currentSeconds));
                    }

                    loadedItems.Add(new TrackedItem(currentState, currentSeconds));
                }
                else
                {
                    Debug.LogError("Seems like the file was formatted wrong. Here is what it says: " + line);
                }
            }

            videoController.SetNewTrackedItemsArray(loadedItems);

            file.Close();
        }
        catch (Exception e)
        {
            Debug.LogError(e.ToString());
        }
    }

    IEnumerator ShowLoadDialogCoroutine()
    {
        // Show a load file dialog and wait for a response from user
        // Load file/folder: file, Initial path: default (Documents), Title: "Load File", submit button text: "Load"
        yield return FileBrowser.WaitForLoadDialog(false, null, "Load File", "Load");

        // Dialog is closed
        // Print whether a file is chosen (FileBrowser.Success)
        // and the path to the selected file (FileBrowser.Result) (null, if FileBrowser.Success is false)
        Debug.Log(FileBrowser.Success + " " + FileBrowser.Result);

        if (FileBrowser.Success)
        {
            LoadData(FileBrowser.Result);
        }
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        StartCoroutine(ShowLoadDialogCoroutine());
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
