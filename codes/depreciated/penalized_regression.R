# script providing penalized regressions:
# 
# LASSO, RIDGE, ELASTIC NET
# 
# Gustavo Vital

# Packages
library(tidyverse)
library(caret)
library(glmnet)

# set wd ----
setwd('C:/Users/gusta/Documents/mestrado/dissertation/thesis_code/')

# read dataset ----
data <- read_csv('data\\data_model.csv')

normal_index_n <- (data$lm_negative - mean(data$lm_negative))/(sd(data$lm_negative))
normal_index_p <- (data$lm_positive - mean(data$lm_positive))/(sd(data$lm_positive))
 



acum <- function(serie) {
  
  acum <- c()
  acum[1] <- serie[1]
  
  for(indice in 2:length(serie)) {
    acum[indice] <- (acum[indice - 1])*(1 + serie[indice]/100)
  }
  acum <- (acum - 1)
  return(acum)
}

normalize <- function(x){
  (x - min(x, na.rm = TRUE))/(max(x, na.rm = TRUE) - min(x, na.rm = TRUE))
}


teste <- data.frame('date'=data$date, 
                    'cps' = (data$cps),
                    'index'=(acum(normal_index_n)),
                    'covid' =data$covid,
                    'cpi' = data$cpi)

teste <- data.frame(teste, 
                    'cps_1' = lag(teste$cps, 1),
                    'cps_2' = lag(teste$cps, 2),
                    'cps_3' = lag(teste$cps, 3),
                    'cps_4' = lag(teste$cps, 4),
                    'cps_5' = lag(teste$cps, 5),
                    'cps_6' = lag(teste$cps, 6),
                    'cps_7' = lag(teste$cps, 7),
                    'index_1' = lag(teste$index, 1),
                    'index_2' = lag(teste$index, 2),
                    'index_3' = lag(teste$index, 3),
                    'index_4' = lag(teste$index, 4),
                    'index_5' = lag(teste$index, 5), 
                    'index_6' = lag(teste$index, 6),
                    'index_7' = lag(teste$index, 7),
                    'index_8' = lag(teste$index, 8),
                    'index_9' = lag(teste$index, 9),
                    'index_10' = lag(teste$index, 10),
                    'index_11' = lag(teste$index, 11),
                    'index_12' = lag(teste$index, 12))



# teste %>% 
#   # filter(date > as.Date('2010-01-01')) %>% 
#   ggplot(aes(x=date)) +
#   geom_line(aes(y=index_12), colour='dodgerblue') +
#   geom_line(aes(y=cps))






for(num in 1:7){
  for(i in 1:12){
    for(j in 1:12){
      for(k in 1:12){
        for(l in 1:12){
          for(m in 1:12){
            for(n in 1:12){
              if(num == 2){
                model <- summary(lm(cps ~ lag(index, i) + lag(cps, j), data = teste))
              } else if(num == 3){
                model <- summary(lm(cps ~ lag(index, i) + lag(cps, j) + lag(cps, k), data = teste))
              } else if(num == 4){
                model <- summary(lm(cps ~ lag(index, i) + lag(cps, j) + lag(cps, k) + lag(cps, l), data = teste))
              } else if(num == 5){
                model <- summary(lm(cps ~ lag(index, i) + lag(index, m) + lag(cps, j), data = teste))
              } else if(num == 6){
                model <- summary(lm(cps ~ lag(index, i) + lag(index, m) + lag(index, n) + lag(cps, j), data = teste))
              } else if(num == 7){
                model <- summary(lm(cps ~ lag(index, i) + lag(index, m) + lag(cps, j) + lag(cps, k), data = teste))
              } else {
                model <- summary(lm(cps ~ lag(index, i) + lag(index, m) + lag(index, n) +
                                      lag(cps, j) + lag(cps, k) + lag(cps, l), data = teste))
              }
              
              if(dim(model[["coefficients"]])[1] == 3){
                if(model[["coefficients"]][2,4] < 0.1 & 
                   model[["coefficients"]][3,4] < 0.1){
                  
                  print(model)
                  print(paste('Model: i', i,'m', m, 'j', n, 'j', j, 'k', k, 'l', l))
                  
                }
                
              } else if(dim(model[["coefficients"]])[1] == 4){
                if(model[["coefficients"]][2,4] < 0.1 & 
                   model[["coefficients"]][3,4] < 0.1 &
                   model[["coefficients"]][4,4] < 0.1){
                  
                  print(model)
                  print(paste('Model: i', i,'m', m, 'j', n, 'j', j, 'k', k, 'l', l))
                }
                
              } else if(dim(model[["coefficients"]])[1] == 5){
                if(model[["coefficients"]][2,4] < 0.1 & 
                   model[["coefficients"]][3,4] < 0.1 &
                   model[["coefficients"]][4,4] < 0.1 &
                   model[["coefficients"]][5,4] < 0.1){
                  
                  print(model)
                  print(paste('Model: i', i,'m', m, 'j', n, 'j', j, 'k', k, 'l', l))
                }
                
              } else if(dim(model[["coefficients"]])[1] == 6){
                if(model[["coefficients"]][2,4] < 0.1 & 
                   model[["coefficients"]][3,4] < 0.1 &
                   model[["coefficients"]][4,4] < 0.1 &
                   model[["coefficients"]][5,4] < 0.1 &
                   model[["coefficients"]][6,4] < 0.1){
                  
                  print(model)
                  print(paste('Model: i', i,'m', m, 'j', n, 'j', j, 'k', k, 'l', l))
                }
              }
            }
          }
        }
      }
    }
  }
}


for(i in 1:12){
  for(j in 1:12){
    
  }
}




for(i in 1:5){
    for(k in 1:6){
      
      model <- summary(lm(cps ~ lag(index, i) + lag(index, (i + 1)) + lag(cps, k) + lag(cpi, k) + covid, teste))
      
      if(model[["coefficients"]][2,4] < 0.1 & 
         model[["coefficients"]][3,4] < 0.1 &
         model[["coefficients"]][4,4] < 0.1){
        
        print(model)
        print(paste0('Model: CPS = Index_', i, ' + Index_', (i+1), ' + CPS_', k, ' + CPI_',k, ' + COVID + e'))
      }
    }
  }





















modelo <- summary(lm(cps ~ cps_2  + index_12, teste))
summary(lm(cps ~ I(lag(cps))  + index_12, teste))



modell <- lm(cps ~ cps_1, teste)
















# train and test data ----
train.sample <- data$cps %>% 
  createDataPartition(p=0.8, list = FALSE)

train.data <- data[train.sample, ]  
test.data <- data[-train.sample, ]  
  
  
  
  
  
  
  
