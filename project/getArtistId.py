#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys  
import re
import urllib2
import json
import csv
import codecs
import os
import socket
from socket import AF_INET, SOCK_DGRAM



def search(search_term, client_access_token):
    #Unfortunately, looks like it maxes out at 50 pages (approximately 1,000 results), roughly the same number of results as displayed on web front end
    page=1
    songs = []
    for i in range(0, 30):
        querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_term) + "&page=" + str(page)
        request = urllib2.Request(querystring)
        request.add_header("Authorization", "Bearer " + client_access_token)   
        request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
        while True:
            try:
                response = urllib2.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
                raw = response.read()
            except socket.timeout:
                print("Timeout raised and caught")
                continue
            break
        json_obj = json.loads(raw)
        body = json_obj["response"]["hits"]

        num_hits = len(body)
        if num_hits==0:
            if page==1:
                print("No results for: " + search_term)
            break      
        #print("page {0}; num hits {1}".format(page, num_hits))
        
        for result in body:
            result_id = result["result"]["id"]
            title = result["result"]["title"]
            if title.find("Tracklist") != -1:
                continue
            url = result["result"]["url"]
            path = result["result"]["path"]
            header_image_url = result["result"]["header_image_url"]
            annotation_count = result["result"]["annotation_count"]
            pyongs_count = result["result"]["pyongs_count"]
            primaryartist_id = result["result"]["primary_artist"]["id"]
            primaryartist_name = result["result"]["primary_artist"]["name"]
            primaryartist_url = result["result"]["primary_artist"]["url"]
            primaryartist_imageurl = result["result"]["primary_artist"]["image_url"]
            row=[page,result_id,title,url,path,header_image_url,annotation_count,pyongs_count,primaryartist_id,primaryartist_name,primaryartist_url,primaryartist_imageurl]
            songs.append(row)
        page+=1
    return songs

def main():
    arguments = sys.argv[1:] #so you can input searches from command line if you want
    search_term = arguments[0].translate(None, "\'\"")
    client_access_token = "rTNAfXuSPK2GWd6eXtmZwuHVMitzHO-iAl5CKKPNiQ-m2arGCN7eqRRRy7v1F6j8"
    search(search_term, client_access_token)

if __name__ == '__main__':
    main()
