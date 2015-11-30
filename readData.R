library(myd)
url <- './1332460298038.json'
raw.data <- readLines(url, warn = "F")
l = list()
s = '['
#for(i in raw.data){
for(i in raw.data){
  #r <- fromJSON(i)
  if (s == '['){
    s = paste(s, raw.data[i], sep ="" )
  }
  else{
    s = paste(s, raw.data[i], sep ="," )
  }
  
  #l = append(l, r)
}
#s = substr(s, 1, length(s)-1)
s = paste(s, "]", collapse = "")
mydf <- fromJSON(s, )
