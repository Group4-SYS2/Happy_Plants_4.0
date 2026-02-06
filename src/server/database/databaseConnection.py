import os
import supabase
from supabase import create_client, Client

global supabaseClient
from dotenv import load_dotenv

load_dotenv() # Loads the .env file

supabaseKey = os.getenv('SUPABASEKEY')
print(supabaseKey)
supabaseURL = os.getenv('SUPABASEURL')
print(supabaseURL)


def deleteUserPlant(plant_id, user_id):
    try:
        response = (supabaseClient.table('user_plants')
                    .delete()
                    .eq("user_id", user_id)
                    .eq("plant_id", plant_id)
                    .execute())

        return response.data

    except supabaseClient.Error as e:
        return e.code


def getUserPlants(user_id):
    try:
        response = (supabaseClient.table('user_plants')
                    .select("*")
                    .eq("user_id", user_id)
                    .execute())

        return response.data

    except supabaseClient.Error as e:
        return e.code


def getAllUsers():
    try:
        response = (supabaseClient.table("users")
                    .select("*")
                    .execute())

        return response.data

    except supabaseClient.AuthApiError as e:
        return e.code

def registerUser(email, password):
    try:
        response = supabaseClient.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )
        return "success"

    except supabase.AuthApiError as e:
        return e.code

def loginUser(email, password):
    try:
        response = supabaseClient.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
        return "success"

    except supabase.AuthApiError as e:
        return e.code

def getCurrentUser():
    return supabaseClient.auth.get_user()

def signOutUser():
    try:
        supabaseClient.auth.sign_out()
        return "success"
    except supabase.AuthApiError as e:
        return e.code

def changePassword(new_password):
    try:
        supabaseClient.auth.update_user({"password" : new_password})
        return "success"
    except supabase.AuthApiError as e:
        return e.code

def initialize():
    global supabaseClient
    global supabaseKey
    global supabaseURL

    supabaseClient = create_client(supabaseURL, supabaseKey)
    print("Connection established!")
    return supabaseClient