library(MASS)

data <- read.csv('final_data.csv')
data <- as.data.frame(data)
data <- data[c(1, 2, 3, 5, 6, 7)]

apply(data,2,function(x) sum(is.na(x)))
index <- sample(1:nrow(data),round(0.8*nrow(data)))
train <- data[index,]
test <- data[-index,]

# regression
# lm.fit <- glm(rt_count~., data=train)
# summary(lm.fit)
# pr.lm <- predict(lm.fit,test)
# MSE.lm <- sum((pr.lm - test$rt_count)^2)/nrow(test)

#normalization
maxs <- apply(data, 2, max) 
mins <- apply(data, 2, min)
scaled <- as.data.frame(scale(data, center = mins, scale = maxs - mins))
train_ <- scaled[index,]
test_ <- scaled[-index,]
 
library(grid) 
library(neuralnet)

print('training')
#train
n <- names(train_)
f <- as.formula(paste("rt_count ~", paste(n[!n %in% "rt_count"], collapse = " + ")))
nn2 <- neuralnet(f,data=train_,hidden=c(2),linear.output=F)
print('testing')
#test
pr.nn2 <- compute(nn2,test_[1:5]) 
pr.nn2_ <- pr.nn2$net.result*(max(data$rt_count)-min(data$rt_count))+min(data$rt_count)
test.r <- (test_$rt_count)*(max(data$rt_count)-min(data$rt_count))+min(data$rt_count)
MSE.nn2 <- sum((test.r - pr.nn2_)^2)/nrow(test_)
print(paste(MSE.nn2))

#plot the results
# plot(test$rt_count,pr.nn2_,col='red',main='Real vs predicted NN2',pch=18,cex=0.7)
# abline(0,1,lwd=2)
# legend('bottomright',legend='NN2',pch=18,col='red', bty='n')


# 
# 
#cross validation
set.seed(450)
cv.error <- NULL
k <- 10

library(plyr) 
pbar <- create_progress_bar('text')
pbar$init(k)

for(i in 1:k){
    print('crossvalidation: ', k)
    index <- sample(1:nrow(data),round(0.8*nrow(data)))
    train.cv <- scaled[index,]
    test.cv <- scaled[-index,]
    
    nn2 <- neuralnet(f,data=train.cv,hidden=c(2),linear.output=F)
    
    pr.nn2 <- compute(nn2,test.cv[,1:5])
    pr.nn2 <- pr.nn2$net.result*(max(data$rt_count)-min(data$rt_count))+min(data$rt_count)
    
    test.cv.r <- (test.cv$rt_count)*(max(data$rt_count)-min(data$rt_count))+min(data$rt_count)
    
    cv.error[i] <- sum((test.cv.r - pr.nn2)^2)/nrow(test.cv)
    
    pbar$step()
}
print(mean(cv.error))