# File for figures
#
# Gustavo Vital

# Packages
# install.packages(c('tidyverse', 'patchwork'))

library(tidyverse)
library(patchwork)
library(zoo)

# Add correlation plot ----
data <- read_csv('data\\data.csv')

# cpi_cps <- data %>%
#   ggplot(aes(cpi, cps)) +
#   geom_point() +
#   geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
#   labs(x = 'Consumer Price Index',
#        y = 'Consumer Opinion Surveys: Consumer Prices') +
#   theme_minimal()
#
# cpi_vader <- data %>%
#   ggplot(aes(cpi, vader_positive)) +
#   geom_point() +
#   geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
#   labs(x = 'Consumer Price Index',
#        y = 'VADER Positive sentiment') +
#   theme_minimal()
#
# cpi_lm <- data %>%
#   ggplot(aes(cpi, lm_positive)) +
#   geom_point() +
#   geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
#   labs(x = 'Consumer Price Index',
#        y = 'Loughran-McDonald Positive Sentiment') +
#   theme_minimal()
#
# vader_loughram <- data %>%
#   ggplot(aes(vader_positive, lm_positive)) +
#   geom_point() +
#   geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
#   labs(x = 'VADER Positive sentiment',
#        y = 'Loughran-McDonald Positive Sentiment') +
#   theme_minimal()
#
# cps_vader <- data %>%
#   ggplot(aes(cps, vader_positive)) +
#   geom_point() +
#   geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
#   labs(x = 'Consumer Price Index',
#        y = 'VADER Positive sentiment') +
#   theme_minimal()
#
# cps_lm <- data %>%
#   ggplot(aes(cps, lm_positive)) +
#   geom_point() +
#   geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
#   labs(x = 'Consumer Opinion Surveys: Consumer Prices',
#        y = 'Loughran-McDonald Positive Sentiment') +
#   theme_minimal()
#
# (cpi_lm + cpi_vader + cpi_cps) / (cps_lm + cps_vader + vader_loughram)

# rm(list = lm())

# consumer sentiment ----

normalize <- function(x){
  (x - min(x, na.rm = TRUE))/(max(x, na.rm = TRUE) - min(x, na.rm = TRUE))
}

# acum <- function(serie) {
#
#   acum <- c()
#   acum[1] <- serie[1]
#
#   for(indice in 2:length(serie)) {
#     acum[indice] <- (acum[indice - 1])*(1 + serie[indice]/100)
#   }
#   acum <- (acum - 1)
#   return(acum)
# }

# plot(data$date, rollmean(data$vader_positive, k = 12), type='l')

# data %>%
#   ggplot(aes(x = normalize(cps))) +
#   geom_line(aes(y = normalize(vader_positive)), size = .3, colour = 'dodgerblue3')
#   # geom_line(aes(y = normalize(cps)), size = .3, colour = 'tomato2')

data %>%
  filter(date > '2010-01-01' & date < '2021-01-01') %>%
  ggplot(aes(x = date)) +
  geom_point(aes(y = normalize(rollmean((lm_positive + vader_positive)/2, k = 12, fill = NA, align = 'right'))),
             colour = 'dodgerblue4', size = 2, alpha=.6) +
  geom_line(aes(y = normalize(rollmean((lm_positive + vader_positive)/2, k = 12, fill = NA))),
             colour = 'dodgerblue4', size = 1, alpha=.6) +
  geom_smooth(aes(y = normalize(rollmean((lm_positive + vader_positive)/2, k = 12, fill = NA))),
             colour = 'dodgerblue2', size = .3, alpha=.6, se = FALSE) +
  # geom_line(aes(y = normalize(rollmean(vader_positive, k = 12, fill = NA)))) +
  # geom_line(aes(y = rollmean(as.numeric(normalize(lm_positive)), k = 12, fill = NA))) +
  geom_point(aes(y = normalize(cps)), colour = 'tomato2', size = 2, alpha=.6) +
  geom_line(aes(y = normalize(cps)), colour = 'tomato2', size = 1, alpha=.6) +
  geom_smooth(aes(y = normalize(cps)), colour = 'tomato4', size = .3, alpha=.6, se = FALSE)


data.teste <-
  data.frame('indice' = rollmean((data$lm_positive + data$vader_positive)/2,
                                 k = 12, fill = NA, align = 'right'),
             'date' = as.Date(data$date),
             'cps' = data$cps,
             'cpi' = data$cpi, 'gdp' = data$gdp_gap,
             'interest' = data$interest)

data %>%
  # filter(date >= '2012-04-01' & date < '2017-12-01') %>%
  ggplot(aes(x = date)) +
  geom_line(aes(y = normalize(rollmean(vader_positive, k=12, fill = NA, align = 'right'))),
            colour='tomato4') +
  geom_line(aes(y = normalize(rollmean(lm_positive, k=12, fill = NA, align = 'right'))),
            colour='tomato2') +
  geom_line(aes(y = normalize(rollmean((vader_positive+lm_positive)/2, k=12, fill = NA, align = 'right'))),
            colour='dodgerblue3') +
  geom_line(aes(y = normalize(cps)))

data %>%
  # filter(date >= '2012-04-01' & date < '2017-12-01') %>%
  ggplot(aes(x = date)) +
  geom_line(aes(y = normalize(rollmean(vader_positive, k=12, fill=NA)))) +
  geom_line(aes(y = normalize(cps)), colour='red')


data %>%
  ggplot(aes(x = ))

summary(lm(cps ~ indice + cpi, data = data.teste))

#  [1] "date"           "gdp_diff"       "cpi"            "interest"       "ppi"            "une"
#  [7] "cps"            "gdp_gap"        "lm_positive"    "lm_negative"    "vader_positive" "vader_negative"
# [13] "words_count"    "recession"      "cpi_diff"       "interest_diff"  "cps_diff"       "une_diff"
# [19] "subprime"       "covid"





plot(data$lm_negative, data$cps)




summary(lm(cps ~ I(vader_negative*lm_negative/2), data))
summary(lm(cps ~ vader_negative , data))
summary(lm(cps ~ lm_negative, data))
summary(lm(cps ~ lm_negative + vader_negative, data))  # not so good

summary(lm(cps ~ I(I(rollmean(lm_negative, k=12, fill=NA, align = 'right'))*
                     I(rollmean(vader_negative, k=12, fill=NA, align = 'right'))/2) + cpi, data))
summary(lm(cps ~ I(rollmean(vader_negative, k=12, fill=NA, align = 'right')), data))
summary(lm(cps ~ I(rollmean(lm_negative, k=12, fill=NA, align = 'right')), data))
summary(lm(cps ~ I(rollmean(lm_negative, k=12, fill=NA, align = 'right')) + I(rollmean(vader_negative, k=12, fill=NA, align = 'right')), data))

data %>%
  ggplot(aes(x = cps, y = lm_negative)) +
  geom_point() +
  geom_smooth(method = 'lm')

data %>%
  # filter(date >= '2012-04-01' & date < '2017-12-01') %>%
  ggplot(aes(x = date)) +
  # geom_line(aes(y = normalize(rollmean(lm_negative, k=12, fill=NA, align = 'right'))), colour = 'tomato4') +
  # geom_line(aes(y = normalize(rollmean(vader_negative, k=12, fill=NA, align = 'right'))), colour = 'tomato2') +
  geom_line(aes(y = normalize(rollmean((lm_negative + vader_negative)/2, k=12, fill=NA, align = 'right')))) +
  geom_line(aes(y = normalize(cps))) +
  scale_x_date(limits = as.Date(c('2013-04-01', '2017-12-01')))


# teste VAR
library(vars)


var_data = data.frame('indice' = (data$vader_negative[2:nrow(data)] +
  data$vader_negative[2:nrow(data)])/2,
                      'cpi' = diff(data$cpi),
                      'gdp' = data$gdp_cycle[2:nrow(data)],
                      'interest' = diff(data$interest),
                      'une' = diff(data$une),
                      'date' = data$date[2:nrow(data)]) %>%
  filter(date > as.Date('2010-01-01')) %>%
  dplyr::select(-date) %>%
  drop_na()  # best model until now




VARselect(var_data, lag.max = 5, type = "const",
          exogen = cbind('recession' = data$recession_x[(1 + nrow(data)-nrow(var_data)):nrow(data)]))


var_model <- VAR(var_data, p=2, type='const',
                 exogen = cbind('recession' = data$recession_x[(1 + nrow(data)-nrow(var_data)):nrow(data)]))
#summary(var_model)


plot(irf(var_model,
           impulse = 'indice',
           response = 'interest',
           n.ahead = 12,
           boot = T,
           ci = 0.90)
)






