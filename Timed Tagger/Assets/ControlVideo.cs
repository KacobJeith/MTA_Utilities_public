using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Video;
using UnityEngine.UI;

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
    public enum StateNames { state1, state2, state3, state4, state5, state6 };

    public Text videoTime;
    public Text playbackSpeed;
    public Text StateText;

    public ToggleButton OverwriteButton;

    VideoPlayer theVideoPlayer;
    StateNames currentState;

    List<TrackedItem> TrackedItems;

    float previousPlaybackSpeed = 1.0f;

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
                file.WriteLine(TrackedItems[i].GetTime() + "," + TrackedItems[i].GetState());
            }
        }
    }

    public void LoadNewVideo(string filePath)
    {
        TrackedItems.Clear();
        currentState = StateNames.state1;
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

    // Start is called before the first frame update
    void Start()
    {
        Screen.SetResolution(800, 600, false);

        TrackedItems = new List<TrackedItem>();
        theVideoPlayer = GetComponent<VideoPlayer>();
    }

    // Update is called once per frame
    void Update()
    {
        DoOverwriteLogic();
        GetCurrentState();
        videoTime.text = theVideoPlayer.time.ToString();
        playbackSpeed.text = theVideoPlayer.playbackSpeed.ToString() + "x";
        StateText.text = currentState.ToString();
    }
}
