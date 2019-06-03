#!/usr/bin/env Rscript
options(digits.secs=6)
args=commandArgs(TRUE)
outputprefix=args[1]
pvalue=args[2]

if (!requireNamespace("BiocManager", quietly = TRUE)) {
    install.packages("BiocManager")}
BiocManager::install("org.Hs.eg.db")
library(org.Hs.eg.db)
library(AnnotationDbi)
library(stats4)
library(Homo.sapiens)
library(qqman)

#read data in 
assoc <- read.table(paste(outputprefix,"_association.txt",sep=""),header = TRUE,sep = " ")
assoc=assoc[unique(order(assoc$p)),]
assoc$ensembl_gene=sub('\\..*', '', assoc$gene)
#mapped to other information
mapped_info<-select(org.Hs.eg.db,keys = assoc$ensembl_gene,columns =c("SYMBOL","ENTREZID","CHR"),keytype = "ENSEMBL")
#a=mapped_info[which(duplicated(mapped_info$ENSEMBL)),]
mapped_info2<-select(Homo.sapiens,keys = keys(Homo.sapiens, keytype="TXID"),columns = c("SYMBOL","TXSTART"),keytype = "TXID")

assoc <- assoc %>%
  dplyr::rename(ENSEMBL=ensembl_gene) %>%
  dplyr::left_join(mapped_info,by="ENSEMBL") %>%
  dplyr::distinct(ENSEMBL,.keep_all = TRUE) %>%
  dplyr::left_join(mapped_info2,by="SYMBOL") %>%
  dplyr::filter(!is.na(SYMBOL) & !is.na(TXSTART) & !is.na(p))

assoc_result=assoc %>%
  dplyr::distinct(SYMBOL,.keep_all=TRUE) %>%
  dplyr::select(CHR,ENSEMBL,SYMBOL,beta,z,p,se.beta.)
#write out the result
write.table(assoc_result,file = paste(outputprefix,"_result.csv",sep=""),col.names = TRUE,row.names = FALSE,sep = ",",quote = FALSE)

#plot
assoc$CHR=as.numeric(assoc$CHR)
png(paste(outputprefix,"_plot.png",sep=""),type="cairo",width = 10000,height = 2500,pointsize=80)
manhattan(assoc,chr = "CHR",bp="TXSTART",p="p",snp = "SYMBOL",
          col=c("#FF0000FF","#FF4600FF", "#FF8B00FF" ,"#FFD100FF","#824acd",
                "#2ac075","#3b5998","#b58096","#a958a5","#d1a258",
                "#00FFB9FF", "#f06261" ,"#00B9FFFF" ,"#0074FFFF" ,"#002EFFFF",
                "#1700FFFF" ,"#5D00FFFF" ,"#A200FFFF" ,"#E800FFFF" ,"#FF00D1FF",
                "#FF008BFF", "#FF0046FF"),suggestiveline=FALSE,annotatePval = pvalue)
dev.off()


