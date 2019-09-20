import http.client
import json
import time
import sys
import collections


api_key = str(sys.argv[1])



conn = http.client.HTTPSConnection("api.themoviedb.org")
payload ="{}"
start = time.time()
write_file = open('movie_ID_name.csv','w')
similar_file = open('movie_ID_sim_movie_ID.csv','w')
similar_movies=[]
movieCT=0

#test_file = open('test.csv','w')
for i in range(1,19):
    conn.request("GET", "/3/discover/movie?api_key="+api_key+"&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page="+str(i)+"&primary_release_date.gte=2004&with_genres=18", payload)
    res = conn.getresponse()
    data = res.read()

    data = json.loads(data)
    for k in data:
        if k == 'results':
            movies = data[k]
            for item in movies:
                if movieCT < 350:
                    row = [item['id'],item['title']]
                    if ',' in item['title']:
                        write_file.write(str(item['id']) +','+"\""+ str(item['title']) + "\"")
                    else:
                        write_file.write(str(item['id']) +','+ str(item['title']))
                    write_file.write('\n')
                    movieCT = movieCT + 1
                    conn.request("GET", "/3/movie/"+str(item['id'])+"/similar?page=1&language=en-US&api_key="+api_key, payload)
                    res_similar = conn.getresponse()
                    data_similar = res_similar.read()
                    data_similar = json.loads(data_similar)
                    time.sleep(1/3)
                    count =0
                    for x in data_similar:
                        if x == 'results':
                            movies_similar = data_similar[x]
                            for similar in movies_similar:
                                if count < 5:
                                    similar_movies.append([item['id'],similar['id']])
                                    count = count + 1
                                    #test_file.write(str(item['id'])+','+str(similar['id']))
                                    #test_file.write('\n')
                                
            
write_file.close()
#test_file.close()                
   
matchList = ['']*len(similar_movies)
myList = []
for x in range(len(similar_movies)):
    duplicate = ''
    for y in range(len(similar_movies)):
        if similar_movies[x][0] == similar_movies[y][1] and similar_movies[x][1] == similar_movies[y][0]:
            duplicate = 'Yes'
    if duplicate == 'Yes':
        matchList[x] = 'Duplicate'
    else:
        matchList[x] = 'Unique'


        
                   
                    

for i in range(len(similar_movies)):
    if matchList[i] == 'Duplicate': #
        for j in range(len(similar_movies)):
            if similar_movies[i][0] == similar_movies[j][1] and similar_movies[i][1] == similar_movies[j][0]:
                if similar_movies[i][0] < similar_movies[j][0]:
                    myList.append([similar_movies[i][0],similar_movies[i][1]])
    else:
        myList.append([similar_movies[i][0],similar_movies[i][1]])
                
for i in range(len(myList)):
    similar_file.write(str(myList[i][0])+','+str(myList[i][1]))
    similar_file.write('\n')
similar_file.close()

end = time.time()
#print('Total Time', end-start)