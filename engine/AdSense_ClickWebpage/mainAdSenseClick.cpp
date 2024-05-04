/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: rera
 *
 * Created on March 14, 2017, 10:36 AM
 */

#include <cstdlib>
#include <iostream>
#include <string>
#include <cgicc/CgiDefs.h>
#include <cgicc/Cgicc.h>
#include <cgicc/CgiEnvironment.h>
#include <cgicc/HTTPHTMLHeader.h>
#include <cgicc/HTMLClasses.h>

#include "../AdEngine/AdEngine.hpp"


using namespace std;
string IP_Modifier = "not-vm";
//string IP_Modifier = "vm";

void GetData(string &IPAddress, string &UserResolution, string &UserOS, string &SiteURL, string &CurrentURL, 
	string &BannerID, string &Height, string &Width, string &BannerSite, string &Mobile);
void ResponceToAdSenseClick();
/*
 * 
 */

int main(int argc, char** argv)
{
	ResponceToAdSenseClick();
	return 0;
}

bool HaveQuestionSign(string Res)
{
	for(int i = 0; i < Res.length(); i++)
		if(Res[i] == '?')
			return true;
	return false;
}

bool IsFromLegalAgent(string UserOS)
{
	bool res = true;
	regex Google("Googlebot");
	smatch sm;
	
	if(regex_search(UserOS, sm, Google))
		res = false;
	
	return res;
}

string JsonizeUserData(string Mobile)
{
	return ("{'mobile':'" + Mobile + "'}");
}

void ResponceToAdSenseClick()
{
	string IPAddress = "", UserResolution = "", UserOS = "", SiteURL = "", BannerID = "", Width = "", Height = "", BannerSite = "", Debugging = "", Res = "", CurrentURL = "", Mobile = "";
	GetData(IPAddress, UserResolution, UserOS, SiteURL, CurrentURL, BannerID, Height, Width, BannerSite, Mobile);
	AdEngine engine(IP_Modifier);
	if(engine.IsAttack(IPAddress))
	{
		cout<<"Content-type:text/html; charset=utf-8\n\n";
		cout<<"Suspicious Request!";
		return;
	}
	if(!IsFromLegalAgent(UserOS))
	{
		cout<<"Content-type:text/html; charset=utf-8\n\n";
		cout<<"<meta http-equiv=\"refresh\" content=\"0; url=8tad.ir\" />";
		return;
	}
	//Debugging
//	cout<<"Content-type:text/html; charset=utf-8\n\n";
//	cout<<"Selected: " + BannerID + "<br>";
//	cout<<"Total Credit before click: " + engine.RedisSmembersFirstOne(engine.CampaignTotalBudget + BannerID) + "<br>";
//	cout<<"Daily Credit before click: " + engine.RedisSmembersFirstOne(engine.CampaignVariableDailyBudget + BannerID) + "<br>";
//	cout<<"Click cost: " + engine.RedisSmembersFirstOne(engine.ClickCost + BannerID) + "<br>";
	//
//	CurrentURL = engine.ConvertURLtoRedisFormat(CurrentURL);
//	engine.RedisSet("isequal", CurrentURL + "___" + SiteURL);
//	if(CurrentURL != "")
	string UserData = JsonizeUserData(Mobile);
	Res = engine.RedirectWhenClick(IPAddress, UserResolution, UserOS, SiteURL, BannerID, Width + "x" + Height, true, Debugging, UserData);

//	Res = engine.RedirectWhenClick("151.241.142.216", "100x100", "Mozilla/5.0-(Windows-NT-6.3;-Win64;-x64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/58.0.3029.110-Safari/537.36", "http://www.8tag.ir/", "5", "125x100", true, Debugging);

//	cout<<"Total Credit after click: " + engine.RedisSmembersFirstOne(engine.CampaignTotalBudget + BannerID) + "<br>";
//	cout<<"Daily Credit after click: " + engine.RedisSmembersFirstOne(engine.CampaignVariableDailyBudget + BannerID) + "<br>";
//	cout<<"Redirect to: " + Res + "<br>" + Debugging;

	cout<<"Content-type:text/html; charset=utf-8\n\n";
	if(Res != "")
	{
		if(Mobile != "")
			cout<<"<html><h4 style='font-family:tahoma;text-align:center;direction:rtl'>با تشکر. شماره تلفن شما ثبت شد</h4></html>";
		else if(HaveQuestionSign(Res))
			cout<<"<meta http-equiv=\"refresh\" content=\"0; url=" + Res + "\" />";
		else
		{
			string HomeURL = engine.ExtractRootURL(engine.ConvertRedisFormattoURL(SiteURL));
			string DomainURL = engine.GetRawURL(HomeURL);
			string tail = "?utm_source=8tad.ir&utm_medium=cpc&utm_content=" + DomainURL + "&utm_term=W" + Width + "H" + Height;
			cout<<"<meta http-equiv=\"refresh\" content=\"0; url=" + Res + tail + "\" />";
		}
	}
	
	else
		cout<<"Banner Not Found!";
	    //   cout<<"<meta http-equiv=\"refresh\" content=\"0; url=" + engine.ConvertRedisFormattoURL(SiteURL) + "\" />";
}

void GetData(string &IPAddress, string &UserResolution, string &UserOS, string &SiteURL, string &CurrentURL, string &BannerID, string &Height, string &Width, string &BannerSite, string &Mobile)
{
    cgicc::Cgicc scriptData;
    cgicc::CgiEnvironment CE = scriptData.getEnvironment();
    IPAddress = UserOS = UserResolution = "";
    cgicc::form_iterator fi;
    IPAddress = CE.getRemoteAddr();
    char *tmp = getenv("HTTP_USER_AGENT");
    if(tmp != NULL)
	UserOS = string(tmp);
    
    tmp = getenv("HTTP_REFERER");
    if(tmp != NULL)
	CurrentURL = string(tmp);
    
    string HashedData = "";
    fi = scriptData.getElement("h");
    if( !fi->isEmpty() && fi != (*scriptData).end()) {
       HashedData = **fi;
    }
    
    fi = scriptData.getElement("mobile");
    if( !fi->isEmpty() && fi != (*scriptData).end()) {
       Mobile = **fi;
    }
    
    AdEngine en(IP_Modifier);
    string aggData = en.RedisGet("hashedData_" + HashedData);
//    string aggData = en.RedisGet("hashedData_8600322876970063044");
//    Mobile = "09151089501";
    if(aggData == "")
	    return;
    list<string> splittedData = en.strSplit(aggData, '_');
    
    SiteURL = splittedData.back();//1
    splittedData.pop_back();
    Height = splittedData.back();//2
    splittedData.pop_back();
    Width = splittedData.back();//3
    splittedData.pop_back();
    UserResolution = splittedData.back();//4
    splittedData.pop_back();
    BannerID = splittedData.back();//5
    splittedData.pop_back();
    BannerSite = splittedData.back();//6
    splittedData.pop_back();
    
    
    
//    CurrentURL = "http://estekhdam.8tag.ir/%D8%B4%D9%87%D8%B1%DB%8C%D8%A7%D8%B1";
//    UserOS = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36";
//    cgicc::form_iterator fi = scriptData.getElement("ip_address");
//    
//    if( !fi->isEmpty() && fi != (*scriptData).end()) {
//       IPAddress = **fi;
//    }
//    else
//    {
////      cout << "No text entered for first name" << endl;  
//       //IPAddress = "2.179.168.1";
//    }
//    
//    fi = scriptData.getElement("user_os");  
//	
//    if( !fi->isEmpty() && fi != (*scriptData).end())
//       UserOS = **fi;
    //else
       //UserOS = "Win";
    
//    fi = scriptData.getElement("user_resolution");  
//	
//    if( !fi->isEmpty() && fi != (*scriptData).end())
//       UserResolution = **fi;
//    //else
//       //UserResolution = "2";
//    
//    fi = scriptData.getElement("site_url");
//    if( !fi->isEmpty() && fi != (*scriptData).end())
//       SiteURL = **fi;
//    
//    fi = scriptData.getElement("banner_id");
//    if( !fi->isEmpty() && fi != (*scriptData).end())
//       BannerID = **fi;
    
    
}

