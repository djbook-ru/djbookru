function help() {
    echo -en "\nUsage: `basename $0` <target> [<command> [<command> ...]]\n\n"
    echo -en "where <target> is:\n"
    echo -en "\t* production\n\t* testing\n\n"
    echo -en "where <command> is:\n"
    echo -en "\t* static   -- import static files;\n"
    echo -en "\t* database -- import database content;\n"
    echo -en "\n"
}

if [ "$#" == "0" ] || [ "$1" == "help" ] || [ "$1" == "-h" ]; then
    help; exit 0
fi

TARGET=$1
FAB="fab ${TARGET} importing"
DELIM=":"

for param in $@; do
    case ${param} in
        testing)
            echo "TESTING";;
        production)
            echo "PRODUCTION";;
        static)
            FAB="${FAB}${DELIM}rsync=y"; DELIM=",";;
        database)
            FAB="${FAB}${DELIM}database=y"; DELIM=",";;
        *)
            help; exit 1;;
    esac
done

${FAB}
