import requests

def get_time():
    url = 'http://worldtimeapi.org/api/timezone/Europe/Moscow'
    resp = requests.get(url)
    unixtime = resp.json()["unixtime"]
    return unixtime

def print_time(unixtime):
    try:
        from Time.pretty_print_package.pretty_print_module import print_time_pretty
        print_time_pretty(unixtime)
    except:
        print(unixtime)

def main():
    unixtime = get_time()
    print_time(unixtime)
if __name__ == '__main__':
    main()