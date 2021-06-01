import praw
import json
from pathlib import Path
import time
import re
from dotenv import load_dotenv

load_dotenv()

def countdownTimer(seconds=970):
    """
    docstring
    """
    

    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        seconds -= 1
    print("Sleep Completed - Trying again...")

    return


def main():
    """
    docstring
    """


    file_path = Path('../free_dawkins/results.json')

    try:
        with open(file_path.resolve()) as f:
            data = json.load(f)
    except Exception as e:
        exit(e)

    reddit = praw.Reddit(
        client_id='***', # Insert dotenv variable, need to implement
        client_secret='***',
        user_agent='***',
        username='***',
        password='***'
    )

    freeDawkins_subreddit = reddit.subreddit("freedawkins")

    counter = 0

    while True:

        try:
            if data[counter]['guessed_youtube_link'][0] != '%':
                url = str(data[counter]['guessed_youtube_link'])
                title = str(data[counter]['title'])
                freeDawkins_subreddit.submit(title=title, url=url)
                print(f"Successfully Posted: {title}")

                counter += 1
                continue

        except praw.exceptions.RedditAPIException as api_exception:
            print(f"Something went wrong!\n{api_exception}")
            # countdownTimer(1)
            api_message = api_exception.message

            if 'minutes' in str(api_message):
                regex_api_message = re.search(r'(.{5}(minutes))', api_message)
                extended_timer_minutes = re.search(r'\d+',regex_api_message[0])
                if extended_timer_minutes is not None:
                    extended_timer_minutes = int(extended_timer_minutes[0])
                    amount_to_extend_seconds = extended_timer_minutes * 60

                    countdownTimer(amount_to_extend_seconds)

                    continue

            if 'second' in str(api_message):
                regex_api_message = re.search(r'(.{5}(seconds))', api_message)
                extended_timer_seconds = re.search(r'\d+',regex_api_message[0])                
                if extended_timer_seconds is not None:
                    amount_to_extend_seconds = int(extended_timer_seconds[0])

                    countdownTimer(amount_to_extend_seconds)

                    continue

        except IndexError:
            print(f"Reached End of Array - Exiting..")
            exit()


            # try:
            #     if data[counter]['guessed_youtube_link'][0] != '%':
            #         url = str(data[counter]['guessed_youtube_link'])
            #         title = str(data[counter]['title'])
            #         freeDawkins_subreddit.submit(title=title, url=url)
            #         print(f"Successfully Posted: {title}")

            #         countdownTimer()
            #     else:
            #         print("JSON Object had incompatible youtube link")
            #         # TODO: Continue onto next link in the json list

            # except praw.exceptions.RedditAPIException as api_exception:
            #         print(f"Something went wrong!\n{api_exception}")
            #         countdownTimer(1)
            #         # TODO: Continue onto next link in the json list
            #         # api_exception.message: 'RATELIMIT: 'you are doing that too much. try again in 38 seconds.' on field 'ratelimit''


if __name__ == "__main__":
    main()