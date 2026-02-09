#!/bin/bash

RED='\033[1;31m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'


print_color() {
    local color="$1"
    local message="$2"

    case "$color" in
        red)
            echo -e "${RED}${message}${RESET}"
            ;;
        blue)
            echo -e "${BLUE}${message}${RESET}"
            ;;
        green)
            echo -e "${GREEN}${message}${RESET}"
            ;;
        yellow)
            echo -e "${YELLOW}${message}${RESET}"
            ;;
        *)
            echo "${message}"
            ;;
    esac
}