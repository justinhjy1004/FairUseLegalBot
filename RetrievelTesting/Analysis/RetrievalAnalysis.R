library(tidyverse)

std_RAG <- read_csv("../Data/StandardRAGRetrieval.csv")
str_RAG <- read_csv("../Data/PRRAGRetrieval.csv")

std_RAG$`Retrieval Method` <- "Standard RAG"
str_RAG$`Retrieval Method` <- "Structured RAG"


df <- rbind(std_RAG, str_RAG) 

df |>
  group_by(`Retrieval Method`) |>
  summarise( m_pagerank = mean(pagerank),
             sd_pagerank = sd(pagerank),
             m_text_sim = mean(text_sim),
             sd_text_sim = sd(text_sim))

t.test(df[df$`Retrieval Method` == "Standard RAG",]$text_sim,
       df[df$`Retrieval Method` == "Structured RAG",]$text_sim)

t.test(df[df$`Retrieval Method` == "Standard RAG",]$pagerank,
       df[df$`Retrieval Method` == "Structured RAG",]$pagerank)

df |>
  gather(key = "Metric", value = "Value", text_sim, pagerank) |>
  mutate(Metric = ifelse(Metric == "pagerank", "PageRank", "Textual Similarity")) -> df_plot

ggplot(data = df_plot, aes(x = Metric, y = Value, color = Metric, fill = Metric)) +
  geom_boxplot(alpha = 0.3) +
  facet_wrap(~`Retrieval Method`, scales = "free_y") +
  coord_flip() +
  theme_classic() +
  theme(legend.position = "none") +
  ylab("min-max adjusted scores") +
  xlab("")


df_cited <- df |>
  group_by(cases, `Retrieval Method`) |>
  summarise(count = n()) |>
  arrange(`Retrieval Method`, desc(count)) |>
  ungroup() |>
  group_by(`Retrieval Method`) |>
  slice_head(n=5) |>
  mutate(custom_hjust = ifelse(`Retrieval Method` == "Standard RAG", 0.75, 1.25),
         custom_hjust = case_when(
           cases == "Hill v. Public Advocate of the United States" ~ 1.55,
           cases == "Ranieri v. Adirondack Dev. Group, LLC" ~ 1.2,
           cases == "Jackson v. Odenat" ~ 1.5,
           cases == "Campbell v. Acuff-Rose Music, Inc." ~ 1.5,
           cases == "BWP Media USA, Inc. v. Gossip Cop Media, Inc." ~ .65,
           .default = custom_hjust
         )) 


ggplot(df_cited, aes(x = reorder(cases, count), y = count, fill = `Retrieval Method`)) +
  geom_bar(stat = "identity", alpha = .6) +
  geom_text(aes(label = cases, hjust = custom_hjust - .2),
            size = 3) +
  facet_wrap(~ `Retrieval Method`, scales = "free") +
  coord_flip() +
  labs(y = "Count", x = "") +
  theme_classic() +
  theme(legend.position = "none", axis.text.y = element_blank(), axis.ticks.y = element_blank()) 
  
