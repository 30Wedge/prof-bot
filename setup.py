import re
import requests

#URL = 'http://www.facebook.com'
params = {"solrformat": "true",
          "rows": "4000",  # set it high number to always get all rows.
          "callback": "noCB",
          "q": "*:*+AND+schoolid_s:1484",
          "defType": "edismax",
          "qf": "teacherfullname_t^1000 autosuggest",
          "bf": "pow(total_number_of_ratings_i,2.1)",
          "sort": "total_number_of_ratings_i desc",
          "siteName": "rmp",
          "rows": "3333",
          "start": "0",
          "fl": "pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s"}

URL = "http://search.mtvnservices.com/typeahead/suggest/"
ST_GEORGE_PARAM = "*:*+AND+schoolid_s:1484"
MISSI_PARAM = "*:*+AND+schoolid_s:4928"
SCRA_PARAM = "*:*+AND+schoolid_s:4919"
RMP_BASE = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='
prof_info_list = []
name_added = set()

'''
Got this part from stackoverflow to find the request page for loading all the profs
http://stackoverflow.com/questions/39065492/dryscrape-click-load-more-button
'''
def main():
    get_st_george()
    get_missi()
    get_scra()
    search_prof("Peter Herman")

def get_school():
    with requests.session() as s:
        s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        res = s.get(URL, params=params)
    content = res.content.decode("utf-8")
    content = get_within(content)
    prof_data_list = content.split("{")
    for prof in prof_data_list:
        extract_info(prof)
def get_st_george():
    params["q"] = ST_GEORGE_PARAM
    get_school()

def get_missi():
    params["q"] = MISSI_PARAM
    get_school()

def get_scra():
    params["q"] = SCRA_PARAM
    get_school()

def get_within(content):
    index1 = content.find("[")
    index2 = content.find("]")
    return content[index1 + 1 : index2]

def extract_info(prof_data):
    prof_id_result = re.search('(?<="pk_id":)([0-9]*)', prof_data)
    if prof_id_result is None:
        return
    prof_id = prof_id_result.group(0)
    prof_first = re.search('(?<="teacherfirstname_t":")([a-zA-Z]*)', prof_data).group(0)
    prof_last = re.search('(?<="teacherlastname_t":")([a-zA-Z]*)', prof_data).group(0)
    avg_rating_result = re.search('(?<="averageratingscore_rf":)(([0-9]*)\.([0-9])*)', prof_data)
    if avg_rating_result == None:
        avg_rating = "0.0"
    else:
        avg_rating = avg_rating_result.group(0)
    if (prof_first is None or prof_last is None):
        return

    name = prof_first + " " + prof_last
    if name not in name_added:
        name_added.add(name)
    else:
        print(name)
    prof_info_list.append([prof_id, prof_first, prof_last, avg_rating])

def search_prof(name):
    for data in prof_info_list:
        if match_name(data[1], data[2], name):
            print("Average rating for " + data[1] + " " + data[2] + ": " + data[3])
            print(RMP_BASE + data[0])


def match_name(first_name, last_name, input_name):
    return ((first_name.lower() + " " + last_name.lower()) == input_name.lower()) or \
           ((last_name.lower() + " " + first_name.lower()) == input_name.lower())


main()