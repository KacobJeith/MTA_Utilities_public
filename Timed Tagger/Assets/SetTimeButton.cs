using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class SetTimeButton : MonoBehaviour, IPointerClickHandler
{
    public GameObject DialogToClose;
    public Text TextInTimeBox;
    public ControlVideo theVideoController;

    int GetIntFromString(string theString)
    {
        int theInt;
        if (int.TryParse(theString, out theInt))
        {
            return theInt;
        }

        return 0;
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        string [] textArray = TextInTimeBox.text.Split(':');

        if(textArray.Length == 3)
        {
            int hours = GetIntFromString(textArray[0]);
            int minutes = GetIntFromString(textArray[1]);
            int seconds = GetIntFromString(textArray[2]);

            double time = hours * 3600 + minutes * 60 + seconds;

            theVideoController.SetVideoTime(time);

            DialogToClose.SetActive(false);
        }
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
