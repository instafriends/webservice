## Instafriends - webservice

After running instafriends using php for some months I realized that it was consuming too much of my server. 

The problem was happening when the app had to get all the user that followed and the ones that were followed by the user. The Instagram API returns just 100 user at time, so the app need to make a lot of requests at the Instagram API. And it was became expensive to my server.

So I decided to start using Google App Engine and let it make the hard work, this is the python file that do that and returns a json file.