# -*- coding: utf-8 -*-
import scrapy

n = 0
class NbaaSpider(scrapy.Spider):
    name = 'nbaa'
    allowed_domains = ['www.basketball-reference.com']
    start_urls = ['https://www.basketball-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=2020&year_max=2020&is_playoffs=N&age_min=0&age_max=99&season_start=1&season_end=-1&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=pts']

    def parse(self, response):
        global n
        log = response.xpath("//tbody/tr")
        for logs in log:
            name = logs.xpath(".//td[@data-stat = 'player']/a/text()").get()
            pos = logs.xpath(".//td[@data-stat = 'pos']/text()").get()
            date = logs.xpath(".//td[@data-stat = 'date_game']/a/text()").get()
            team = logs.xpath(".//td[@data-stat = 'team_id']/a/text()").get()
            opp = logs.xpath(".//td[@data-stat = 'opp_id']/a/text()").get()
            game_result = logs.xpath(".//td[@data-stat = 'game_result']/text()").get()
            MP = logs.xpath(".//td[@data-stat = 'mp']/text()").get()
            FG = logs.xpath(".//td[@data-stat = 'fg']/text()").get()
            FGA = logs.xpath(".//td[@data-stat = 'fga']/text()").get()
            FG_pct = logs.xpath(".//td[@data-stat = 'fg_pct']/text()").get()
            twoP = logs.xpath(".//td[@data-stat = 'fg2']/text()").get()
            twoPA = logs.xpath(".//td[@data-stat = 'fg2a']/text()").get()
            twoP_pct = logs.xpath(".//td[@data-stat = 'fg2_pct']/text()").get()
            threeP = logs.xpath(".//td[@data-stat = 'fg3']/text()").get()
            threePA = logs.xpath(".//td[@data-stat = 'fga']/text()").get()
            threeP_pct = logs.xpath(".//td[@data-stat = 'fg3_pct']/text()").get()
            FT = logs.xpath(".//td[@data-stat = 'ft']/text()").get()
            FTA = logs.xpath(".//td[@data-stat = 'fta']/text()").get()
            FT_pct = logs.xpath(".//td[@data-stat = 'ft_pct']/text()").get()
            ORB = logs.xpath(".//td[@data-stat = 'orb']/text()").get()
            DRB = logs.xpath(".//td[@data-stat = 'drb']/text()").get()
            TRB = logs.xpath(".//td[@data-stat = 'trb']/text()").get()
            AST = logs.xpath(".//td[@data-stat = 'ast']/text()").get()
            STL = logs.xpath(".//td[@data-stat = 'stl']/text()").get()
            BLK = logs.xpath(".//td[@data-stat = 'blk']/text()").get()
            TOV = logs.xpath(".//td[@data-stat = 'tov']/text()").get()
            PF = logs.xpath(".//td[@data-stat = 'pf']/text()").get()
            PTS = logs.xpath(".//td[@data-stat = 'pts']/text()").get()
            
            if name:
            
                yield{'Athlete':name, 'Pos': pos, 'Date': date, 'Team': team, 'Opp' :opp, 'Game Result': game_result,
                      'MP': MP, 'FG': FG, 'FGA': FGA, 'FG%': FG_pct, '2P':twoP, '2PA': twoPA, '2P%':twoP_pct, '3A':threeP,'3PA':threePA,
                      '3P%':threeP_pct, 'FT':FT, 'FTA':FTA, 'FT%':FT_pct, 'ORB':ORB, 'DRB': DRB, 'TRB': TRB, 'AST': AST, 'STL': STL,
                      'BLK':BLK, 'TOV':TOV, 'PF':PF, 'PTS':PTS}

        
        if n <= 1:
            n+=1
        else:
            n = 2
        nn = str(n)
        next_page = response.xpath('((//p)[7]/a/@href)['+nn+']').get()
        if next_page:
            yield scrapy.Request(url = 'https://www.basketball-reference.com'+next_page, callback = self.parse)
            
            