using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;

public class CSVOptionParser
{
    private Dictionary<string, string> optionMap;

    public CSVOptionParser(string fileName)
    {
        try
        {
            string line;

            optionMap = new Dictionary<string, string>();

            // Read the file and display it line by line.  
            System.IO.StreamReader file = new System.IO.StreamReader(fileName);
            while ((line = file.ReadLine()) != null)
            {
                //System.Console.WriteLine(line);
                string[] splitLine = line.Split(',');

                Debug.Log(splitLine.Length + " " + splitLine[0] + " " + splitLine[1]);

                if (splitLine.Length == 2)
                {
                    optionMap.Add(splitLine[0], splitLine[1]);
                }
                else
                {
                    // Something is formatted wrong! TODO: Maybe throw?
                }
            }

            file.Close();
        }
        catch(Exception e)
        {
            Debug.LogError(e.ToString());
        }
    }

    public int GetIntOption(string optionName)
    {
        string stringValue = GetStringOption(optionName);

        if(stringValue.Length > 0)
        {
            int outputInt;
            if (Int32.TryParse(stringValue, out outputInt))
            {
                return outputInt;
            }
            else
            {
                Debug.LogError("Could not parse int from option " + optionName);
            }
        }

        return 0;
    }

    public float GetFloatOption(string optionName)
    {
        string stringValue = GetStringOption(optionName);

        if (stringValue.Length > 0)
        {
            float outputFloat;
            if (Single.TryParse(stringValue, out outputFloat))
            {
                return outputFloat;
            }
            else
            {
                Debug.LogError("Could not parse float from option " + optionName);
            }
        }

        return 0;
    }

    public string GetStringOption(string optionName)
    {
        string optionValue;
        if (optionMap.TryGetValue(optionName, out optionValue))
        {
            return optionValue;
        }
        else
        {
            Debug.LogError("Option name " + optionName + " does not exist.");
            return "";
        }
    }
}
