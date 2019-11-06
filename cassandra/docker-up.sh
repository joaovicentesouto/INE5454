
# Shared folder
mkdir -p mnt

# Init cassandra
sudo docker run           \
	--name cassandra-node \
	-v $(pwd)/mnt:/mnt    \
	-p 7000:7000          \
	-d cassandra