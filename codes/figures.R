
# Packages
library(tidyverse)
library(patchwork)

# Add correlation plot ----
data <- read_csv('data\\data_variables.csv')

cpi_cps <- data %>%
  ggplot(aes(cpi, cps)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
  labs(x = 'Consumer Price Index',
       y = 'Consumer Opinion Surveys: Consumer Prices') +
  theme_minimal()

cpi_vader <- data %>%
  ggplot(aes(cpi, vader_positive)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
  labs(x = 'Consumer Price Index',
       y = 'VADER Positive sentiment') +
  theme_minimal()

cpi_lm <- data %>%
  ggplot(aes(cpi, lm_positive)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
  labs(x = 'Consumer Price Index',
       y = 'Loughran-McDonald Positive Sentiment') +
  theme_minimal()

vader_loughram <- data %>%
  ggplot(aes(vader_positive, lm_positive)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
  labs(x = 'VADER Positive sentiment',
       y = 'Loughran-McDonald Positive Sentiment') +
  theme_minimal()

cps_vader <- data %>%
  ggplot(aes(cps, vader_positive)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
  labs(x = 'Consumer Price Index',
       y = 'VADER Positive sentiment') +
  theme_minimal()

cps_lm <- data %>%
  ggplot(aes(cps, lm_positive)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
  labs(x = 'Consumer Opinion Surveys: Consumer Prices',
       y = 'Loughran-McDonald Positive Sentiment') +
  theme_minimal()

(cpi_lm + cpi_vader + cpi_cps) / (cps_lm + cps_vader + vader_loughram)