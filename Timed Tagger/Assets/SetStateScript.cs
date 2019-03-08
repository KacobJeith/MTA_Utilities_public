using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class SetStateScript : MonoBehaviour, IPointerClickHandler
{
    public ControlVideo.StateNames thisState;
    public ControlVideo videoController;

    public void OnPointerClick(PointerEventData eventData)
    {
        videoController.SetState(thisState);
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
