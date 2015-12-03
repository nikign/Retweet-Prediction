# setwd("~/Documents/niki/StreamingAPITrackData")

# require(RJSONIO)
# con = file("./1332460298038.json", "r")
# input <- readLines(con, -1L)
# training <- lapply(X=input,fromJSON)
# library(igraph)

print("load done")

# dat=read.csv(file.choose(),header=FALSE)
# el=as.matrix(dat)
# el[,1]=toString(as.character(el[,1]))
# el[,2]=toString(as.character(el[,2]))
# el = el[,1:2]
# users_graph=graph.edgelist(el,directed=TRUE)
# set.vertex.attribute(users_graph,'retweeted_by' , value=0)
# set.vertex.attribute(users_graph,'retweeted_tweets' , value=0)
# set.vertex.attribute(users_graph,'total_tweets' , value=0)

retweeted_by = {}
total_tweets = {}
retweet_count = {}


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
  #print(t)
  df[t, "user_id"] <- training[[t]]$user$id
  df[t, "retweet_count"] <- training[[t]]$retweet_count
  df[t, "hashtags"] <- length(training[[t]]$entities$hashtags)
  df[t, "links"] <- FALSE
  id_str = toString(df[t, "user_id"])
 # users_graph = set.vertex.attribute(users_graph,'total_tweets' ,id_str, value=get.vertex.attribute(users_graph, 'total_tweets', id_str) + 1)
  if (id_str %in% names(total_tweets)){

    total_tweets[id_str] = total_tweets[id_str] + 1
  }
  else{
    total_tweets[id_str] = 1
  }
  if(length(training[[t]]$entities$urls$url)>0){
    df[t, "links"] <- TRUE
  }
  df[t, "mentions"] <- length(training[[t]]$entities$user_mentions)
  df[t, "user_favorites"] <- training[[t]]$user$favourites_count
  df[t, "user_statuses"] <- training[[t]]$user$statuses_count
  as.null(df[t, "user_location"])

  if(!is.null(training[[t]]$retweeted_status)){
    df[t, "rt_user_fav_count"] <- training[[t]]$retweeted_status$user$favourites_count
    df[t, "rt_user_stat_count"] <- training[[t]]$retweeted_status$user$statuses_count
    as.null(df[t, "rt_user_loc"])

    df[t, "rt_user_id"] <- training[[t]]$retweeted_status$user$id
    
    if(id_str %in% names(retweet_count)){
      retweet_count[id_str] = retweet_count[id_str] + 1
    }
    else{
      retweet_count[id_str] = 1
    }
    rt_id_str = toString(df[t, "rt_user_id"])
    if(rt_id_str %in% names(retweeted_by)){

      retweeted_by[rt_id_str] = retweeted_by[rt_id_str] + 1
    }
    else{
      retweeted_by[rt_id_str] = 1
    }
    # users_graph = set.vertex.attribute(users_graph,'retweet_count' , df[t, "user_id"], value=get.vertex.attribute(users_graph, 'retweet_count', df[t, "user_id"]) + 1)
    # users_graph = set.vertex.attribute(users_graph,'retweeted_by' , df[t, "rt_user_id"], value=get.vertex.attribute(users_graph, 'retweeted_by', df[t, "rt_user_id"]) + 1)

  }
  else{
    as.null(df[t, "rt_user_fav_count"]) 
    as.null(df[t, "rt_user_stat_count"])
    as.null(df[t, "rt_user_loc"])
    as.null(df[t, "rt_user_id"]) 
  }
  
}
write.csv(df, './out.csv')


