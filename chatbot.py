import aiml
import os
import requests
import json

# Setting up caching
CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

# Function to cache URLs
def getWithCaching(baseURL, params={}):
    req = requests.Request(method = 'GET', url=baseURL, params = sorted(params.items()))
    prepped = req.prepare()
    fullURL = prepped.url

    if fullURL not in CACHE_DICTION:
        response = requests.Session().send(prepped)
        CACHE_DICTION[fullURL] = response.text
        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()

    return CACHE_DICTION[fullURL]

# kernel is responsible for responding to suers
kernel = aiml.Kernel()

# load every aiml file in the 'standard' directory
# use os.listdir and a for loop to do this
for file in os.listdir('aiml_data'):
    kernel.learn(os.path.join('aiml_data', file))

kernel.learn(os.path.join('aiml_data', 'std-hello.aiml'))

# Function for requesting data from Google API
def reqGoogle(city):
    try:
        google_base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        google_api_key = 'AIzaSyC-7A1pLcaYS-hLYu-21NkZFXYltMLZ42Y'
        google_cache = getWithCaching(google_base_url, params=
        {
        'address': city, 'key': google_api_key
        })
        google_data = json.loads(google_cache)
        #print json.dumps(google_data, indent=4)
        coordinates = (google_data['results'][0]['geometry']['location']['lat'], google_data['results'][0]['geometry']['location']['lng'])
        return coordinates # returns tuple with lat and lng
    except:
        return 'Is {} a city?'.format(city)

# Function for requesting data from DarkSky Net API
def reqDarkSky(city):
    try:
        lat_lng = reqGoogle(city)
        darksky_base_url = 'https://api.darksky.net/forecast/'
        darksky_api_key = 'e5617eb09fadb996c0bbd0a4a5735a14'
        darksky_full_url=darksky_base_url + darksky_api_key + '/' + str(lat_lng[0]) + ',' + str(lat_lng[1])
        darksky_cache = getWithCaching(darksky_full_url)
        darksky_data = json.loads(darksky_cache)
        #print json.dumps(darksky_data, indent=4)
        return darksky_data # returns dictionary of weather report
    except:
        return "Sorry, I don't know"

# add a new response for when the user says "example * and *"
# note that the ARGUMENT NAMES (first and second) must match up with
# the names in kernel.addPattern
def exampleResponse(city, state):
    return '{} eh? Do you like it in {}?'.format(state, city)
kernel.addPattern("I live in {city}, {state}", exampleResponse)

# Function for "What's the weather like in {}?"
def weatherislike(city):
    try:
        weather_data = reqDarkSky(city)
        current_temp = weather_data['currently']['apparentTemperature']
        condition = weather_data['currently']['summary']
        return 'In {}, it is {} and {}'.format(city, current_temp, condition)
    except:
        return 'I {} a city?'.format(city)
kernel.addPattern("What's the weather like in {city}?", weatherislike)

# Function for "Is it going to rain in {} today?"
def raintoday(city):
    try:
        rain_data = reqDarkSky(city)
        rain_prob = rain_data['currently']['precipProbability']
        if rain_prob < 0.1:
            return 'It almost definitely will not rain in {}.'.format(city)
        elif rain_prob >= 0.1 and rain_prob < 0.5:
            return 'It probably will not rain in {}.'.format(city)
        elif rain_prob >= 0.5 and rain_prob < 0.9:
            return 'It probably will rain in {}.'.format(city)
        elif rain_prob >= 0.9:
            return 'It will almost definitely rain in {}.'.format(city)
    except:
            return 'I {} a city?'.format(city)
kernel.addPattern("Is it going to rain in {city} today?", raintoday)

# Function for "How hot will it get in {} today?"
def maxTempToday(city):
    try:
        temp_data = reqDarkSky(city)
        temp_max = temp_data['daily']['data'][0]['temperatureMax']
        return 'In {} today, it will reach a high of {}.'.format(city, temp_max)
    except:
        return 'I {} a city?'.format(city)
kernel.addPattern("How hot will it get in {city} today?", maxTempToday)

# Function for "How cold will it get in {} today?
def minTempToday(city):
    try:
        temp_data = reqDarkSky(city)
        temp_min = temp_data['daily']['data'][0]['temperatureMin']
        return 'In {} today, it will reach a low of {}.'.format(city, temp_min)
    except:
        return 'I {} a city?'.format(city)
kernel.addPattern("How cold will it get in {city} today?", minTempToday)

# Function for "Is it goin to rain in {} this week?"
def rainWeekProb(city):
    try:
        rain_data = reqDarkSky(city)['daily']['data']
        weekly_prob = (1 - rain_data[0]['precipProbability'])
        for day in range(1,8):
            weekly_prob *= (1 - rain_data[day]['precipProbability'])
        week_rain_prob = 1 - weekly_prob
        if week_rain_prob < 0.1:
            return 'It almost definitely will not rain in {} this week.'.format(city)
        elif week_rain_prob >= 0.1 and week_rain_prob < 0.5:
            return 'It probably will not rain in {} this week.'.format(city)
        elif week_rain_prob >= 0.5 and week_rain_prob < 0.9:
            return 'It probably will rain in {} this week.'.format(city)
        elif week_rain_prob >= 0.9:
            return 'It will almost definitely rain in {} this week.'.format(city)
    except:
        return 'I {} a city?'.format(city)
kernel.addPattern("Is it going to rain in {city} this week?", rainWeekProb)

# Function for "How hot will it get in {} this week?"
def maxTempWeek(city):
    try:
        temp_data = reqDarkSky(city)['daily']['data']
        weekly_max_temp = temp_data[0]['temperatureMax']
        for day in range(1,8):
            if temp_data[day]['temperatureMax'] > weekly_max_temp:
                weekly_max_temp = temp_data[day]['temperatureMax']
        return 'In {} it will reach {}.'.format(city, weekly_max_temp)
    except:
        return 'Is {} a city?'.format(city)
kernel.addPattern("How hot will it get in {city} this week?", maxTempWeek)

# Function for "How cold will it get in {} this week?"
def minTempWeek(city):
    try:
        temp_data = reqDarkSky(city)['daily']['data']
        weekly_min_temp = temp_data[0]['temperatureMin']
        for day in range(1,8):
            if temp_data[day]['temperatureMin'] < weekly_min_temp:
                weekly_min_temp = temp_data[day]['temperatureMin']
        return 'In {} it will reach {}.'.format(city, weekly_min_temp)
    except:
        return 'I {} a city?'.format(city)
kernel.addPattern("How cold will it get in {city} this week?", minTempWeek)

user_input = ''
while user_input != 'exit':
    user_input = raw_input('> ')
    print(kernel.respond(user_input))

 # get a few example responses
#print('Example queries:\n')
#queries = ['hello', 'Alexander', 'I live in Ann Arbor, Michigan', "What's the weather like #in Detroit?", 'Is it going to rain in Ypsilanti today?', 'How hot will it get in Detroit #today?', 'How cold will it get in Flint today?', 'Is it going to rain in East Lansing this #week?', 'How hot will it get in Grand Rapids this week', 'How cold will it get in #Kalamazoo this week']
#for q in queries:
    #print('> {}'.format(q))
    #print('...{}\n'.format(kernel.respond(q)))
