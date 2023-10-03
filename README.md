# NotInstagram

This app allows users to post their PNG and JPEG files.
User credentials are 'email' and 'password'

1. Pull the repository
2. docker-compose up -d
3. docker exec -it app sh -c "python manage.py create_users"

   This command creates superuser admin@admin.com with password: 123
   It also creates 3 users for testing, all with password: 123
   test1@test.com
   test2@test.com
   test3@test.com

4. Go to http://localhost:8000/ to see the endpoints

  http://localhost:8000/api-token-auth/ is POST for authorizing login and obtaining Token
    
    request sent should have 'email' and 'password'
  http://localhost:8000/images/ is GET for the list of Images that User has uploaded
    
    request needs to have the Token as Authorization: Token <token>  in the Header
  http://localhost:8000/upload/ is POST for Image upload
    
    request needs to have the Token as Authorization: Token <token>  in the Header
    and file: <file> , expiration_time = <value (default 300, max 30000)> (optional)
  http://localhost:8000/media/image_files/<str:filename>/ [name='image_view']
  http://localhost:8000/signed_image_view/<str:signed_value>/ [name='signed_image_view']
    
    Both used for file preview
  http://localhost:8000/admin/ to log in with the superuser credentials and start testing
