using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class HandleTimeSlide : MonoBehaviour, IDragHandler, IEndDragHandler, IPointerUpHandler
{
    public ControlVideo theVideoPlayer;
    Slider timeSlider;

    public void OnDrag(PointerEventData eventData)
    {
        theVideoPlayer.OnDragSlider(timeSlider.value);
    }

    // Start is called before the first frame update
    void Start()
    {
        timeSlider = GetComponent<Slider>();   
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void OnEndDrag(PointerEventData eventData)
    {
        theVideoPlayer.SetVideoTimeBasedOnPercentage(timeSlider.value); 
    }

    public void OnPointerUp(PointerEventData eventData)
    {
        theVideoPlayer.SetVideoTimeBasedOnPercentage(timeSlider.value);
    }
}
