

library(tidyverse)

setwd('E:\\backup_8112020\\Thesis FEP\\code_thesis')

index_data <- read_csv('data\\index_data.csv')

index_data %>% 
  filter(date > '2008-01-01') %>%
  mutate(crisis = ifelse(date < '2013-04-01', 'subprime', 
                         ifelse(date > '2020-01-01', 'covid', 'normal'))) %>% 
  ggplot(aes(x = date, colour = crisis)) +
  geom_point(aes(y = index), size = 3, alpha = .4) +
  geom_smooth(aes(y = index), size = 1.5, method = 'lm', se=TRUE) +
  theme_minimal()
