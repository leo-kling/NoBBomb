#!/bin/bash

source .mise-tasks/utils/colors.sh

ask_yes_no() {
    local usage_question="$1"
    while true; do
        read -r -p "${usage_question?} (y/n): " reponse
        case "$reponse" in
            [Yy])
                print_color "green" "Proceeding.."
                echo ""
                break
                ;;
            [Nn])
                print_color "yellow" "Cancelled by user."
                echo ""
                exit 1
                ;;
            *)
                print_color "red" "Invalid input. Please enter Y or N."
                ;;
        esac
    done
}