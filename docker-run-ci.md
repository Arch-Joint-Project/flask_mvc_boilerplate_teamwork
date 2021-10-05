
 -e is the environment variables to pass from .env file.
 
 *your_preferred_name_of_container* = name for container you would like to create for the docker run.
 
 *the_docker-image-pulled from DockerHub* = name of docker image obtained from docker pull action.
 
**Syntax**<br>
sudo docker run -d -p 8000:5000 --network=host \
  -e DB_NAME=*your_database_name_running_on_local machine* \
  -e DB_PORT=*your_database_port_running_on_local machine* \
  -e DB_USER=*your_database_username* \
  -e DB_PASSWORD=*your_database_password* \
  -e DB_HOST=127.0.0.1 \
  --name *your_preferred_name_of_container* *the_docker-image-pulled from DockerHub*
 
 Example:<br>
 > sudo docker run -d -p 8000:5000 --network=host -e DB_NAME=postgres -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=rootpassword -e DB_HOST=127.0.0.1 -e FLASK_ENV=development --name thiscontainer thebluedocker/flask_mvc_boilerplate_teamwork

 
 **To verify running status of container**<br>
 sudo docker logs *your_preferred_name_of_container*
 
 sudo docker ps
 
 sudo docker images
 
 sudo docker stop 
