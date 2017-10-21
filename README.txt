ADD:
- Your name
- Your UMID
- Instructions on how to run your submission
- Anything else that we need to know to grade your submission

*** Alexander Shell - DarkSky Net - 54532242 ***

*** Code Summary ***
The code for my chat bot begins with setting up caching in order to store weather data for future use. When weather data is fetched for a city, this stores it so it can be looked up there instead of having to process another request with an API. Then functions for getting the coordinates for cities from Google Maps API and then using those coordinates to get weather data for that location from DarkSky Net API. Next are a series of functions for extracting out the particular weather data when prompted such as temperature from the requested json weather file. The kernel pattern is used to group certain phrases with these functions to return the right data for the given prompt. Next a while loop is used with raw input to keep the chat bot responding to the user until is broken by 'exit'.

 *** Running the Chat Bot ***
- My program runs correctly to request the appropriate weather data from the API and relay it when connected to wifi:

> hello
What can I call you?
> Alex
Nice to meet you Alex.
> Are you a robot?
How did you know I am a machine?
> What's the weather like in Detroit?
In Detroit, it is 50.06 and Partly Cloudy
> How hot will it get in Ann Arbor this week?
In Ann Arbor it will reach 76.53.
> Is it going to rain in Paris today?
It almost definitely will not rain in Paris.
> What's the weather like in FJDKSJFDSK?
I FJDKSJFDSK a city?
> What's the weather like in Los Angelos?
In Los Angelos, it is 62.41 and Partly Cloudy
> Is it going to rain in Vancouver today?
It almost definitely will not rain in Vancouver.
> How hot will it get in Calgary this week?
In Calgary it will reach 60.99.

- My program caches the data from requested cities so it can access it even when offline:

> How hot will it get in Detroit this week?
In Detroit it will reach 71.79.
> What's the weather like in Ann Arbor?
In Ann Arbor, it is 50.56 and Mostly Cloudy
> How hot will it get in FJDKSJFDSK this week?
Is FJDKSJFDSK a city?
> What's the weather like in Paris?
In Paris, it is 26.82 and Clear
> What's the weather like in Vancouver?
In Vancouver, it is 47.9 and Clear

- My programs accepts all required query types from the user:

> What's the weather like in Ann Arbor?
In Ann Arbor, it is 50.56 and Mostly Cloudy
> Is it going to rain in Ypsilanti today?
It almost definitely will not rain in Ypsilanti.
> How hot will it get in Detroit today?
In Detroit today, it will reach a high of 64.45.
> How cold will it get in Flint today?
In Flint today, it will reach a low of 35.88.
> Is it going to rain in East Lansing this week?
It will almost definitely rain in East Lansing this week.
> How hot will it get in Grand Rapids this week?
In Grand Rapids it will reach 73.19.
> How cold will it get in Kalamazoo this week?
In Kalamazoo it will reach 34.27.
