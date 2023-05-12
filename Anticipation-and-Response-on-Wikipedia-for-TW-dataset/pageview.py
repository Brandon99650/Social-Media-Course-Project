import os
import requests 
import json
import pandas as pd

class JsonIO():
    def __init__(self) -> None:
        pass

    @staticmethod
    def loadjson(jsonfilepath:os.PathLike):
        """
        Load a json format file 
        by using python native package ```json```
        """
        ret = None
        with open(jsonfilepath, "r") as jf:
            ret =json.load(jf)
        return ret

    @staticmethod
    def writejson(data, jsonfilepath:os.PathLike):
        """
        write standard data type to json format file 
        by using python native package ```json```.

        parameter:
        - encoding: utf-8
        - indent: 4
        - ensure_ascii = False
        """

        with open(jsonfilepath,"w+", encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=4)
    

def getpageviews(
    article_title,start,end,User_agent, 
    project="zh.wikipedia.org", access="all-access",agent="user", granularity="daily"
)->dict:

    """
    Using ```Wiki media REST API``` to get pageviews 
    for an article.

    parameter:
    - User-agent: In my case, I enter my email account 
    and it is avaliale. 
    Note that I don't have wiki account for my mail.

    It seens that they just want to identity user.
    """

    wikimedia_kit = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
    url = f"{wikimedia_kit}/{project}/{access}/{agent}/{article_title}/{granularity}/{start}/{end}"
    print(url)

    headers = {
        "User-Agent":User_agent
    }

    res = requests.get(
        url=url, headers=headers
    )
    if res.status_code != 200:
        print(res.status_code)
        raise ConnectionError
    print("extract json data ..")
    data = json.loads(res.text)
    print(".. OK")

    views ={
        record["timestamp"]:record['views'] 
        for record in data['items']
    }
    return views
    

def main():

    User_agent= "EMAIL_ADDR"
    #JsonIO.loadjson(os.path.join(".","Myprofile.json"))["email"]
    title = "黃珊珊"
    views = getpageviews(
        article_title=title,
        User_agent=User_agent,
        start="20221025",
        end="20221225"
    )
    save_root = os.path.join("data", "actual","91",f"{title}")
    if not os.path.exists(save_root):
        os.mkdir(save_root)
    
    result_save = os.path.join(save_root,f"{title}")
    JsonIO.writejson(data=views, jsonfilepath=f"{result_save}.json")
    views_df = pd.DataFrame(
        {
            "timestamp":list(views.keys()),
            "views":list(views.values())
        }
    )
    views_df.to_csv(f"{result_save}.csv",index=False)




if __name__ == "__main__":
    main()