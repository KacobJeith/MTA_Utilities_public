using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Video;
using UnityEngine.UI;

public class ControlVideo : MonoBehaviour
{
    public Text videoTime;
    public Text playbackSpeed;

    VideoPlayer theVideoPlayer;

    public void LoadNewVideo(string filePath)
    {
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

    // Start is called before the first frame update
    void Start()
    {
        theVideoPlayer = GetComponent<VideoPlayer>();
        
    }

    // Update is called once per frame
    void Update()
    {

        if(Input.GetKeyDown(KeyCode.G))
        {
            theVideoPlayer.playbackSpeed++;
        }

        if (Input.GetKeyDown(KeyCode.H))
        {
            theVideoPlayer.playbackSpeed = 1;
        }

        if (Input.GetKeyDown(KeyCode.F))
        {
            theVideoPlayer.time -= 5;
        }

        if(Input.GetKeyDown(KeyCode.P))
        {
            theVideoPlayer.playbackSpeed = 0;
        }

        videoTime.text = theVideoPlayer.time.ToString();
        playbackSpeed.text = theVideoPlayer.playbackSpeed.ToString() + "x";
    }
}
