library(readr)
library(igraph)


ask_ans <- read_delim("C:/Users/Akhil/Desktop/askeranswerer.tsv", 
                      "\t", escape_double = FALSE, trim_ws = TRUE)

link<-data.frame(
  asker=ask_ans[1],
  answerer=ask_ans[2])

net1<-graph_from_data_frame(d=link, directed=T)
plot(net1,vertex.size = 3,vertex.color = 'yellow',edge.width = .2,
     edge.color = 'black',edge.arrow.size=.02, vertex.label = NA)

library(CINNA)
gaint<-giant_component_extract(net1,directed = TRUE)

link_big<-data.frame(
  asker=gaint[2][[1]][,1],
  answer=gaint[2][[1]][,2]
)
net2<-graph_from_data_frame(d=link_big, directed=T)
plot(net2,vertex.size = 4,vertex.color= 'yellow',edge.width = .6,
     edge.color = 'black',edge.arrow.size=.02, vertex.label = NA)

write.table(link_big, file='gaint_component.tsv', quote=FALSE, sep='\t', col.names = NA)
