using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class VideoControlButtonScript : MonoBehaviour, IPointerClickHandler
{
    public enum buttonFunction { play, pause, skipBack, increaseSpeed, skipForward };

    public buttonFunction currentButtonFunction;
    public ControlVideo theVideoController;

    public virtual void OnPointerClick(PointerEventData eventData)
    {
        if(currentButtonFunction == buttonFunction.play)
        {
            theVideoController.PlayVideo();
        }
        else if (currentButtonFunction == buttonFunction.pause)
        {
            theVideoController.PauseVideo();
        }
        else if (currentButtonFunction == buttonFunction.skipBack)
        {
            theVideoController.SkipBack(5);
        }
        else if (currentButtonFunction == buttonFunction.increaseSpeed)
        {
            theVideoController.IncreasePlaybackSpeed();
        }
        else if (currentButtonFunction == buttonFunction.skipForward)
        {
            theVideoController.SkipAhead(5);
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
