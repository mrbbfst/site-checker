#!/bin/bash

# Function to read user input with a prompt
read_input() {
    read -r -p "$1" input
    echo "$input"
}

read_input_s() {
    read -r -s -p "$1" input
    echo "$input"
}

echo "  _____                                         "
echo " |___ /_      _____ ___  _ __ ___   _   _  __ _ "
echo "   |_ \ \ /\ / / __/ _ \| '_ \` _ \ | | | |/ _\` |"
echo "  ___) \ V  V / (_| (_) | | | | | || |_| | (_| |"
echo " |____/ \_/\_(_)___\___/|_| |_| |_(_)__,_|\__,_|"
echo ''                                                


echo "Welcome to the setup script for the site-checker project."
echo "This script will set up the project by creating a .env file and building docker images."
echo "To run the project, make sure you have the following dependencies installed: docker, docker compose and crontab."
if [ "$(read_input "Do you want to continue? (y/n)")" != "y" ]; then
    echo "Exiting..."
    exit 1
fi
# Get the current working directory
CURRENT_WORK_DIR=$(pwd)

# Replace placeholder in check.sh with the current working directory
echo "#!/bin/bash
cd $CURRENT_WORK_DIR

docker compose up checker" > check.sh
# sed -i "s|{REPLACE_ME_TO_CURRENT_WORK_DIR}|$CURRENT_WORK_DIR|g" check.sh

# Create a new .env file
echo "# .env file" > .env

# Array of variables from .env.sample
variables=()
while IFS= read -r line; do
    # Check if the line is not empty and does not start with a comment character (#)
    if [ -n "$line" ] && [ "${line:0:1}" != "#" ]; then
        variable=$(echo "$line" | cut -d'=' -f1)
        variables+=("$variable")
    fi
done < .env.sample

# Prompt user for input for each variable in .env.sample
for variable in "${variables[@]}"; do
    # value=$(read_input "Enter value for $variable: ")
if [[ "$variable" =~ [Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd] ]]; then
        value=$(read_input_s "Enter value for $variable: ")
        echo ''
    else
        value=$(read_input "Enter value for $variable: ")
    fi
    # Append the variable and its value to .env
    echo "$variable=$value" >> .env
done

if read_input "Build docker images? (y/n) " == "y"; then
    if command -v docker &> /dev/null && command -v compose &> /dev/null; then
    # Build docker images
        docker compose build
        if [ $? -eq 0 ]; then
        echo "Build successful"
        if read_input "Do you want to run services? (y/n)" == "y"; then
            # Run services
            docker compose up -d
            if command -v crontab &> /dev/null; then
                # Add the execution of check.sh to crontab
                (crontab -l ; echo "* * * * * cd $CURRENT_WORK_DIR && ./check.sh") | crontab -
                echo "Now run the following command for setup database:"
                echo "docker exec -it <name>-site-<number> python /usr/src/app/manage.py makemigrations && docker exec -it <name>-site-<number> python /usr/src/app/manage.py migrate"
                echo "and create django superuser with the following command:"
                echo "docker exec -it <name>-site-<number> python /usr/src/app/manage.py createsuperuser"
                echo "and then collect staticfiles with the following command:"
                echo "docker exec -it <name>-site-<number> python /usr/src/app/manage.py collectstatic"
            else 
                echo "crontab command not found. Please install it and try again."
            fi
        fi
        else
            echo "Build failed"
        fi
    else
        echo "docker compose command not found. Please install it and try again."
        exit 1
    fi
fi


# Check and set execute permissions for check.sh if needed
[ -x check.sh ] || chmod +x check.sh

echo "Setup completed successfully."
