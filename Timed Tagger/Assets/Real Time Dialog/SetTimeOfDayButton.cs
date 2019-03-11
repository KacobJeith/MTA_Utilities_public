using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using System;

public class SetTimeOfDayButton : MonoBehaviour, IPointerClickHandler
{
    public GameObject RealTimeDialog;
    public Text InputText;
    public ControlVideo theVideoController;
    public Text InstructionText;

    public void OnPointerClick(PointerEventData eventData)
    { 
        DateTime realDateTime;

        if(DateTime.TryParse(InputText.text, out realDateTime))
        {
            theVideoController.SetStartingDateAndTime(realDateTime);

            Debug.Log("Date time set to : " + realDateTime);
            RealTimeDialog.SetActive(false);
        }
        else
        {
            InstructionText.color = new Color(1.0f, 0, 0);
            InstructionText.text = "Failed! Make sure you enter your date and time in a standard mm/dd/yyyy hh:mm:ss format";
            Debug.Log("Failed to parse date time");
        }
    }

    private void OnEnable()
    {
        InstructionText.color = new Color(0, 0, 0);
        InstructionText.text = "Set the real date and time of the video. Standard formats like mm/dd/yyyy hh:mm:ss will work.";
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
