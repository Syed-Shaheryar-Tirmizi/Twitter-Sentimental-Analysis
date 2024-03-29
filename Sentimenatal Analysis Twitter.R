library(twitteR)
library(tm)
library(syuzhet)
library(ggplot2)

consumer_key <-"Enter your key"
consumer_secret <- "Enter your key"
access_token <- "Enter your key"
access_secret <- "Enter your key"
setup_twitter_oauth(consumer_key,consumer_secret,access_token,access_secret)
a<- c("coronavirus","pakistan","filter:verified")
as.String(a)
a<-paste(a, collapse = " ")
tweets<-searchTwitter(a,n=100,lang = "en")
class(tweets)
dftweets<-twListToDF(tweets)
View(tweets)
text<-dftweets$text
text<-tolower(text)

cleanText<-gsub("^rt","",text)
cleanText<-gsub("#","",cleanText)
cleanText<-gsub("@\\w+","",cleanText)
cleanText<-gsub("http.*","",cleanText)
cleanText<-gsub("[[:punct:]]","",cleanText)
cleanText<-gsub("^ ","",cleanText)
cleanText<-gsub(" $","",cleanText)

corpusList<-Corpus(VectorSource(cleanText))
listt<-tm_map(corpusList,function(x) removeWords(x,stopwords()))

sentiments<-get_nrc_sentiment(as.character(listt))
View(sentiments)
data<-as.data.frame(colSums(sentiments))
View(data)
names(data)<-"Score"
data<-cbind("Sentiments"= rownames(data),data)
rownames(data)<-NULL

g<-ggplot(data=data, aes(x=Sentiments,y=Score))
g<-g+geom_bar(aes(fill=Sentiments),stat="identity")
g<-g+ ggtitle("Sentimental Analysis about Corona Virus")
g<-g+theme(plot.title = element_text(hjust = 0.5),text=element_text(size = 20), legend.position = "none")
print(g)

dev.copy(png,"Twitter sentiments.png", width=1080, height=720)
dev.off()

#knit("DS Project Report.Rmd")
a <- readLines()
