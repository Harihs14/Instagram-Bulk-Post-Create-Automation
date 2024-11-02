import os
import random
import spacy
import asyncio
from playwright.async_api import async_playwright

# Load Spacy model for NLP
nlp = spacy.load('en_core_web_sm')

# Love-related emojis
love_emojis = ["❤️", "😍", "😘", "💖", "💞", "💕", "💘", "💓", "💗", "💜"]

# Love-related hashtags
love_hashtags = ["#Love", "#Romance", "#LoveQuotes", "#RelationshipGoals", "#CoupleGoals", "#InLove", "#LoveLife", "#LoveStory", "#Heart", "#TrueLove"]

# Function to generate a random caption with love-related emojis and hashtags
def generate_caption(quote):
    doc = nlp(quote)
    keywords = [token.text for token in doc if token.pos_ in ("NOUN", "ADJ")]

    if keywords:
        keywords_sample = random.sample(keywords, min(len(keywords), 3))
        caption = f"{random.choice(love_emojis)} {' '.join(keywords_sample)} {random.choice(love_emojis)}"
    else:
        caption = f"{random.choice(love_emojis)} {quote[:50]} {random.choice(love_emojis)}"

    hashtags = " ".join(random.sample(love_hashtags, min(len(love_hashtags), 3)))
    return f"\"{quote}\" - {caption}\n\n{hashtags}"

# Path to the posts folder
posts_folder = "posts"

# Get the list of post files
post_files = [os.path.join(posts_folder, f) for f in os.listdir(posts_folder) if f.endswith('.png')]

# Instagram credentials
username = "amourbits"
password = "Hari@1234"

async def login_instagram(page):
    await page.goto("https://www.instagram.com/accounts/login/")
    await page.fill("input[name='username']", username)
    await page.fill("input[name='password']", password)
    await page.click("button[type='submit']")

    try:
        # Wait for the home page to load indicating successful login
        await page.wait_for_selector("xpath=//span[contains(text(), 'Home')]", timeout=10000)
        print("Login successful.")
        await page.click("button[type='button']")
        await page.click("button._a9--._ap36._a9_1")
        return True
    except Exception as e:
        print(f"Login error: {e}")
        return False

async def upload_post(page, image_path, caption):
    try:
        print("Navigating to new post creation page...")
        await page.goto("https://www.instagram.com/")

        # Click on the 'New Post' button
        await page.click("[aria-label='New post']")

        # Wait for the 'Post' button to be visible and click it
        await page.wait_for_selector("[aria-label='Post']")
        await page.click("[aria-label='Post']")
        
        await page.wait_for_selector("text=Select from computer")
        
        # Upload the image file
        file_input = await page.query_selector("input[type='file']")
        await file_input.set_input_files(image_path)

        print("Waiting for file upload...")
        await page.click("text=Next")

        await page.click("text=Next")

        await page.click("text=Share") 
        
        print("Post shared successfully.")
    except Exception as e:
        print(f"Error in uploading post: {e}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        # Log in to Instagram
        page = await browser.new_page()
        if not await login_instagram(page):
            await browser.close()
            return

        # Load quotes from file
        with open("quotes.txt", "r") as file:
            quotes = file.readlines()

        # Upload posts
        for i, post_file in enumerate(post_files):
            quote = quotes[i].strip()
            caption = generate_caption(quote)
            try:
                await upload_post(page, os.path.abspath(post_file), caption)

                # Navigate back to home page
                await page.goto("https://www.instagram.com/")
                await page.wait_for_selector("xpath=//span[contains(text(), 'Home')]", timeout=10000)
            except Exception as e:
                print(f"Error uploading post: {e}")

        await browser.close()

# Run the main function
asyncio.run(main())
