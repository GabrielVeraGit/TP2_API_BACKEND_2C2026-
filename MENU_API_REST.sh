#!/bin/bash
func_menu(){
    echo "Crear Entorno Virtual y Instalar dependencias ---------- 1"
    echo "Crear .env e ingresar las variables para Base de Datos - 2"
    echo "Crear Estructura_General de la DB MySQL ---------------- 3"
    echo "ELIMINAR Estructura de la DB MySQL --------------------- 4"
    echo "Lanzar API-REST Sistema de Reservas de Club Deportivo -- 5"
    echo "Salir -------------------------------------------------- 0"
}

instalar_dependencias(){
    #actualización/instalación interna de pip en el entorno
    ./.venv/bin/python3 -m ensurepip --default-pip
    ./.venv/bin/python3 -m pip install --upgrade pip

    #instalar las dependencias del proyecto
    if [[ -f "requirements.txt" ]]; then
        echo -n "Instalando dependencias desde requirements.txt... "
        ./.venv/bin/python3 -m pip install -r requirements.txt
        sleep 0.5
        echo "Exito!"
    else
        echo "Alerta: No se encontró el archivo requirements.txt"
    fi
}
crear_entorno_virtual(){
    if [ ! -d ".venv" ]; then
        echo -n "Creando entorno virtual .venv... "
        python3 -m venv .venv
        sleep 0.5
        echo "Exito!"
        
        instalar_dependencias

    else
        echo "Ya fue creado"
    fi
}

crear_ingresar_env(){
    igual_enter="si"
    if [[ -f ".env" ]];then
        echo "Ya existe"
    else
        echo "Inicializando las variables .env de la Base de Datos"

        read -p "[default=root] DB_USER=" db_user
        if [[ -z "${db_user}" ]]; then
            db_user="root"
        fi

        while [[ "${igual_enter}" == "si" ]];do
            read -s -p "DB_PASSWORD=" db_password
            echo ""
            if [[ -n "${db_password}" ]]; then
                igual_enter="no"
            fi
        done
        touch .env
        echo "DB_HOST=localhost" >> .env
        echo "DB_USER=${db_user}" >> .env
        echo "DB_NAME=Club_Deportivo" >> .env
        echo "DB_PASSWORD=${db_password}" >> .env
        echo "DB_ESTRUCTURA_CREADA=false" >> .env
        echo "Exito!"

    fi

}

crear_estructura_db(){
    if [[ -f ".env" && $(source .env; echo "$DB_ESTRUCTURA_CREADA") == "false" ]];then
        echo -n "CREANDO la estructura de la base de datos..."

        (
            source .env
            export MYSQL_PWD="${DB_PASSWORD}"
            mysql -h "${DB_HOST}" -u "${DB_USER}" < ./db/init_db.sql
            unset MYSQL_PWD
        )

        sed -i "s/DB_ESTRUCTURA_CREADA=false/DB_ESTRUCTURA_CREADA=true/" .env
        sleep 1
        echo "EXITO!"
    else
        echo "Archivo .venv no existe o la estructura DB ya fue creada"
    fi
}

eliminar_estructura_db(){
    if [[ -f ".env" && $(source .env; echo "$DB_ESTRUCTURA_CREADA") == "true" ]];then
        read -p "¿Desea eliminarla la estructura DB? (si/no): " borrar
        if [[ "${borrar,,}" == "si" ]]; then
            echo -n "ELIMINANDO la estructura de la base de datos..."
            (
                source .env
                export MYSQL_PWD="${DB_PASSWORD}"
                mysql -h "${DB_HOST}" -u "${DB_USER}" -e "DROP DATABASE IF EXISTS ${DB_NAME};"
                unset MYSQL_PWD
            )

            sed -i "s/DB_ESTRUCTURA_CREADA=true/DB_ESTRUCTURA_CREADA=false/" .env
            sleep 1
            echo "EXITO!"
        fi
    else
        echo "Archivo .env no existe o la estructura DB NO EXISTE."
    fi
}

ejecutar_app_py(){

    if [[ -d ".venv" && -f ".env" ]];then

        db_estructura_creada=$(source .env; echo "$DB_ESTRUCTURA_CREADA") #hacer (comandos) ,esto crea una subshell en la q las variables viven brevemente omg
        
        if [[ "$db_estructura_creada" == "true" ]]; then
            ./.venv/bin/python3 ./app.py
        else
            echo "La estructura del DB, no fue creada"
        fi
    else
        echo "ERROR! procure haber hecho las anteriores opciones (1, 2 y 3)"
    fi
}
script_menu_continua="si"
while [[ ${script_menu_continua} == "si" ]];do
    func_menu
    echo ""
    read -p "Ingrese una op -> " opcion
    case "$opcion" in
        "1")
            crear_entorno_virtual
            ;;
        "2")
            crear_ingresar_env
            ;;
        "3")
            crear_estructura_db
            ;;
        "4")
            eliminar_estructura_db
            ;;
        "5")
            ejecutar_app_py
            ;;
        "0")
            script_menu_continua="no"
            ;;
        *)
            echo "OP no valida"
            ;;
    esac
    sleep 0.4
    read -p "   press to continue .."
    clear
done


#source .venv/bin/activate