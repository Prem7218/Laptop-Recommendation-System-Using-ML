import streamlit as st
import requests
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import random


def recommend(price, laptops):
    choice = False
    view_option = st.selectbox("Select View Option:", ["Please Select", "View All in Below Range", "View All in Above Range"])
    if view_option == "View All in Above Range":
        affordable_laptops = laptops[laptops['Price'] >= price].head(
            5)  # Assuming 'Price' is correctly set up and laptops is a DataFrame
        choice = True
    else:
        affordable_laptops = laptops[laptops['Price'] <= price].head(
            5)
        choice = True

    if choice:
        if affordable_laptops.empty:
            st.write("No laptops found within this price range.")
            return

        fig, ax = plt.subplots()
        brands = affordable_laptops['Brand'].values
        prices = affordable_laptops['Price'].values

        ax.scatter(brands, prices)
        ax.set_xlabel('Brand')
        ax.set_ylabel('Price')
        ax.set_title('Top 5 Affordable Laptops')

        # Display the laptops in a table and the plot
        st.write(affordable_laptops)
        st.pyplot(fig)
    else:
        print("\n\t[ * ] Select Choice From Above...")


def search_google_image(query):
    api_key = 'AIzaSyBWmiK6lpcdkP-YYI9UMtzJojvoFSHpaO0'
    cse_id = 'e465b812daba544b5'
    search_type = 'image'
    # Append "laptop" to the query to narrow down the search to laptop images
    refined_query = f"{query} laptop"
    num_results = 10  # Adjust based on how many results you want to fetch
    url = f'https://www.googleapis.com/customsearch/v1?q={refined_query}&key={api_key}&cx={cse_id}&searchType={search_type}&num={num_results}'

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        items = results.get('items', [])
        if len(items) < 5:
            print("Not enough images available for this query.")
            return []

            # Randomly select 5 unique images from the items
        selected_items = random.sample(items, 5)
        selected_images = [item['link'] for item in selected_items]

        return selected_images

    # # except requests.RequestException as e:
    # print(f"Request failed: {}")
    # return ['https://via.placeholder.com/400'] * 5  # Return placeholder images in case of failure


# def search_google_image(query):
#     api_key = 'AIzaSyCrOIklqgXwxh_3Y6zgQlj5RYlKqS_W6ag'
#     cse_id = 'e465b812daba544b5'
#     search_type = 'image'
#     url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&searchType={search_type}&num=1'
#
#     response = requests.get(url)
#     if response.status_code == 200:
#         results = response.json()
#         if results.get('items'):
#             return results['items'][0]['link']
#     return 'https://via.placeholder.com/400'  # Fallback image URL


# def search_google_image(query):
#     api_key = 'AIzaSyCrOIklqgXwxh_3Y6zgQlj5RYlKqS_W6ag'
#     cse_id = 'e465b812daba544b5'
#     search_type = 'image'
#     num_results = 10  # Fetch 10 results; adjust as needed based on your use case
#
#     url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&searchType={search_type}&num={num_results}'
#
#     response = requests.get(url)
#     if response.status_code == 200:
#         results = response.json()
#         items = results.get('items', [])
#         if items and len(items) >= 2:
#             # Select the second-to-last image from the results
#             return items[-2]['link']
#     return 'https://via.placeholder.com/400'  # Fallback image URL

# def search_unsplash_image(query):
#     access_key = 'PwnK-fI0NVOhSGvglFvVaAbu9VVglVMDYaG33PNalCw'
#     url = 'https://api.unsplash.com/search/photos'
#     headers = {'Authorization': f'Client-ID {access_key}'}
#     params = {'query': query, 'per_page': 1}
#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         results = response.json()['results']
#         if results:
#             return results[0]['urls']['regular']
#     return 'https://via.placeholder.com/400'  # Fallback image URL


st.header('Laptop Recommendation By User Price')
laptops_new = pickle.load(open('laptops.pkl', 'rb'))
laptops = pd.DataFrame(laptops_new)

price = st.slider('Select Laptop Price Here:- ', 0, 500000)
if price >= 9800:
    recommended_laptops = recommend(price, laptops)
    if recommended_laptops is not None:
        st.write(recommended_laptops[['Brand', 'Model', 'Price']])
else:
    st.text('Selected Price Is Very Low...')

# Assuming search_google_image is defined elsewhere in your script.

search_term = st.text_input("Enter Laptop Name:- ")
view_option = st.selectbox("Select View Option:", ["Please Select", "View All in One Row", "View One by One"])

if st.button('Search for Image'):
    if search_term:
        images = search_google_image(search_term)

        if not images:
            st.warning('No images found. Please try a different search term.')
            # Early exit if no images found

        if view_option == "View All in One Row":
            cols = st.columns(len(images))  # Create a column for each image
            for col, image in zip(cols, images):
                col.image(image, use_column_width=True)  # Display each image in its respective column

        elif view_option == "View One by One":
            for image in images:
                st.image(image, use_column_width=True)  # Display each image in the app

        else:
            st.warning("Please select a view option.")

    else:
        st.warning('Please enter a laptop name to search for its image.')
