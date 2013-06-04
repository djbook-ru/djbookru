
function help() {
    echo -en "\nUsage: `basename $0` [<command> [<command> ...]]\n\n"
    echo -en "where <command> is:\n"
    echo -en "\t* pipi    -- install packages into virtual environment;\n"
    echo -en "\t* pipu    -- update packages of virtual environment;\n"
    echo -en "\t* rsync   -- send source code to a server;\n"
    echo -en "\t* po      -- compile PO resources;\n"
    echo -en "\t* migrate -- run migrations on the database;\n"
    echo -en "\t* static  -- collect static files;\n"
    echo -en "\t* i18n    -- update multilanguage fields;\n"
    echo -en "\t* index   -- rebuild search index;\n"
    echo -en "\t* touch   -- restart web server.\n"
    echo -en "\n"
}

if [ "$#" == "0" ] || [ "$1" == "help" ] || [ "$1" == "-h" ]; then
    help; exit 0
fi
TARGET=$1
FAB="fab production deploy_server"
DELIM=":"

for param in $@; do
    case ${param} in
        pipi)
            FAB="${FAB}${DELIM}pip=i"; DELIM=",";;
        pipu)
            FAB="${FAB}${DELIM}pip=u"; DELIM=",";;
        po)
            FAB="${FAB}${DELIM}po=y"; DELIM=",";;
        rsync)
            FAB="${FAB}${DELIM}rsync=y"; DELIM=",";;
        migrate)
            FAB="${FAB}${DELIM}migrate=y"; DELIM=",";;
        static)
            FAB="${FAB}${DELIM}static=y"; DELIM=",";;
        i18n)
            FAB="${FAB}${DELIM}i18n=y"; DELIM=",";;
        index)
            FAB="${FAB}${DELIM}haystack=y"; DELIM=",";;
        touch)
            FAB="${FAB}${DELIM}touch=y"; DELIM=",";;
        *)
            help; exit 1;;
    esac
done

${FAB}
