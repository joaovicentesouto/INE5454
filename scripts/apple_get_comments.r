library(itunesr)

input   = read.csv("datasets/apple/AppleStore.csv")
dataset = list()

# Sets column names
dataset[["id"]]     <- 0
dataset[["review"]] <- "Dummy"

# Create dataset
count <- 0
total <- length(input$id)
for (id in input$id)
{
    count       <- (count + 1)
    percentagem <- as.integer((count / total) * 100)

    tryCatch({
        reviews_list <- getReviews(id,'us',1)

        for (review in reviews_list$Review[1:3])
        {
            dataset$id     <- c(dataset$id, c(id))
            dataset$review <- c(dataset$review, c(gsub('\n', ' ', review)))
        }

        cat(paste0(percentagem, "% -> downloaded\n"))
    }, error = function(error_condition) {
        dataset$id     <- c(dataset$id, c(id))
        dataset$review <- c(dataset$review, c("NULL"))

        cat(paste0(percentagem, "% -> failed\n"))
    })
}

# Removes dummy entry
dataset$id     <- dataset$id[-1]
dataset$review <- dataset$review[-1]

# Writes csv
write.csv(dataset, file = "datasets/apple/AppleStoreReviews.csv")