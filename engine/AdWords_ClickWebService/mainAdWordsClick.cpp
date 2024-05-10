/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   mainAdWordsClick.cpp
 * Author: rera
 *
 * Created on May 8, 2017, 9:31 AM
 */

#include <cstdlib>
#include <cgicc/Cgicc.h>
#include <cgicc/CgiEnvironment.h>
#include "../AdEngine/AdEngine.hpp"

using namespace std;
//string IP_Modifier = "not-vm";
string IP_Modifier = "vm";

void GetData(string &IPAddress, string &UserResolution, string &UserOS, string &SiteURL, string &BannerID, string &BannerSite, string &UserQuery)
{
    cgicc::Cgicc scriptData;
    cgicc::CgiEnvironment CE = scriptData.getEnvironment();
    IPAddress = UserOS = UserResolution = "";
    cgicc::form_iterator fi;
    IPAddress = CE.getRemoteAddr();
    char *tmp = getenv("HTTP_USER_AGENT");
    if(tmp != NULL)
	UserOS = string(tmp);
    
    string HashedData = "";
    fi = scriptData.getElement("h");
    if( !fi->isEmpty() && fi != (*scriptData).end()) {
       HashedData = **fi;
    }
    
    AdEngine en(IP_Modifier);
    string aggData = en.RedisGet("hashedData_" + HashedData);
    if(aggData == "")
	    return;
//    aggData = en.RedisGet("hashedData_9037515474422149900");
    list<string> splittedData = en.strSplit(aggData, '_');
    
    SiteURL = splittedData.back();//1
    splittedData.pop_back();
    UserResolution = splittedData.back();//2
    splittedData.pop_back();
    BannerID = splittedData.back();//3
    splittedData.pop_back();
    BannerSite = splittedData.back();//4
    splittedData.pop_back();
    UserQuery = splittedData.back();//5
    splittedData.pop_back();
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



void ResponceToAdWordsClick()
{
	string IPAddress = "", UserResolution = "", UserOS = "", SiteURL = "", BannerID = "", UserQuery = "", BannerSite = "", Debugging = "";
	GetData(IPAddress, UserResolution, UserOS, SiteURL, BannerID, BannerSite, UserQuery);
	
	//IPAddress = "151.241.142.216"; UserOS = "Mozilla/5.0-(X11;-Ubuntu;-Linux-x86_64;-rv:53.0)-Gecko/20100101-Firefox/53.0", "http://www.8tag.ir/";
	AdEngine engine(IP_Modifier);
	BannerSite = engine.ConvertRedisFormattoURL(BannerSite);
	if(engine.IsAttack(IPAddress))
	{
		cout<<"Content-type:text/html\n\n";
		cout<<"Suspicious Request!";
		return;
	}

	if(!IsFromLegalAgent(UserOS))
	{
		cout<<"Content-type:text/html\n\n";
		cout<<"<meta http-equiv=\"refresh\" content=\"0; url=8tad.ir\" />";
		return;
	}
	//    cout<<"Content-Type:text/html; charset=utf-8\n\n";
	//    cout<<"Selected: " + BannerID + "<br>";
	//    cout<<"Total Credit before click: " + engine.RedisSmembersFirstOne(engine.CampaignTotalBudget + BannerID) + "<br>";
	//    cout<<"Daily Credit before click: " + engine.RedisSmembersFirstOne(engine.CampaignVariableDailyBudget + BannerID) + "<br>";
	//    cout<<"Click cost: " + engine.RedisSmembersFirstOne(engine.ClickCost + BannerID) + "<br>";

	string Res = engine.RedirectWhenClick(IPAddress, UserResolution, UserOS, SiteURL, BannerID, UserQuery, false, Debugging, "");

	//    cout<<"Total Credit after click: " + engine.RedisSmembersFirstOne(engine.CampaignTotalBudget + BannerID) + "<br>";
	//    cout<<"Daily Credit after click: " + engine.RedisSmembersFirstOne(engine.CampaignVariableDailyBudget + BannerID) + "<br>";
	//    cout<<"Redirect to: " + Res + "<br>" + Debugging;

	//    string Res = engine.RedirectWhenClick("127.0.0.1", "2", "Mozilla/5.0-(X11;-Ubuntu;-Linux-x86_64;-rv:53.0)-Gecko/20100101-Firefox/53.0", "http://www.8tag.ir/", "defaultBanner");
	//    cout<<"Content-type:application/json\n\n";
	//    cout<<"{ \"Landing_Page\" : \"" + Res + "\" }";
	cout<<"Content-type:text/html\n\n";
	if(Res != "")
	    cout<<"<meta http-equiv=\"refresh\" content=\"0; url=" + Res + "\" />";
	
	else
	    cout<<"<meta http-equiv=\"refresh\" content=\"0; url=" + engine.ConvertRedisFormattoURL(SiteURL) + "\" />";
}

/*
 * 
 */
int main(int argc, char** argv)
{
	ResponceToAdWordsClick();
	return 0;
}

