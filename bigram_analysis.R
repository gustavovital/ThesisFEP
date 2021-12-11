setwd('E:\\backup_8112020\\Thesis FEP\\code_thesis')

# Required libraries ----
library(tidyverse)
library(tidytext)
library(qdap)
library(tm)
library(zoo)

# Data ----
press_data <- read_csv('data\\press_data.csv')

# Tokenization ----

bigram_total <- press_data %>% 
  unnest_tokens(bigram, Doc, token = 'ngrams', n = 2) %>% 
  count(bigram, sort = TRUE) %>% 
  separate(bigram, c('term1', 'term2'), sep = ' ') %>% 
  
  filter(!term1 %in% stopwords()) %>% 
  filter(!term2 %in% stopwords()) %>% 
  
  arrange(desc(n)) %>% 
  mutate(Terms = paste(term1, term2)) %>% 
  select(Terms, n)


# Tokenization for periods

press_data$Text <- press_data$Doc
press_data$Doc <- 1:nrow(press_data)

bigram_data <- data.frame(Terms=character(),
                          n = integer(),
                          Id = integer(),
                          Date = as.Date(character()))


for(text in 1:nrow(press_data)){
  
  bigram <- press_data[text, ] %>% 
    unnest_tokens(bigram, Text, token = 'ngrams', n = 2) %>% 
    count(bigram, sort = TRUE) %>% 
    separate(bigram, c('term1', 'term2'), sep = ' ') %>% 
    
    filter(!term1 %in% stopwords()) %>% 
    filter(!term2 %in% stopwords()) %>% 
    
    arrange(desc(n)) %>% 
    mutate(Terms = paste(term1, term2)) %>% 
    select(Terms, n)
  
  bigram$Doc <- press_data$Doc[text]
  bigram$Date <- press_data$Dates[text]
  bigram_data <- rbind(bigram_data, bigram)
  
}    

bigram_data %>% 
  filter((Terms == 'monetary policy' |
           Terms == 'euro area' |
            Terms == 'governing council' |
            Terms == 'price stability' |
            Terms == 'interest rates' |
            Terms == 'inflation expectations') &
           n > 1 & Date > as.Date('2008-01-01')) %>% 
  ggplot(aes(x = Date, y = rollmean(n, 10, na.pad = TRUE), color = Terms)) +
  geom_line()
