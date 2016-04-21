#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__plugin__ = 'GoogleScraper'

import argparse
import logging
import os
from GoogleScraper import scrape_with_config, GoogleSearchError
try:
    import coloredlogs
    colored_logs_present = True
except:
    print("(Install 'coloredlogs' for colored logging)")
    colored_logs_present = False


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    # parse input arguments
    parser = argparse.ArgumentParser(prog=__file__,
                                     description="Task runner for SCAPL plugin {}.".format(__plugin__),
                                     epilog="Usage example:\n python3 {} -q test -n 10".format(__file__),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--config", dest="config",
                        help="task configuration dictionary")
    parser.add_argument("--keywords", help="keywords to be scraped")
    parser.add_argument("--task", help="task identifier for logging purpose")
    parser.add_argument("-n", dest="n", type=int, default=0, help="number of results to return [default: 0 (=all)]")
    parser.add_argument("-v", dest="verbose", action="count", default=0,
                        help="verbose level [default: 0 (critical)]")
    args = parser.parse_args()
    args.config = eval(args.config)
    # configure logging and get the root logger
    args.verbose = args.config['LOG_LEVEL_MAPPING'][min(max(args.config['LOG_LEVEL_MAPPING'].keys()), args.verbose)]
    logging.basicConfig(format='%(name)s - %(asctime)s [%(levelname)s] %(message)s', level=args.verbose)
    logger = logging.getLogger(args.task)
    if colored_logs_present:
        coloredlogs.install(args.verbose)
    # now, prepare task-specific configuration
    config = {
        'use_own_ip': True,
        'keyword': args.keywords,
        'search_engines': ['google'],
        'scrape_method': 'http',
        'do_caching': True,
    }
    if args.n > 0:
        config.update({'num_pages_for_keyword': args.n})
    if 'PROXY_FILE' in args.config and args.config['PROXY_FILE'] not in [None, '']:
        config.update({'proxy_file': args.config['PROXY_FILE'], 'check_proxies': False})
        # NB: check_proxies is a parameter aimed to make the (public) proxy address checked on a website,
        #     so if using a private network proxy, this check is not required
    # try to scrape on keywords and to get a connection to the cache database
    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        logger.error(str(e))
        print(e)
        exit(1)
    # collect found links
    links, suggestions = [link for serp in search.serps for link in serp.links], []
    for link in sorted(links, key=lambda k: k.rank)[:args.n if args.n > 0 else None]:
        suggestions.append({'link': link.link, 'title': link.title, 'text': link.snippet})
    print(suggestions)
