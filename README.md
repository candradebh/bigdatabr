# Trabalho pratico IGTI


## Criando banco de dados
/server/database/$ py create_schema.py

## Want to use this project?

1. Fork/Clone

1. Executando o servidor :

    ```sh
    $ cd server
    $ virtualenv venv
    $ py -m venv env
    $ venv\Scripts\activate
    (env)$ pip install -r requirements.txt
    (env)$ py app.py
    ```

    Acessar pela URL [http://localhost:5000](http://localhost:5000)

1. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run serve
    ```

    Acessar pela URL [http://localhost:8080](http://localhost:8080)




## Spark 

1. twitter_app.py
spark-submit --executor-cores 31 --executor-memory 10G --driver-memory 2G spark_app.py