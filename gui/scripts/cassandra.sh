
run() {
    	if [ ! -d $(pwd)/bulk_load ];
	then
        echo "- volume"
		docker run --name cassandra-node -d -p 9042:9042 cassandra
    else
        echo "+ volume"
        docker run --name cassandra-node -v $(pwd)/bulk_load:/bulk_load -d -p 9042:9042 cassandra
	fi
}

attach() {
    docker exec -it cassandra-node bash
}

ip() {
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cassandra-node
}

stop() {
    docker stop cassandra-node
}

rm() {
    docker rm cassandra-node
}

case $1 in
    run|attach|stop|rm|ip)
		;;

	# Every else.
    *)
		echo "Function $1() not defined."
		exit 1 # error
		;;
esac

"$@"