import os
import supabase
from supabase import create_client, Client

global supabaseClient
from dotenv import load_dotenv

supabaseClient = None


# Loads the .env file from the root of the project.
# Add a .env file with SUPABASEKEY and SUPABASEURL variables
# if you haven't already.
load_dotenv()


# Here we fetch the environment variables from our .env file.
supabaseKey = os.getenv('SUPABASEKEY')
supabaseURL = os.getenv('SUPABASEURL')

# Here we establish our supabase client that we can use to
# communicate with the database.
# NOTICE: This will be have to be done in the frontend.
def initialize():
    global supabaseClient
    global supabaseKey
    global supabaseURL

    # Creates a supabase client from the supabase package.
    supabaseClient = create_client(supabaseURL, supabaseKey)
    print("Connection established!")
    return supabaseClient

def get_client_for_token(token: str):
    """Skapar en ny Supabase-klient med en aktiv session för den tokenen"""
    client = create_client(supabaseURL, supabaseKey)
    client.auth.set_session(token, "")
    return client

# Deletes a users plants if they are logged in.
def deleteUserPlant(plant_id, user_id, token):
    # Here we use the supabase client to delete a users plant
    # from the user_plants table.
    client = get_client_for_token(token)
    try:
        response = (client.table('user_plants')
                    .delete()
                    .eq("user_id", user_id)
                    .eq("plant_id", plant_id)
                    .execute())

        return response.data

    # If there is an error from the client, we return it.
    except client.Error as e:
        return e.code


# Fetches all plants in user_plants that match the users id.
def getUserPlants(user_id, token):
    client = get_client_for_token(token) 

    try:
        response = (client.table('user_plants')
                    .select("*")
                    .eq("user_id", user_id)
                    .execute())

        return response.data

    # If there is an error from the client, we return it.
    except client.Error as e:
        return e.code

# Registers a new user
def registerUser(email, password):
    # Here we use the supabase client to easily
    # register a new user.
    # The client will return an error in case such a user already exists.
    try:
        response = supabaseClient.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )
        return "success"

    # If there is an error with the authentication, we return it.
    except supabase.AuthApiError as e:
        return e.code

# Logs in a user if their email:password combo is correct.
def loginUser(email, password):
    # We use the supabaseClient to sign in the user.
    # This will return a JWT token from supabase,
    # which can be used to do execute functions
    # specifically on the signed-in users account.
    try:
        response = supabaseClient.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
        return response.session

    # If there is an error with the authentication, we return it.
    except supabase.AuthApiError as e:
        return None

#def getCurrentUser():
 #   return supabaseClient.auth.get_user()

def signOutUser():
    try:
        supabaseClient.auth.sign_out()
        return "success"
    except supabase.AuthApiError as e:
        return e.code

def changePassword(access_token, new_password):
    client = get_client_for_token(access_token)
    try:
        client.auth.update_user({"password": new_password})
        return "success"
    except supabase.AuthApiError as e:
        return e.code
