# Weather-Influenced-Tourism-App
This a web app developed using django and machine learning to suggest tourist places depending on weather condition.![](00_Website_Walk_Through.gif)
---
## Stepwise project implementation:
Grouping of weather data:
1. I researched 20 places with different weather conditions from one extreme to other.
2. Gathered past year's weather data of these 20 places using WeathermapAPI and requests library of Python.
3. Preprocessed the data and arranged in a consumable format by feature engineering and feature extraction.
4. Applied different clustering models namely K-means Clustering, DB-scan, Hierachical Clustering.
5. Since K-means had better so I went with K-means Clustering.
6. So, till now I had clustered all the weather data in 5 groups.
---
Getting co-ordinates of user inputed place and using co-ordinates to find the tourist places:
1. Then I used google maps keywords and classified them in weather groups based on my understanding.
2. Used free credits of Google Maps services and got access to Geocoding API (Geocoding API converts Address to Coordinates and vice-versa).
3. Now I can get coordinates of the place whenever a user inputs some place.
4. Then again I used current weather feature of Weather API  to get current weather of that place using the coordinates I got.
4. Also used Places API of google maps to find tourist attractions in that vicinity.
5. Then again I used current weather feature of Weather API  to get current weather of that place using the coordinates I got.
6. Filtered and formatted the weather data into a consumable format by the model.
7. Now applied the machine learning model to the weather data and found the suitable group for it.
8. And based on which group it was allotted, I could find relevant keywords for that kind of weather.
9. Used those keywords to filter places obtained earlier from Places API.

---
----> Displaying the results.
1. To provide a user friendly interface I used Django to build a web app.
2. You just need to enter the place you are interested in and rest will be handled internally.
3. Output gives Weather in that area and top 20 nearest relevant places with there name rating and address.
---
Industry scope  --> I think this idea have a huge scope in tourism industries with their marketing. Tourism companies can use this to attract customers and build a trust that even in some unlikely event they will get the best outcome of the situation.
---
Future improvements:
1. We can classify weather for a specific location and train them individually for tourist places in that area only.
2. Also to reduce complexity I just used Temperature, Cloud Percentage, Humidity and Weather description. We can add more weather parameters.
3. There are limited keywords in places API, we can use their descriptions and apply some NLP algorithms to filter them more effectively.
4. We can build a better recommendation system based on rating, distance, quality of reviews and popularity.
