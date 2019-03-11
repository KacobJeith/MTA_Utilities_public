using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class OpenRealTimeDialog : MonoBehaviour, IPointerClickHandler
{
    public GameObject RealTimeDialog;

    public void OnPointerClick(PointerEventData eventData)
    {
        RealTimeDialog.SetActive(true);
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
