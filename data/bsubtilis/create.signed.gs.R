#create a signed matrix keeping exactly
#the same order in original gs

setwd("inferelator_ng/data//bsubtilis/")
temp.gs<-read.table("gold_standard.tsv")
load("bsubtilis.signed.prior.mat.RData")
new.mat<-matrix(nrow=dim(temp.gs)[1],ncol=dim(temp.gs)[2],0)
rownames(new.mat)<-rownames(temp.gs)
colnames(new.mat)<-colnames(temp.gs)

for(m in 1:dim(new.mat)[2])
{
 col<-as.character(colnames(new.mat)[m])
 pos.col<-which(colnames(gs.signed)==col)
 targets<-rownames(gs.signed)[which(gs.signed[,pos.col]!=0)]
 signs<-as.numeric(gs.signed[which(gs.signed[,pos.col]!=0),pos.col])
 if(length(targets)>0)
 {
 	for(t in 1:length(targets))
 	{
 		current.target<-as.character(targets[t])
 		target.pos<-which(rownames(new.mat)==current.target)
 		new.mat[target.pos,m]<-signs[t]
 	}
 }

}
