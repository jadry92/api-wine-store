
#!/bin/bash

MODE=$1
FOLDER_NAME="wine_store"

if [ $# -eq 0 ]
then
    echo "No arguments supplied"
    echo "Please provide the mode in which you want to run the server"
    echo "Usage: ./run.sh [dev/prod]"
    exit 1
fi

function start_server() {
    if [ $MODE == "dev" ]
    then
        echo "Starting Server in Dev Mode"
        docker-compose -f local.yml up -d
        return
    elif [ $MODE == "prod" ]
    then
        echo "Starting Server in Production Mode"
        docker compose -f production.yml up -d
        return
    fi
}

function stop_server() {
    if [ $MODE == "dev" ]
    then
        echo "Stopping Server in Dev Mode"
        docker-compose -f local.yml down
        return
    elif [ $MODE == "prod" ]
    then
        echo "Stopping Server in Production Mode"
        docker compose -f production.yml down
        return
    fi
}

function run_test() {
    echo "Running Tests in Dev Mode"
    docker-compose -f local.yml run --rm django pytest
}

function run_migrations() {
    if [ $MODE == "dev" ]
    then
        echo "Running Migrations in Dev Mode"
        docker-compose -f local.yml run --rm django python manage.py makemigrations
        docker-compose -f local.yml run --rm django python manage.py migrate
        return
    elif [ $MODE == "prod" ]
    then
        echo "Running Migrations in Production Mode"
        docker compose -f production.yml run --rm django python manage.py makemigrations
        docker compose -f production.yml run --rm django python manage.py migrate
        return
    fi

}

function delete_volumes(){
    if [ $MODE == "dev" ]
    then
        echo "Deleting Volumes in Dev Mode"
        rm -rv ./${FOLDER_NAME}/media/*
        docker volume rm ${FOLDER_NAME}_local_postgres_data
        return
    elif [ $MODE == "prod" ]
    then
        echo "Deleting Volumes in Production Mode"
        docker volume rm ${FOLDER_NAME}_production_django_media
        docker volume rm ${FOLDER_NAME}_production_postgres_data
        return
    fi
}

function delete_migrations(){
    if [ $MODE == "dev" ]
    then
        echo "Deleting Volumes in Dev Mode"
        rm -rv ./${FOLDER_NAME}/media/*
        docker volume rm "${FOLDER_NAME}_local_postgres_data"
        return
    elif [ $MODE == "prod" ]
    then
        echo "Deleting Volumes in Production Mode"
        docker volume rm main-backend_production_django_media
        docker volume rm main-backend_production_postgres_data
        return
    fi
}

function create_super_user(){
    if [ $MODE == "dev" ]
    then
        echo "Creating Super User in Dev Mode"
        docker-compose -f local.yml run --rm django python manage.py createsuperuser
        return
    elif [ $MODE == "prod" ]
    then
        echo "Creating Super User in Production Mode"
        docker compose -f production.yml run --rm django python manage.py createsuperuser
        return
    fi
}

function change_super_user_password(){
    if [ $MODE == "dev" ]
    then
        echo "Changing Super User Password in Dev Mode"
        docker-compose -f local.yml run --rm django python manage.py changepassword
        return
    elif [ $MODE == "prod" ]
    then
        echo "Changing Super User Password in Production Mode"
        docker compose -f production.yml run --rm django python manage.py changepassword
        return
    fi
}

function backup_database(){
    echo "To be implemented"
}

function restore_database(){
    echo "To be implemented"
}

while true; do
    echo "Welcome to shorcut Server script in Mode ($MODE)"
    echo "1. Start Server"
    echo "2. Stop Server"
    echo "3. Run Tests"
    echo "4. Run Migrations"
    echo "5. Delete Volumes, Media"
    echo "6. Delete Migrations"
    echo "7. Create Super User"
    echo "8. Change Super User Password"
    echo "9. Backup Database"
    echo "10. Restore Database"
    echo "10. Exit"

    read -p "Enter your choice (1/2/3/4/5/6/7/8/9/10): " choice

    case $choice in
        1) start_server ;;
        2) stop_server ;;
        3) run_test ;;
        4) run_migrations ;;
        5) delete_volumes ;;
        6) delete_migrations ;;
        7) create_super_user ;;
        8) change_super_user_password ;;
        9) backup_database ;;
        10) restore_database ;;
        11) echo "Exiting the application. Goodbye!"; exit 0 ;;
        *) echo "Invalid choice. Please try again." ;;
    esac

    echo
done
