# baby_sleep_feed_awake_graph
Shows baby's awake, feed, sleep cycle for the last 7 days on a graph. 

This becomes very useful in understanding and analyzing baby's daily pattern.

The script reads the awake, feed and sleep events of a baby from excel sheet. 

Excel sheet holds the time when a awake, feed or sleep event occured.

Output of the script is a line graph showing when baby was asleep, awake and feeding.

Also prints the total time for each of the event in a day.

Script
  
  1. Expects the excel sheet to give clock time showing hour and minutes
  
  2. Expects the events to be logged in increasing order of time within a day
  
  3. A day is assumed as 12:00am to 11:59pm
  
  4. First event in the list under a date is also assumed to be the event at 12:00am
  
  5. Last event in the list under a date is also assumed to be the event at 11:59pm
