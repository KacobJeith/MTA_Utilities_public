using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class ToggleButton : MonoBehaviour, IPointerClickHandler
{
    public bool Toggled;

    public void OnPointerClick(PointerEventData eventData)
    {
        if (Toggled)
            Toggled = false;
        else
            Toggled = true;
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(Toggled)
        {
            GetComponent<Image>().color = new Color(0.2f, 0.8f, 0.2f);
        }
        else
        {
            GetComponent<Image>().color = new Color(1,1,1);
        }
    }
}
