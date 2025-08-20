from supabase import create_client
from django.conf import settings
import os

# Create the Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Function to list files in a folder in your Supabase bucket
def list_files_in_folder(bucket_name, folder_name):
    files = supabase.storage.from_(bucket_name).list(path=folder_name)
    return files

# Function to upload a file to a specific folder in your Supabase bucket
def upload_file_to_bucket(file_path, bucket_name, folder_name, file_name):
    with open(file_path, 'rb') as file:
        file_path_in_bucket = f"{folder_name}/{file_name}"
        response = supabase.storage.from_(bucket_name).upload(file_path_in_bucket, file)
        return response

# Function to delete a file from a specific folder in your Supabase bucket
def delete_file_from_bucket(bucket_name, folder_name, file_name):
    file_path_in_bucket = f"{folder_name}/{file_name}"
    response = supabase.storage.from_(bucket_name).remove([file_path_in_bucket])
    return response

# Function to get the public URL of a file
def get_public_url(bucket_name, folder_name, file_name):
    file_path_in_bucket = f"{folder_name}/{file_name}"
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path_in_bucket)
    return public_url 

# Example Usage
if __name__ == "__main__":
    
    buckets = supabase.storage.list_buckets()
    print(buckets)
    # List files in 'videos' folder
    # print("Listing files in 'videos' folder:")
    # files = list_files_in_folder('ezclip-generated-videos', 'videos')
    # print(files)
    
    # # Upload a new file
    # print("\nUploading a video...")
    # upload_response = upload_file_to_bucket('generated-videos', 'videos', 'path_to_your_video/video.mp4', 'new_video.mp4')
    # print(upload_response)

    # # Get public URL of the uploaded video
    print("\nPublic URL for the uploaded video:")
    url = get_public_url('ezclip-generated-videos', 'videos', 'ezclip_video_67.mp4')
    print(url)
    
    # # Delete a file
    # print("\nDeleting the video...")
    # delete_response = delete_file_from_bucket('generated-videos', 'videos', 'new_video.mp4')
    # print(delete_response)
