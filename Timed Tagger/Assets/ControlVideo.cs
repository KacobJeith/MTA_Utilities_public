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

    VideoPlayer theVideoPlayer;
    StateNames currentState;

    List<TrackedItem> TrackedItems;

    void GetCurrentState()
    {
        double currentTime = theVideoPlayer.time;

        for(int i = 0; i < TrackedItems.Count; i++)
        {

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
    }

    public void SkipBack(float numberOfSeconds)
    {
        theVideoPlayer.time -= numberOfSeconds;
    }

    public void IncreasePlaybackSpeed()
    {
        theVideoPlayer.playbackSpeed++;
    }

    public void PauseVideo()
    {
        theVideoPlayer.playbackSpeed = 0;
    }

    public void PlayVideo()
    {
        theVideoPlayer.playbackSpeed = 1;
    }

    public void SetState(StateNames newState)
    {
        if(newState != currentState)
        {
            TrackedItems.Add(new TrackedItem(newState, theVideoPlayer.time));
            currentState = newState;

            string TrackedItemStr = "";
            for (int i = 0; i < TrackedItems.Count; i++)
            {
                TrackedItemStr += TrackedItems[i].GetTime();
                TrackedItemStr += ", ";
            }
            Debug.Log(TrackedItemStr);

            TrackedItems.Sort((x, y) => x.GetTime().CompareTo(y.GetTime()));

            TrackedItemStr = "";
            for(int i = 0; i < TrackedItems.Count; i++)
            {
                TrackedItemStr += TrackedItems[i].GetTime();
                TrackedItemStr += ", ";
            }
            Debug.Log(TrackedItemStr);
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
        videoTime.text = theVideoPlayer.time.ToString();
        playbackSpeed.text = theVideoPlayer.playbackSpeed.ToString() + "x";
        StateText.text = currentState.ToString();
    }
}
