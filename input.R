require(RJSONIO)
con = file("./1332460298038.json", "r")
input <- readLines(con, -1L)
training <- lapply(X=input,fromJSON)
library(igraph)

# dat=read.csv(file.choose(),header=FALSE)
# el=as.matrix(dat)
# el[,1]=as.character(el[,1])
# el[,2]=as.character(el[,2])
# el = el[,1:2]
# users_graph=graph.edgelist(el,directed=TRUE)
# set.vertex.attribute(users_graph,'retweeted_by' , value=0)
# set.vertex.attribute(users_graph,'retweeted_tweets' , value=0)
# set.vertex.attribute(users_graph,'total_tweets' , value=0)



df <- data.frame(user_id = numeric(),
                 retweet_count = numeric(),
                 hashtags = numeric(),
                 links = logical(),
                 mentions = logical(),
                 user_favorites = numeric(),
                 user_statuses = numeric(),
                 user_location = character(),
                 rt_user_fav_count = numeric(),
                 rt_user_stat_count = numeric(),
                 rt_user_loc = character(),
                 rt_user_id = numeric(),
                 stringsAsFactors = FALSE) 

for(t in 1:length(training)){
  df[t, "user_id"] <- training[[t]]$user$id
  df[t, "retweet_count"] <- training[[t]]$retweet_count
  df[t, "hashtags"] <- length(training[[t]]$entities$hashtags)
  df[t, "links"] <- FALSE
  users_graph = set.vertex.attribute(users_graph,'total_tweets' , df[t, "user_id"], value=get.vertex.attribute(users_graph, 'total_tweets', df[t, "user_id"]) + 1)
  if(length(training[[t]]$entities$urls$url)>0){
    df[t, "links"] <- TRUE
  }
  df[t, "mentions"] <- length(training[[t]]$entities$user_mentions)
  df[t, "user_favorites"] <- training[[t]]$user$favourites_count
  df[t, "user_statuses"] <- training[[t]]$user$statuses_count
  as.null(df[t, "user_location"])
  if(training[[t]]$user$geo_enabled==true() && length(training[[t]]$user$location)>0){
    
    df[t, "user_location"] <- training[[t]]$user$location
  }
    
  if(!is.null(training[[t]]$retweeted_status)){
    df[t, "rt_user_fav_count"] <- training[[t]]$retweeted_status$user$favourites_count
    df[t, "rt_user_stat_count"] <- training[[t]]$retweeted_status$user$statuses_count
    as.null(df[t, "rt_user_loc"])
    if(training[[t]]$retweeted_status$user$geo_enabled==true() && length(training[[t]]$retweeted_status$user$location)>0){
      df[t, "rt_user_loc"] <- training[[t]]$retweeted_status$user$location
    }
    df[t, "rt_user_id"] <- training[[t]]$retweeted_status$user$id
    users_graph = set.vertex.attribute(users_graph,'retweet_count' , df[t, "user_id"], value=get.vertex.attribute(users_graph, 'retweet_count', df[t, "user_id"]) + 1)
    users_graph = set.vertex.attribute(users_graph,'retweeted_by' , df[t, "rt_user_id"], value=get.vertex.attribute(users_graph, 'retweeted_by', df[t, "rt_user_id"]) + 1)

  }
  else{
    as.null(df[t, "rt_user_fav_count"]) 
    as.null(df[t, "rt_user_stat_count"])
    as.null(df[t, "rt_user_loc"])
    as.null(df[t, "rt_user_id"]) 
  }
  
}
write.csv(df, './out.csv')


