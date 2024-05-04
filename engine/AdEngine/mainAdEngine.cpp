/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: rera
 *
 * Created on February 18, 2017, 5:20 AM
 */

#include <cstdlib>
#include <stdio.h>

using namespace std;
#include <string>
#include <map>
#include <fstream>
#include <iostream>
#include <list>
#include <vector>
#include <chrono>

#include "AdEngine.hpp"

void RedisTest();

int main(int argc, char** argv) {  
    
// Instanciate elasticsearch client.
//    ElasticSearch es("localhost:9200");
    //    unsigned long int Res = IPv4AddresstoIPNumber("202.186.13.4");
//    string Res1 = IPNumbertoIPv4Address(3401190660);
//    RedisTest();
//    LoadIPNumbertoCityPairs();
    AdEngine AE;
    string Debugging = "";
    AE.RedirectWhenClick("151.241.142.216", "100x100", "Mozilla/5.0-(Windows-NT-6.3;-Win64;-x64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/58.0.3029.110-Safari/537.36", "http://www.8tag.ir/", "5", "125x100", true, Debugging, "");
//    string r = AE.GetRootQuery("فروشگاه-اینترنتی-من");
//    AE.LoadIP2LocationToRedis();
//    AE.LoadIP2LocationFromRedis();
    
//    string city = AE.NewIP2Location("2.181.5.1");
//    AE.Elasticsearch_UpdateCampaignForURL("http://www.google.com/", "2");
//    AE.SaveSiteContentstoElasticsearch("http://www.varzesh3.com/news/1401386/%D8%AF%DB%8C%D8%AF%D8%A7%D8%B1-%D9%82%D8%B7%D8%B1-%D8%A8%D8%A7-%D8%A2%D8%B0%D8%B1%D8%A8%D8%A7%DB%8C%D8%AC%D8%A7%D9%86-%D9%BE%D8%B4%D8%AA-%D8%AF%D8%B1%D9%87%D8%A7%DB%8C-%D8%A8%D8%B3%D8%AA%D9%87");
//    bool b = AE.IsRegisteredWebsite("www.google.com");
//    redisReply *s = AE.RedisSmembers("cityTehran");
//    AE.FetchPendingWebpages();
//    
//    AE.AssignBannersToURL("http,@@www.asriran.com@f%8C_%D9%86%D8%A7%D9%85%D8%B2%D8%AF_%D9%BE%D9%88%D8%B4%D8%B4%DB%8C_%DA%86%DB%8C%D8%B3%D8%AA");
//    string s = " <!DOCTYPE HTML> <html> <head></div> </div> </body> </html>";
//    AE.HTMLToContent(s);
//    string BannerSite = "", BannerFile = "";
//    string tmp = AE.FindSuitableBannerAdSense("209.95.51.176", "2", "Win", "www.90tv.ir", 100, 100, BannerFile, BannerSite);
    return 0;
}

void RedisTest()
{
    redisContext *c = redisConnect("127.0.0.1", 6379);
    if (c == NULL || c->err) {
        if (c) {
            printf("Error: %s\n", c->errstr);
            // handle error
        } else {
            printf("Can't allocate redis context\n");
        }
    }
    redisReply * reply = (redisReply *)redisCommand(c, "GET ali");
    printf("Result: %s", reply->str);
}



