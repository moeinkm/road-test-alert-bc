DATE_LABEL = 'date'
DAY_OF_WEEK_LABEL = 'day_of_week'
START_AT_LABEL = 'start_at'

TEST_LOCATIONS_TO_SCRAPE = [
    {'city': 'Vancouver', "lng":-123.13377, "lat":49.283037},
    {'city': 'Abbotsford', "lng":-122.30377, "lat":49.063037},
    {'city': 'Hope', "lng":-121.44377, "lat":49.383037},
    {'city': 'Kelowna', "lng":-119.46377, "lat":49.873037},
    {'city': 'Kamloops', "lng":-120.33377, "lat":50.673037},
    {'city': 'Victoria', "lng":-123.36377, "lat":48.423037},
    {'city': 'Nanaimo', "lng":-123.93377, "lat":49.163037},
    {'city': 'Prince George', "lng":-122.75377, "lat":53.913037},
    {'city': 'Prince Rupert', "lng":-125.73377, "lat":54.313037},
    {'city': 'Bella Coola', "lng":-126.75377, "lat":52.383037},
    {'city': 'Terrace', "lng":-128.60377, "lat":54.513037},
    {'city': 'Dawson Creek', "lng":-120.24377, "lat":55.763037},
    {'city': 'Fort St. John', "lng":-120.85377, "lat":56.253037},
    {'city': 'Smithers', "lng":-127.16377, "lat":54.783037},
    {'city': 'Cranbrook', "lng":-115.76377, "lat":49.613037},
    {'city': 'Nelson', "lng":-117.28377, "lat":49.493037},
    {'city': 'Port Hardy', "lng":-127.41377, "lat":50.693037},
    {'city': 'Masset', "lng":-132.15377, "lat":54.013037},
    {'city': 'Quesnel', "lng":-122.48370, "lat":52.978416},
    {'city': 'Valemount', "lng":-119.12384, "lat":52.831073},
    {'city': 'Stewart', "lng":-130.00279, "lat":55.936954},
    {'city': 'Atlin', "lng":-133.70021, "lat":59.574044},
    {'city': 'Telegraph Creek', "lng":-131.13642, "lat":57.904683},
    {'city': 'Iskut', "lng":-130.63534, "lat":56.666406},
    {'city': 'Cassiar', "lng":-129.82297, "lat":59.281324},
    {'city': 'Coal River', "lng":-126.96600, "lat":59.805705},
    {'city': 'Fort Nelson', "lng":-122.70155, "lat":58.805519},
    {'city': 'Fort Ware', "lng":-125.64892, "lat":57.318403},
]
TEST_CENTERS_HEADERS = {
  "sec-ch-ua-platform": "Windows",
  "Referer": "https://onlinebusiness.icbc.com/webdeas-ui/booking",
  "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
  "Accept": "application/json, text/plain, */*",
  "Content-Type": "application/json"
}
LOGIN_HEADERS = {
    "sec-ch-ua-platform": "\"Windows\"",
    "Cache-control": "no-cache, no-store",
    "Referer": "https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "Expires": "0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
  }