import json
from typing import List
from pydantic import BaseModel

class Advertisement(BaseModel):
    screen_id: int
    adveritsement_id: str

class AllAds(BaseModel):
    ads: List[Advertisement] = []

class RenderAd:

    def __init__(self):
        self.reset()
        f = open('lp_add_linkage.json')
        self.lp_ad_map = json.load(f)

    def reset(self):
        self.ads = AllAds(ads=[])

    def set_ad_to_screen(self, lp: str):
        self.reset()
        # print('incoming lp is :', lp)
        for each_lp_ad_map in self.lp_ad_map:
            if each_lp_ad_map['lp'] == lp:
                ad_obj = Advertisement(screen_id=each_lp_ad_map['display'], adveritsement_id=each_lp_ad_map['ad'])
                self.ads.ads.append(ad_obj)

    def get_ad_id(self, screen_id: int):
        ad_id = {'id':'ad1'}
        for each_ad in self.ads.ads:
            if screen_id == each_ad.screen_id:
                ad_id['id'] = each_ad.adveritsement_id
                break
        print('Given Id is :', ad_id)
        return ad_id


        
