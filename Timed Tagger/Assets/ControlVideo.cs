using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Video;
using UnityEngine.UI;
using System;

public class TrackedItem
{
    double currentTime;
    ControlVideo.StateNames currentState;

    public TrackedItem(ControlVideo.StateNames _currentState, double _currentTime)
    {
        currentState = _currentState;
        currentTime = _currentTime;
    }

    public ControlVideo.StateNames GetState()
    {
        return currentState;
    }

    public double GetTime()
    {
        return currentTime;
    }
}

public class ControlVideo : MonoBehaviour
{
    public enum StateNames { state0 = 0, state1 = 1, state2 = 2, state3 = 3, state4 = 4, state5 = 5};
    List<string> StateNameStrings;

    public Text videoTime;
    public Text playbackSpeed;
    public Text StateText;

    public ToggleButton OverwriteButton;

    VideoPlayer theVideoPlayer;
    StateNames currentState;

    List<TrackedItem> TrackedItems;

    float previousPlaybackSpeed = 1.0f;

    CSVOptionParser SystemOptions;

    public List<GameObject> StateButtons;

    public Slider videoPositionSlider;
    bool displaySliderTime = false;
    double sliderTime;

    DateTime startingDateTime;

    public void SetNewTrackedItemsArray(List <TrackedItem> newItems)
    {
        TrackedItems = newItems;
    }

    void GetCurrentState()
    {
        double currentTime = theVideoPlayer.time;

        for(int i = 0; i < TrackedItems.Count; i++)
        {
            if(TrackedItems[i].GetTime() > currentTime)
            {
                break;
            }

            currentState = TrackedItems[i].GetState();
        }
    }

    public void SaveStateData(string filePath)
    {
        using (System.IO.StreamWriter file =
           new System.IO.StreamWriter(filePath, true))
        {
            for (int i = 0; i < TrackedItems.Count; i++)
            {
                file.WriteLine(TrackedItems[i].GetTime() + "," + (int)TrackedItems[i].GetState());
            }
        }
    }

    public void LoadNewVideo(string filePath)
    {
        TrackedItems.Clear();
        currentState = StateNames.state0;
        TrackedItems.Add(new TrackedItem(currentState, 0));

        theVideoPlayer.url = filePath;
    }

    public void SkipAhead(float numberOfSeconds)
    {
        theVideoPlayer.time += numberOfSeconds;
        OverwriteStartTime = theVideoPlayer.time;
    }

    public void SkipBack(float numberOfSeconds)
    {
        theVideoPlayer.time -= numberOfSeconds;
        OverwriteStartTime = theVideoPlayer.time;
    }

    public void IncreasePlaybackSpeed()
    {
        theVideoPlayer.playbackSpeed++;
    }

    public void PauseVideo()
    {
        previousPlaybackSpeed = theVideoPlayer.playbackSpeed;
        theVideoPlayer.playbackSpeed = 0;
    }

    public void PlayVideo()
    {
        theVideoPlayer.playbackSpeed = previousPlaybackSpeed;
    }

    public void DecreasePlaybackSpeed()
    {
        theVideoPlayer.playbackSpeed--;
    }

    public void SetVideoTime(double newTime)
    {
        theVideoPlayer.time = newTime;
    }

    double GetTimeBasedOnPercentage(float percentage)
    {
        double newSeconds = (double)percentage * theVideoPlayer.length;
        return newSeconds;
    }

    public void SetVideoTimeBasedOnPercentage(float percentage)
    {
        displaySliderTime = false;
        theVideoPlayer.time = GetTimeBasedOnPercentage(percentage);
    }

    public void SetState(StateNames newState)
    {
        if(newState != currentState)
        {
            TrackedItems.Add(new TrackedItem(newState, theVideoPlayer.time));
            currentState = newState;

            TrackedItems.Sort((x, y) => x.GetTime().CompareTo(y.GetTime()));

            // Start overwrite time where the last state was added;
            OverwriteStartTime = theVideoPlayer.time;
        }   
    }

    bool InOverwriteMode = false;
    double OverwriteStartTime = 0;
    void DoOverwriteLogic()
    {
        if(OverwriteButton.Toggled)
        {
            if(!InOverwriteMode)
            {
                InOverwriteMode = true;
                OverwriteStartTime = theVideoPlayer.time;
            }

            OverwriteDataIfNecessary();
        }
        else
        {
            InOverwriteMode = false;
        }
    }

    void OverwriteDataIfNecessary()
    {
        for(int i = 0; i < TrackedItems.Count; i++)
        {
            if(TrackedItems[i].GetTime() > OverwriteStartTime && TrackedItems[i].GetTime() < theVideoPlayer.time)
            {
                TrackedItems.RemoveAt(i);
                OverwriteDataIfNecessary();
                break;
            }
        }
    }

    void SetButtonNames()
    {
        for(int i = 0; i < StateButtons.Count; i++)
        {
            string stateName = SystemOptions.GetStringOption("state" + i);
            StateButtons[i].transform.GetChild(0).gameObject.GetComponent<Text>().text = stateName;
            StateNameStrings.Add(stateName);
        }
    }

    string Get2DigitString(int value)
    {
        string numberString = "";
        if (value < 10)
            numberString += 0;
        numberString += value;

        return numberString;
    }

    public string FormatTimeDouble(double time)
    {
        int seconds = (int)time % 60;
        int minutes = ((int)time % 3600) / 60;
        int hours = ((int)time / 3600);

        return Get2DigitString(hours) + ":" + Get2DigitString(minutes) + ":" + Get2DigitString(seconds);
    }

    public string GetFormattedTime()
    {
        return FormatTimeDouble(theVideoPlayer.time);
    }

    public string GetDisplayTime()
    {
        if(displaySliderTime)
        {
            return FormatTimeDouble(sliderTime);
        }
        else
        {
            return GetFormattedTime();
        }
    }

    void SetSliderPosition()
    {
        if(theVideoPlayer.length > 0 && !displaySliderTime)
        {
            float percentage = (float)(theVideoPlayer.time / theVideoPlayer.length);
            videoPositionSlider.value = percentage;
        }
        
    }

    public void OnDragSlider(float sliderValue)
    {
        displaySliderTime = true;
        sliderTime = GetTimeBasedOnPercentage(sliderValue);
    }

    public void SetStartingDateAndTime(DateTime startTime)
    {
        startingDateTime = startTime;
    }

    // Start is called before the first frame update
    void Start()
    {
        SystemOptions = new CSVOptionParser("VideoPlayerOptions.csv");

        Screen.SetResolution(800, 600, false);

        TrackedItems = new List<TrackedItem>();
        theVideoPlayer = GetComponent<VideoPlayer>();
        StateNameStrings = new List<string>();

        SetButtonNames();
    }

    // Update is called once per frame
    void Update()
    {
        DoOverwriteLogic();
        GetCurrentState();
        videoTime.text = GetDisplayTime();
        playbackSpeed.text = theVideoPlayer.playbackSpeed.ToString() + "x";
        SetSliderPosition();
        StateText.text = ((int)currentState).ToString() + " : " + StateNameStrings[(int)currentState];
    }
}
