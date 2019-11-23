
run() {
    docker run --name mongo-node -v $(pwd)/bulk:/bulk -p 27017:27017 -e AUTH=no -d mongo
}

attach() {
    docker exec -it mongo-node bash
}

ip() {
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongo-node
}

stop() {
    docker stop mongo-node
}

rm() {
    docker rm mongo-node
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