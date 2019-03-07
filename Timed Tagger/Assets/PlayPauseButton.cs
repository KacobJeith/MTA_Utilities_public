using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class PlayPauseButton : VideoControlButtonScript
{
    public Sprite PlayButton;
    Sprite PauseButton;

    public override void OnPointerClick(PointerEventData eventData)
    {
        base.OnPointerClick(eventData);

        if(currentButtonFunction == buttonFunction.play)
        {
            currentButtonFunction = buttonFunction.pause;
            GetComponent<Image>().sprite = PauseButton;
        }
        else if(currentButtonFunction == buttonFunction.pause)
        {
            PauseButton = GetComponent<Image>().sprite;
            currentButtonFunction = buttonFunction.play;
            GetComponent<Image>().sprite = PlayButton;
        }
    }
}
