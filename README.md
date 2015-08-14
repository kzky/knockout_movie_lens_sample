# knockout_movie_lens_sample
knockout x flask x movie_lens data sample, to show c2c and u2c.

## Directory Schema and Files
- batch
  - create_recommendation\_result.py: creates db and collections
  - dataset
  - ratings_3cols.dat: movie_lens dataset containing 3 cols; user, movie, rating
- knockout\_movie\_lens
    - app
      -  \_\_init\_\_.py: init for app
      - controllers.py
      - models.py
      - services.py
      - static
      - templates
  - config.py
  - run.py

## How to run an app
1. Install Necessary Components
   - middleware
     - monogodb sever and client
   - python libs
     - scipy==0.13.3
     - pymongo==3.0.3
     - Flask==0.10.1

    You can install python libs with requements.txt

    ```sh
    python install -r requements.txt
    ```

1. Create Database

    1. Get MoveiLens Dataset
      - Download movielens dataset [here](http://grouplens.org/datasets/movielens )
      - Any dataset are acceptable if it includes ratings.data
      - [ml-latest.zip](http://files.grouplens.org/datasets/movielens/ml-latest.zip) inclues ratings.dat.
      - Get ratings.data inside the zip file.

    1. Run Batch Job
   
       To run the batch script create_recommendation\_result.py, you first retrieve first 3 columns from the ratings.dat.

       ```sh
       $ gawk -F "::" '{print $1","$2","$3}' ratings.dat > ratings_3cols.dat
       ```
     
       Run the batch script, which took a few 10 mins with 10,000,054 records.
       
       ```sh
       $ python create_recommendation_result.py ${pathto}/ratings_3cols.dat
        ```

1. Run Flask App

    You can find configuration file (config.py) where hosts and ports are set as default in flask app and mongodb and change at your disposal.

    Go to the directory where run.py is located and execute run.py
    ```sh
    $ python run.py
    ```

    Access to http://localhost:8080/web/movie_lens/top.html through your browser.
