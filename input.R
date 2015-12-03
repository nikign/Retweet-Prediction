# require(RJSONIO)
# con = file("./1332460298038.json", "r")
# input <- readLines(con, -1L)
# training <- lapply(X=input,fromJSON)
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
  }
  else{
    as.null(df[t, "rt_user_fav_count"]) 
    as.null(df[t, "rt_user_stat_count"])
    as.null(df[t, "rt_user_loc"])
    as.null(df[t, "rt_user_id"]) 
  }
  
}
write.csv(df, './out.csv')


