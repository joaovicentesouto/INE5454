devtools::install_github("amrrs/itunesr")

library(itunesr)

input   = read.csv("datasets/apple/AppleStore.csv")
dataset = list()

# Sets column names
dataset[["id"]]     <- 0
dataset[["review"]] <- "Dummy"

# Create dataset
for (id in input$id)
{
    cat("Downloading ", id, " reviews")

    reviews <- getReviews(id, 'us', 1)

    for (review in reviews$Review[1:5])
    {
        dataset$id     <- c(dataset$id, c(id))
        dataset$review <- c(dataset$review, c(review))
    }
}

# Removes dummy entry
dataset$id     <- dataset$id[-1]
dataset$review <- dataset$review[-1]

# Writes csv
write.csv(dataset, file = "datasets/apple/AppleStoreReviews.csv")