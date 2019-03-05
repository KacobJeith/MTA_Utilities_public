using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

public class StuffToTrack
{
    public enum Trackables { thing1, thing2, thing3 };
    Trackables currentTrackable;
    TimeSpan currentTime;

    public StuffToTrack(Trackables trackedThing, TimeSpan timePassed)
    {
        currentTime = timePassed;
        currentTrackable = trackedThing;
    }

    public Trackables GetTrackable()
    {
        return currentTrackable;
    }

    public TimeSpan GetTime()
    {
        return currentTime;
    }
}

public class ControlScript : MonoBehaviour
{
    public Text timeDisplay;

    private DateTime startingTime;
    private DateTime currentTime;
    private TimeSpan currentTimeDifference;

    private bool runningTimer;
    private bool startedTimer;

    List<StuffToTrack> trackedItems;

    public GameObject Dylan;
    public GameObject Jacob;
    public GameObject Victor;
    public GameObject Yenny;

    public GameObject theCanvas;

    void SpawnAPic()
    {
        GameObject spawnedPerson;
        int randomNumber = UnityEngine.Random.Range(0, 4);

        Debug.Log(randomNumber);

        if (randomNumber == 0)
            spawnedPerson = Instantiate(Dylan);
        else if (randomNumber == 1)
            spawnedPerson = Instantiate(Victor);
        else if (randomNumber == 2)
            spawnedPerson = Instantiate(Yenny);
        else
            spawnedPerson = Instantiate(Jacob);

        spawnedPerson.transform.parent = theCanvas.transform;
        spawnedPerson.GetComponent<RectTransform>().position = new Vector2(UnityEngine.Random.Range(200, 600), UnityEngine.Random.Range(100, 500));
        Destroy(spawnedPerson, 0.5f);
    }

    // Start is called before the first frame update
    void Start()
    {
        trackedItems = new List<StuffToTrack>();

        runningTimer = false;

        startingTime = DateTime.Now;
    }

    // Update is called once per frame
    void Update()
    {
        
        if(startedTimer)
        {
            DetectThingKeyPresses();
        }
        

        if(Input.GetKeyDown(KeyCode.S))
        {
            if(!startedTimer)
            {
                startingTime = DateTime.Now;
                runningTimer = true;
                startedTimer = true;
            }
            
        }

        if(Input.GetKeyDown(KeyCode.E))
        {
            if(startedTimer)
            {
                startedTimer = false;
                runningTimer = false;
                PrintOutputAndClear();
            }
        }

        if(Input.GetKeyDown(KeyCode.P))
        {
            if(startedTimer)
            {
                if (runningTimer)
                {
                    runningTimer = false;
                }
                else
                {
                    runningTimer = true;
                    startingTime = DateTime.Now - currentTimeDifference;
                }
            }
            
        }


        if (runningTimer)
        {
            currentTime = DateTime.Now;
            currentTimeDifference = currentTime - startingTime;
        }

        UpdateTimeText();
    }

    void DetectThingKeyPresses()
    {
        if (Input.GetKeyDown(KeyCode.F))
        {
            SpawnAPic();
            trackedItems.Add(new StuffToTrack(StuffToTrack.Trackables.thing1, currentTimeDifference));
        }

        if (Input.GetKeyDown(KeyCode.G))
        {
            SpawnAPic();
            trackedItems.Add(new StuffToTrack(StuffToTrack.Trackables.thing2, currentTimeDifference));
        }

        if (Input.GetKeyDown(KeyCode.H))
        {
            SpawnAPic();
            trackedItems.Add(new StuffToTrack(StuffToTrack.Trackables.thing3, currentTimeDifference));
        }
    }

    void UpdateTimeText()
    {
        
        timeDisplay.text = currentTimeDifference.ToString();
    }

    void PrintOutputAndClear()
    {
        using (System.IO.StreamWriter file =
            new System.IO.StreamWriter("Output.csv", true))
        {
            for (int i = 0; i < trackedItems.Count; i++)
            {
                file.WriteLine(trackedItems[i].GetTime() + "," + trackedItems[i].GetTrackable());
            }

            trackedItems.Clear();
        }
        
    }
}
