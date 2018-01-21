# WikiWorld

## How to run it

Navigate to the "Data Generator" folder and run the command `python3 [person name] [degrees of separation] [# connections per degree]`

Then navigate to the "Web Side" folder and run `python3 -m http.server 8080`

Finally, go to localhost:8080 in your favorite web browser!

## Inspiration
We thought that there was a lot of fantastic information out there in the world, but it was stuck inside huge chunks of text that involved a lot of work to analyze. So, we started to wonder if we could help break it down and visualize it with nice graphics. Our minds wandered towards visualizing parts of Wikipedia, and after looking around for nice visualizations, we couldn't find any! So we decided we needed to make our own.

## What it does
It starts from a person and starts spanning out a variety of people related to that person. It uses an Algorithm similar to Google's PageRank to look through their wikipedia page and find important people and helps you visualize some of their degrees of separation.

## How We built it
The database of people is constructed using Python and a variety of Wikipedia's different APIs. We then apply our algorithms to decide who to visualize and who to prioritize before visualizing the graph on the screen!

## What's next for WikiWorld
This is a minimum viable product to show that connections between people can indeed be found. Going forward, we'd like to work to make these connections more relevant and make the visualization more powerful and useful!
