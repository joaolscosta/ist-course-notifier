import discord
import requests
import feedparser
import asyncio

# Read the bot token
with open("token.txt", "r") as file:
    TOKEN = file.read().strip()

# Bot configuration
COURSE_IDS = [
    '2816360379851131',  # CSF
    '2816360379851174',  # AP
    '2816360379851175',  # SIRS
    '2816360379851135',  # SSof
    '2816360379851118'   # CCU
]
CHECK_INTERVAL = 600  # Interval for checking new announcements in seconds

# Initialize Discord client with default intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Dictionary to track the last announcement for each course
last_announcements = {course_id: None for course_id in COURSE_IDS}

async def check_announcements():
    """Periodically checks for new announcements for all courses and sends them to Discord."""
    while True:
        try:
            for course_id in COURSE_IDS:
                # Fetch course data from the API
                response = requests.get(f'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/courses/{course_id}')
                
                if response.status_code == 200:
                    course_data = response.json()
                    announcement_url = course_data.get('announcementLink')
                    course_name = course_data.get('name', 'Unknown Course')  # Get the course name

                    # Check the RSS feed for announcements
                    if announcement_url:
                        feed = feedparser.parse(announcement_url)
                        if feed.entries:
                            latest_entry = feed.entries[0]
                            latest_title = latest_entry.title
                            latest_link = latest_entry.link

                            # Check if the announcement is new
                            if last_announcements[course_id] != latest_title:
                                last_announcements[course_id] = latest_title
                                
                                # Send the new announcement to the "anuncios" channel
                                channel = discord.utils.get(client.get_all_channels(), name="anuncios")
                                if channel:
                                    await channel.send(f"📢 @here\n**{course_name}**:\n{latest_title}\n{latest_link}\n")
                else:
                    print(f"Error accessing API for course {course_id}: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

        # Wait for the specified interval before checking again
        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    """Event triggered when the bot is ready."""
    print(f'Bot connected as {client.user}')
    # Start the announcement check loop
    client.loop.create_task(check_announcements())

# Run the bot
client.run(TOKEN)
