#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from GoogleScraper import scrape_with_config, GoogleSearchError
from lib import TaskRunner


@TaskRunner.bind(__file__, 'GoogleScraper')
def run(self):
    n = self.param['n'] * 10  # multiplier is set to collect far more results than required for establishing suggestions
    MAX_PER_PAGE = 100        # this is a limit imposed by GoogleScraper
    config = {
        'use_own_ip': True,
        'keyword': self.param['keywords'],
        'search_engines': ['google'],
        'scrape_method': 'http',
        'do_caching': False,
        'log_level': self.verbose,
        'num_pages_for_keyword': len(range(0, n, MAX_PER_PAGE)) if n > 0 else 1,
        'num_results_per_page': min(n, MAX_PER_PAGE) if n > 0 else MAX_PER_PAGE,
    }
    if 'PROXY_FILE' in self.config and self.config['PROXY_FILE'] not in [None, '']:
        config.update({'proxy_file': self.config['PROXY_FILE'], 'check_proxies': False})
        # NB: check_proxies is a parameter aimed to make the (public) proxy address checked on a website,
        #     so if using a private network proxy, this check is not required
    # scrape on keywords and get a connection to the cache database
    search = scrape_with_config(config)
    # check the status and raise an exception if scraping failed
    for serp in search.serps:
        if serp.status != 'successful' and serp.no_results:
            self.logger.error(serp.status)
            exit(1)
    # collect found links
    links, suggestions = [link for serp in search.serps for link in serp.links], []
    k, l = 0, len(links)
    while len(suggestions) < self.param['n'] and k < l:
        # TODO: write a filter
        #  e.g. for:
        #  - favouring links with domain containing one or more of the keywords)
        #  - excluding links on specific forums and/or download sites
        #  - exluding maliious domains acording to Norton Safe Web or other security sources (e.g. Webputation)
        suggestions.append({'link': links[k].link, 'title': links[k].title, 'text': links[k].snippet})
        k += 1
    return suggestions


if __name__ == '__main__':
    run()
