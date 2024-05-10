/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   mainWebservice.cpp
 * Author: rera
 *
 * Created on May 7, 2017, 12:39 PM
 */

#include <cstdlib>
#include <cgicc/Cgicc.h>
#include <cgicc/CgiEnvironment.h>
#include "../AdEngine/AdEngine.hpp"
#include <jansson.h>

using namespace std;
string IP_Modifier = "not-vm";
//string IP_Modifier = "vm";

string GetAdCoreCookie(cgicc::CgiEnvironment CE)
{
	vector<cgicc::HTTPCookie> allCookies = CE.getCookieList();
	int l = allCookies.size();
	for(int i = 0; i < l; i++)
	{
		cgicc::HTTPCookie co = allCookies.back();
		allCookies.pop_back();
		if(co.getName() == "adcore")
		{
			return co.getValue();
		}
	}
	return "";
}

string GetData(string &IPAddress, string &UserResolution, string &UserOS, string &SiteURL, string &Query, string &UserName, string &Password, string &Size, string &Error, string &Cookies)
{
	cgicc::Cgicc scriptData;
	cgicc::CgiEnvironment CE = scriptData.getEnvironment();
	IPAddress = UserOS = UserResolution = "";

	IPAddress = CE.getRemoteAddr();
	char *tmp = getenv("HTTP_USER_AGENT");
	if(tmp != NULL)
	UserOS = string(tmp);
    
	tmp = getenv("HTTP_REFERER");
	if(tmp != NULL)
	    SiteURL = string(tmp);
	
	Cookies = GetAdCoreCookie(CE);
	
	string data = CE.getPostData();
	string output = data;
//	data = "{\"ip_address\": \"178.252.144.18\", \"password\": \"111111\", \"query\": \"حسابرسی مو\", \"site_url\": \"http://estekhdam.8tag.ir/\", \"size\": \"3\", \"user_agent\": \"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132-Safari/537.36\", \"user_resolution\": \"2\", \"username\": \"user@homaplus.ir\"}";
//	data = AE.RedisGet("postData");
	
	regex r("\n|\\\\n|\\n|\\\n");
	data = regex_replace(data, r, " ");
	r.assign("\r|\\\\r|\\r|\\\r");
	data = regex_replace(data, r, " ");
	r.assign("-");
	data = regex_replace(data, r, " ");
	r.assign("( )+");
	data = regex_replace(data, r, " ");
	
//	redisContext *c = redisConnect("127.0.0.1", 6379);
//	r.assign(" ");
//	string tmpData = regex_replace(data, r, "-");
//	redisCommand(c, string("SET postData " + tmpData).c_str());
//	redisFree(c);
	
	json_error_t error;
	json_t *root = json_loads(data.c_str(), 0, &error);
	json_t *Res = json_object_get(root, "user_resolution");
	if(json_is_string(Res))
		UserResolution = json_string_value(Res);
	Res = json_object_get(root, "username");
	if(json_is_string(Res))
		UserName = json_string_value(Res);
	Res = json_object_get(root, "password");
	if(json_is_string(Res))
		Password = json_string_value(Res);
	Res = json_object_get(root, "query");
	if(json_is_string(Res))
		Query = json_string_value(Res);
	Res = json_object_get(root, "size");
	if(json_is_string(Res))
		Size = json_string_value(Res);
	
	
	Res = json_object_get(root, "site_url");
	if(json_is_string(Res))
		SiteURL = json_string_value(Res);
	Res = json_object_get(root, "ip_address");
	if(json_is_string(Res))
		IPAddress = json_string_value(Res);
	Res = json_object_get(root, "user_agent");
	if(json_is_string(Res))
		UserOS = json_string_value(Res);
	
	
	
//	cgicc::form_iterator fi;
//	fi = scriptData.getElement("user_resolution");  
//	if( !fi->isEmpty() && fi != (*scriptData).end())
//	   UserResolution = **fi;
//
//	fi = scriptData.getElement("username");
//	if( !fi->isEmpty() && fi != (*scriptData).end())
//	   UserName = **fi;
//
//	    fi = scriptData.getElement("password");
//	if( !fi->isEmpty() && fi != (*scriptData).end())
//	   Password = **fi;
//
//	fi = scriptData.getElement("query");
//	if( !fi->isEmpty() && fi != (*scriptData).end())
//	   Query = **fi;
//
//	fi = scriptData.getElement("size");
//	if( !fi->isEmpty() && fi != (*scriptData).end())
//	   Size = **fi;
//
//	fi = scriptData.getElement("site_url");
//	if( !fi->isEmpty() && fi != (*scriptData).end())
//	   SiteURL = **fi;

	//    fi = scriptData.getElement("ip_address");
	//    if( !fi->isEmpty() && fi != (*scriptData).end())
	//       IPAddress = **fi;
	return output;
}

void SendBanner(list<AdwordsPackage> SelectedBanners, string SiteURL, string UserResolution, string UserQuery, string Debugging, string Error)
{
	int l = SelectedBanners.size();
	cout<<"Content-type:application/json; charset=utf-8\n\n";
	if(Error != "")
	{
		cout<<Error;
		return;
	}
	string ReturnValue = "{ \"Results\" : [";
	AdEngine engine(IP_Modifier);
	for(int i = 0; i < l; i++)
	{
		AdwordsPackage tmp = SelectedBanners.back();
		SelectedBanners.pop_back();
		string RedisURL = engine.ConvertURLtoRedisFormat(SiteURL);
		string Data = RedisURL + "_" + UserResolution + "_" + tmp.BannerID + "_" + engine.ConvertURLtoRedisFormat(tmp.Website) + "_" + UserQuery;
		hash<string> hs;
		tmp.HashedData = to_string(hs(Data));
		engine.RedisSet("hashedData_" + tmp.HashedData, Data);
		string json = "{ \"title\" : \"" + tmp.Title + "\", " +
			"\"description\" : \"" + tmp.Description + "\", " +
			//"\"debug\" : \"" + Debugging + "\", " +
			"\"email\" : \"" + tmp.Email + "\", " +
			"\"phone\" : \"" + tmp.Phone + "\", " +
			"\"address\" : \"" + tmp.Address + "\", " +
			"\"ID\" : \"" + tmp.BannerID + "\", " +
//			"\"landing_url\" : \"http://31.184.132.157:4444/cgi-bin/cws.sh?h=" + tmp.HashedData + "\" }";
//			"\"landing_url\" : \"http://click.adcore.ir/click/cws.sh?h=" + tmp.HashedData + "\" }";
			"\"landing_url\" : \"http://click.8tad.ir/click/cws.sh?h=" + tmp.HashedData + "\" }";
		ReturnValue = ReturnValue + json;
		if(i < l - 1)
			ReturnValue += ",";
	}
	ReturnValue = ReturnValue + "] }";
	cout<<ReturnValue;
}

void ResponceToAdWordsRequest()
{
    AdEngine engine(IP_Modifier);
    string IPAddress = "", UserResolution = "", UserOS = "", SiteURL = "", Query = "", Debugging = "", UserName = "", Password = "",
	    Size = "", Error = "", Cookies = "", apiAddress;
    apiAddress = "http://192.168.156.28:5555/api/normalizer/string";
//    apiAddress = "http://8tad.ir/api/normalizer/string";
    string output = GetData(IPAddress, UserResolution, UserOS, SiteURL, Query, UserName, Password, Size, Error, Cookies);
    engine.RedisSet("adwords_query", output);
//    IPAddress = "151.241.142.216", UserResolution = "", UserOS = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", SiteURL = "http://www.8tag.ir", Query = "فروشگاه اینترنتی", UserName = "publisher@adcore.ir", Password = "111111", Size = "3";
    try
    {
	    int k = stoi(Size);
    }
    catch(exception e)
    {
	    Size = "1";
    }
    list<AdwordsPackage> SelectedBanners = engine.FindSuitableBannerAdWords(IPAddress, UserResolution, UserOS, SiteURL, Query, Debugging,
	    UserName, Password, stoi(Size), Error, Cookies, apiAddress);
    SendBanner(SelectedBanners, SiteURL, UserResolution, Query, Debugging, Error);
}

int main(int argc, char** argv)
{
	ResponceToAdWordsRequest();
	return 0;
}