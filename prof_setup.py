import re
import requests

class Data_Extractor():
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

    '''
    Got this part from stackoverflow to find the request page for loading all the profs
    http://stackoverflow.com/questions/39065492/dryscrape-click-load-more-button
    '''

    def __init__(self):
        return

    def setup(self):
        #reinitilize
        self.prof_info_list = []
        self.name_added = set()
        self.get_st_george()
        self.get_missi()
        self.get_scra()

    def get_school(self):
        with requests.session() as s:
            s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
            res = s.get(self.URL, params=self.params)
        content = res.content.decode("utf-8")
        content = self.get_within(content)
        prof_data_list = content.split("{")
        for prof in prof_data_list:
            self.extract_info(prof)

    '''
    Get professors in the three campuses
    '''
    def get_st_george(self):
        self.params["q"] = self.ST_GEORGE_PARAM
        self.get_school()

    def get_missi(self):
        self.params["q"] = self.MISSI_PARAM
        self.get_school()

    def get_scra(self):
        self.params["q"] = self.SCRA_PARAM
        self.get_school()

    #helper function to parse the document we get
    def get_within(self, content):
        index1 = content.find("[")
        index2 = content.find("]")
        return content[index1 + 1 : index2]

    #read the document and store all the relevant info in a list
    def extract_info(self, prof_data):
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
        '''
        if name not in self.name_added:
            self.name_added.add(name)
        else:
            print(name)
        '''
        self.prof_info_list.append([prof_id, prof_first, prof_last, avg_rating])

    #search for the professors in our list
    def search_prof(self, name):
        for data in self.prof_info_list:
            if self.match_name(data[1], data[2], name):
                comment = "Average rating for {} {} is: {}\n\n[link to his/her rating]({})"\
                    .format(data[1], data[2], data[3], self.RMP_BASE + data[0])

                return comment
        return "{} Cannot be Found\n\n".format(name)

    '''
     let's say we want to match Bill Gates
     then we can either input (case insensetive)
     1. bill gates
     2. b. gates
     3. b.gates
     4. gates bill
     '''
    def match_name(self, first_name, last_name, input_name):
        #apprantly there are empty spaces added inside of the data list
        if first_name == "":
            return False

        return ((first_name.lower() + " " + last_name.lower()) == input_name.lower()) or \
               ((first_name[0].lower() + " " + last_name.lower()) == input_name.lower()) or \
               ((first_name[0]).lower() + ". " + last_name.lower() == input_name.lower()) or \
                ((last_name.lower() + " " + first_name.lower()) == input_name.lower())
