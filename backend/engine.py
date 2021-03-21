import sys, os, math
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from utils import block_print, enable_print
from sites.youtube import YouTubeChatDownloader
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from json.decoder import JSONDecodeError


@retry(stop=stop_after_attempt(10), retry=retry_if_exception_type(JSONDecodeError))
def get_youtube_messages(link, start_time, end_time):

    parsed = urlparse(link)
    query = parse_qs(parsed.query)
    video_id = query['v'][0]

    params = {
        'url' :  link,
        'start_time' :  start_time,
        'end_time' :  end_time,
        'max_attempts' :  15,
        'retry_timeout' :  None,
        'timeout' :  None,
        'max_messages' :  None,
        'logging' :  'info',
        'pause_on_debug' :  False,
        'inactivity_timeout' :  None,
        'message_groups' :  ['messages'],
        'message_types' :  None,
        'format' :  'youtube',
        'format_file' :  None,
        'chat_type' :  'live',
        'message_receive_timeout' :  0.1,
        'buffer_size' :  4096
    }

    yt = YouTubeChatDownloader()
    chat = yt.get_chat_by_video_id(video_id,params=params)
    youtube_messages = list(chat)
    return youtube_messages

def search(link, search_terms, analysis_interval, start_time, end_time):

    analysis_interval = int(analysis_interval)
    start_time = int(start_time)
    end_time = int(end_time)

    search_terms = search_terms.lower()
    search_terms = search_terms.split(',')
    for index, search_term in enumerate(search_terms):
        search_terms[index] = search_term.lower()

    search_terms = list(set(search_terms))

    print('Search Parameters -> ' + str(search_terms) + '\t' + link + '\t' + str(analysis_interval) + '\t' + str(start_time) + '\t' + str(end_time))

    # block_print()
    # youtube_messages = get_chat_replay(link, start_time = start_time, end_time = end_time)
    
    youtube_messages = get_youtube_messages(link, start_time = start_time, end_time = end_time)
    # print(youtube_messages)
    # enable_print()

    for index, message in enumerate(youtube_messages):
        youtube_messages[index]['message'] = message['message'].lower()

    duration = youtube_messages[-1]['time_in_seconds']

    buckets = []
    bucket_num = math.ceil(duration/(analysis_interval)) - 1

    next_lower_bound = 0
    next_upper_bound = analysis_interval

    buckets.append({
        'lower_bound': next_lower_bound,
        'lower_timestamp': str(timedelta(seconds=next_lower_bound)),
        'upper_bound': next_upper_bound,
        'upper_timestamp': str(timedelta(seconds=next_upper_bound)),
        'count': 0,
        'matched_messages': [],
        'all_messages': []
    })

    for i in range(bucket_num):
        # next_lower_bound = next_lower_bound + analysis_interval + 1
        next_lower_bound = next_lower_bound + analysis_interval
        next_upper_bound = next_lower_bound + analysis_interval
        buckets.append({
            'lower_bound': next_lower_bound,
            'lower_timestamp': str(timedelta(seconds=next_lower_bound)),
            'upper_bound': next_upper_bound,
            'upper_timestamp': str(timedelta(seconds=next_upper_bound)),
            'count': 0,
            'matched_messages': [],
            'all_messages': []
        })

    for search_term in search_terms:
        for bucket in buckets:
            lower_bound = bucket['lower_bound']
            upper_bound = bucket['upper_bound']
            # print(lower_bound)
            # print(upper_bound)
            for message in youtube_messages:
                time_in_seconds = message['time_in_seconds']
                within_bucket_range = lower_bound <= time_in_seconds <= upper_bound
                if within_bucket_range:
                    bucket['all_messages'].append(message)
                    if search_term in message['message']:
                        # print(message)
                        bucket['count'] = bucket['count'] + 1
                        bucket['matched_messages'].append(message)
                # else:
                #     print(str(lower_bound) + '\t' + str(time_in_seconds) + '\t' + str(upper_bound))

    # print(buckets)
    return buckets


# datetime.now().strftime("%H:%M:%S")