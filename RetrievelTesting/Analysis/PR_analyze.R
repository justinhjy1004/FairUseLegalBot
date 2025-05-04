library(tidyverse)

d <- read_csv("PR_Analysis.csv") |>
  mutate(Court = case_when(
    grepl("Supreme Court of the United States", Court, ignore.case = TRUE) ~ "SCOTUS",
    grepl("District", Court, ignore.case = TRUE) ~ "District Court",
    grepl("Appeal", Court, ignore.case = TRUE) ~ "Appeals Court",
    TRUE ~ "Other"
  ))

ggplot(d, aes(x = PageRank, fill = Court)) +
  geom_histogram(position = "identity", alpha = 0.6, bins = 30) +
  scale_x_log10() +  # log-transform x-axis
  labs(title = "Log-Transformed Histogram of CasePR",
       x = "CasePR (log10)", y = "Count") +
  theme_classic() +
  theme(legend.position = "top") +
  annotate("text", x = 4.5, y = 17, label = "Harper & Row \n v.\n Nation Enterprises", hjust = 0.5, vjust = 0.5, size = 3) +
  annotate("segment", x = 4.5, xend = 5.43, y = 10, yend = 2,
           arrow = arrow(length = unit(0.2, "cm")), color = "red") +
  annotate("text", x = .4, y = 44, label = "Andy Warhol Foundation for the Visual Arts, Inc. \n v. \n Goldsmith", hjust = 0.5, vjust = 0.5, size = 3) +
  annotate("segment", x = .4, xend = .23, y = 36, yend = 1,
           arrow = arrow(length = unit(0.2, "cm")), color = "red") +
  annotate("text", x = 2, y = 22, label = "Campbell \n v. \n Acuff-Rose Music, Inc.", hjust = 0.5, vjust = 0.5, size = 3) +
  annotate("segment", x = 2, xend = 2.6, y = 15, yend = 1,
           arrow = arrow(length = unit(0.2, "cm")), color = "red") +
  ggtitle("") +
  xlab("log-adjusted PageRank")

