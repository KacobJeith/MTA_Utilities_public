using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using SimpleFileBrowser;

public class SaveCurrentData : MonoBehaviour, IPointerClickHandler
{
    public ControlVideo videoController;

    IEnumerator ShowSaveDialogCoRoutine()
    {
        // Show a load file dialog and wait for a response from user
        // Load file/folder: file, Initial path: default (Documents), Title: "Load File", submit button text: "Load"
        yield return FileBrowser.WaitForSaveDialog(false, null, "Save File", "Save");

        // Dialog is closed
        // Print whether a file is chosen (FileBrowser.Success)
        // and the path to the selected file (FileBrowser.Result) (null, if FileBrowser.Success is false)
        Debug.Log(FileBrowser.Success + " " + FileBrowser.Result);

        if (FileBrowser.Success)
        {
            videoController.SaveStateData(FileBrowser.Result);
        }
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        StartCoroutine(ShowSaveDialogCoRoutine());
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
