library(DBI)
library(lmerTest)
con = dbConnect(RSQLite::SQLite(), "cambridgedata.db")
dbListTables(con)

results = dbReadTable(con, "results")

dbListFields(con, "results")

#Tried cropping 'extreme' results but data still very skewed and didn't change regression results much

results = results[results[["pb"]] != 0 & results[["runid"]] > 250,] #Ignoring 200-250 runs because pb not as meaningful

attach(results)
y = 5000/time
x = experience/10 #Tried Tanh(experience/...) but didn't make much difference or made it worse
x2 = 5000/pb
model = lmer(y ~ x + x2 + (x + x2|runnerid) + (1|runid))
summary(model)
detach(results)

par(mfrow=c(1,3))
plot(fitted(model), resid(model))
qqnorm(resid(model))
qqline(resid(model))

c = coef(model)
par(mfrow=c(1,1))
plot(1:length(c$runid[["(Intercept)"]]), c$runid[["(Intercept)"]])
lines(1:length(c$runid[["(Intercept)"]]), c$runid[["(Intercept)"]])

for (j in 1:20) {

	resultsample = results[sample(nrow(results), nrow(results), replace=TRUE),]

	attach(resultsample)
	y = 5000/time
	x = experience/10 #Tried Tanh(experience/...) but didn't make much difference or made it worse
	x2 = 5000/pb
	models = lmer(y ~ x + x2 + (x + x2|runnerid) + (1|runid))
	detach(resultsample)

	cs = coef(models)
	
	c$runid[[paste("Boot sample", j)]] = cs$runid[["(Intercept)"]]

}

bootsamples = c$runid[,4:ncol(c$runid)]

ma = array(0, c(nrow(bootsamples), 1))
mi = array(0, c(nrow(bootsamples), 1))
me = array(0, c(nrow(bootsamples), 1))
for (j in 1:nrow(bootsamples)) {ma[j] = max(bootsamples[j,])}
for (j in 1:nrow(bootsamples)) {mi[j] = min(bootsamples[j,])}
for (j in 1:nrow(bootsamples)) {me[j] = sum(bootsamples[j,])/ncol(bootsamples)}

plot(1:length(me), me)
arrows(1:length(me), mi, 1:length(me), ma, length=0.05, angle=90, code=3)
lines(1:length(me), me)

dbDisconnect(con)