
# Packages
library(tidyverse)
library(patchwork)

# Add correlation plot ----
data <- read_csv('data\\data_variables.csv')

data %>%
  ggplot(aes(cpi, cps)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, colour = 'gray50') +
  labs(x=)
  theme_minimal()