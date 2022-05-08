# File for figures
#
# Gustavo Vital

# Packages
install.packages(c('tidyverse', 'patchwork'))

library(tidyverse)
library(patchwork)
library(zoo)

# Add correlation plot ----
data <- read_csv('data\\data_M_variables.csv')

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

acum <- function(serie) {

  acum <- c()
  acum[1] <- serie[1]

  for(indice in 2:length(serie)) {
    acum[indice] <- (acum[indice - 1])*(1 + serie[indice]/100)
  }
  acum <- (acum - 1)
  return(acum)
}

plot(data$date, rollmean(data$vader_positive, k = 12), type='l')

data %>%
  ggplot(aes(x = normalize(cps))) +
  geom_line(aes(y = normalize(vader_positive)), size = .3, colour = 'dodgerblue3')
  # geom_line(aes(y = normalize(cps)), size = .3, colour = 'tomato2')

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


plot(normalize())

data.teste <-
  data.frame('indice' = rollmean((data$lm_positive + data$vader_positive)/2,
                                 k = 12, fill = NA, align = 'right'),
             'date' = as.Date(data$date),
             'cps' = data$cps,
             'cpi' = data$cpi, 'gdp' = data$gdp_gap,
             'interest' = data$interest)

data.teste %>%
  filter(date >= '2010-01-01' & date < '2021-01-01') %>%
  ggplot(aes(x = date, y = indice)) +
  geom_line() +
  geom_smooth(method = 'lm')


summary(lm(cps ~ indice + cpi, data = data.teste))

#  [1] "date"           "gdp_diff"       "cpi"            "interest"       "ppi"            "une"
#  [7] "cps"            "gdp_gap"        "lm_positive"    "lm_negative"    "vader_positive" "vader_negative"
# [13] "words_count"    "recession"      "cpi_diff"       "interest_diff"  "cps_diff"       "une_diff"
# [19] "subprime"       "covid"