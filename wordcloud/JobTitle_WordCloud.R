library(wordcloud)
library(RColorBrewer)

x <- read.csv('~/GA-class/MyProject/cleanOrderedTitleWords.csv', header=F, sep = ",")

names(x) <- c("words", "count")

png("TitleWordC.png", width=1280,height=800)
wordcloud(x$words, # words
          x$count, # frequencies
          scale = c(10,2), # size of largest and smallest words
          colors = brewer.pal(8,"Dark2"), # number of colors, palette
          min.freq=1,
          #max.freq=20,
          maxWords = Inf,
          rot.per = .15) # proportion of words to rotate 90 degrees
dev.off()