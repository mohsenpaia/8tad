/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: rera
 *
 * Created on February 27, 2017, 7:05 AM
 */

#include <cstdlib>
#include <iostream>
#include <cgicc/CgiDefs.h>
#include <cgicc/Cgicc.h>
#include <cgicc/CgiEnvironment.h>
#include <cgicc/HTTPHTMLHeader.h>
#include <cgicc/HTMLClasses.h>

#include "../AdEngine/AdEngine.hpp"

using namespace std;
using namespace cgicc;
string IP_Modifier = "not-vm";
//string IP_Modifier = "vm";

void GetData(string &IPAdress, string &UserResolution, string &UserOS, string &SiteURL, string &Height, string &Width, string &Cookies);
void ShowBanner(string BannerFile, string HashedData, string Height, string Width, string DomainURL, string statistical);
void ShowHTML(string BannerFile, string HashedData, string Height, string Width, string DomainURL, string HTML);
string GetAdCoreCookie(cgicc::CgiEnvironment CE);
void ResponceToAdSenseRequest();
/*
 * 
 */
int main(int argc, char** argv) {
	ResponceToAdSenseRequest();
	return 0;
}

void ResponceToAdSenseRequest()
{
	string IPAddress = "", BannerFile = "", UserResolution = "", UserOS = "", SiteURL = "", Height = "", Width = "", BannerID, Debugging = "", Cookies = "";
	GetData(IPAddress, UserResolution, UserOS, SiteURL, Height, Width, Cookies);
	AdEngine engine(IP_Modifier);
	engine.RedisSet("lastip", IPAddress);
	
	engine.RedisSet("lastrequest", IPAddress + "_" + UserResolution + "_" + UserOS + "_" + engine.ConvertURLtoRedisFormat(SiteURL)
			+ "_" + Height + "_" + Width + "_" + Cookies);
	

	string HomeURL = engine.ExtractRootURL(SiteURL);
	string DomainURL = engine.GetRawURL(HomeURL);
	if(DomainURL == "faraazin.ir")
		engine.RedisSet("faraazin", IPAddress + "_" + UserResolution + "_" + UserOS + "_" + engine.ConvertURLtoRedisFormat(SiteURL)
			+ "_" + Height + "_" + Width + "_" + Cookies);
	string BannerSite = "";
	BannerID = engine.FindSuitableBannerAdSense(IPAddress, UserResolution, UserOS, SiteURL, stoi(Height), stoi(Width), BannerFile, BannerSite, Debugging, Cookies);
//	BannerID = engine.FindSuitableBannerAdSense("31.214.154.91", "", "Mozilla/5.0-(Windows-NT-10.0;-Win64;-x64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/58.0.3029.110-Safari/537.36", "http://estekhdam.8tag.ir/search?q=%D9%BE%D8%B1%D8%B3%D9%BE%D9%88%D9%84%DB%8C%D8%B3", stoi("90"), stoi("970"), BannerFile, BannerSite, Debugging, "");
//	BannerID = engine.FindSuitableBannerAdSense("178.252.144.18", "300x600", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "estekhdam.8tag.ir/", stoi("300"), stoi("600"), BannerFile, BannerSite, Debugging, "");
	if(BannerID != "")
	{
		string RedisURL = engine.ConvertURLtoRedisFormat(SiteURL);
		string Data = RedisURL + "_" + Height + "_" + Width + "_" + UserResolution + "_" + BannerID + "_" + engine.ConvertURLtoRedisFormat(BannerSite);
		hash<string> hs;
		string HashedData = to_string(hs(Data));

		engine.RedisSet("hashedData_" + HashedData, Data);

		string statistical = "Selected: " + BannerID + "<br>" +
		"Total Credit before click: " + engine.RedisSmembersFirstOne(engine.CampaignTotalBudget + BannerID) + "<br>" +
		"Daily Credit before click: " + engine.RedisSmembersFirstOne(engine.CampaignConstantDailyBudget + BannerID) + "<br>" +
		"Click cost: " + engine.RedisSmembersFirstOne(engine.ClickCost + BannerID) + "<br>";

		
		
		string HomeURL = engine.ExtractRootURL(SiteURL);
		string DomainURL = engine.GetRawURL(HomeURL);
		string BannerType = engine.RedisSmembersFirstOne(engine.CampaignType + BannerID);
		if(BannerType == "banner")
			ShowBanner(BannerFile, HashedData, Height, Width, DomainURL, Debugging + " " + statistical);
		else if (BannerType == "html")
		{
			string HTML = engine.RedisSmembersFirstOne(engine.Campaignstr + BannerID + engine.HTMLstr + Width + "x" + Height);
			ShowHTML(BannerFile, HashedData, Height, Width, DomainURL, HTML);
		}
		
		engine.RedisSet("mobug", IPAddress + "_" + BannerFile + "_" + UserResolution + "_" + UserOS + "_" +
			engine.ConvertURLtoRedisFormat(SiteURL) + "_" + Height + "_" + Width + "_" + BannerID);
		
	}
	else
	{
		cout<<"Content-Type:text/html; charset=utf-8\n\n";
		cout<<"<html><h4 style='font-family:tahoma;text-align:center;direction:rtl'>نمایش‌دهنده‌ی محترم، لطفا منتظر منتظر تایید کارشناسان سامانه هشتاد بمانید!!</h4></html>";
	}
}

void GetData(string &IPAddress, string &UserResolution, string &UserOS, string &SiteURL, string &Height, string &Width, string &Cookies)
{
    Cgicc scriptData;
    CgiEnvironment CE = scriptData.getEnvironment();
    IPAddress = UserOS = UserResolution = "";
    
    IPAddress = CE.getRemoteAddr(); 
    char *tmp = getenv("HTTP_USER_AGENT");
    if(tmp != NULL)
	UserOS = string(tmp);
    
    
    tmp = getenv("HTTP_REFERER");
    if(tmp != NULL)
	SiteURL = string(tmp);
    
    Cookies = GetAdCoreCookie(CE);
    
    form_iterator fi;
//    
    fi = scriptData.getElement("ip_address");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       IPAddress = **fi;
 
    fi = scriptData.getElement("user_os");  
    if( !fi->isEmpty() && fi != (*scriptData).end())
       UserOS = **fi;
    
    fi = scriptData.getElement("user_resolution");  
    if( !fi->isEmpty() && fi != (*scriptData).end())
       UserResolution = **fi;
    
    fi = scriptData.getElement("site_url");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       SiteURL = **fi;
    
    fi = scriptData.getElement("banner_height");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       Height = **fi;
    
    fi = scriptData.getElement("banner_width");  
    if( !fi->isEmpty() && fi != (*scriptData).end())
       Width = **fi;
    
    
//    		5.78.208.52_0625f776-b3da-4413-8154-5dcc7bd77fe0/320_48.gif__Mozilla/5.0-(iPhone;-CPU-iPhone-OS-11_1_2-like-Mac-OS-X)-AppleWebKit/604.1.34-(KHTML,-like-Gecko)-CriOS/62.0.3202.70-Mobile/15B202-Safari/604.1_http://estekhdam.8tag.ir/_48_320_90
//    IPAddress = "188.253.44.113";
//    UserOS = "Mozilla/5.0-(Windows-NT-6.1;-WOW64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/41.0.2272.76-Safari/537.36";
//    UserResolution = 2;
//    SiteURL = "http://faraazin.ir";
//    Height = "300";
//    Width = "600";
    
//    IPAddress = "188.253.44.113";
//    UserOS = "Mozilla/5.0-(Windows-NT-6.1;-WOW64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/41.0.2272.76-Safari/537.36";
//    UserResolution = 2;
//    SiteURL = "http://www.eghtesadnews.com/%D8%A8%D8%AE%D8%B4-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D8%AF%D8%B1-%D8%B1%D8%B3%D8%A7%D9%86%D9%87-%D9%87%D8%A7-67/196921-%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%AE%D8%A8%D8%B1-%D8%A7%D8%B2-%DB%8C%D8%A7%D8%B1%D8%A7%D9%86%D9%87-%DB%8C%D8%A7%D8%B1%D8%A7%D9%86%D9%87-%D9%85%DB%8C%D9%84%DB%8C%D9%88%D9%86-%D9%86%D9%81%D8%B1-%D9%82%D8%B7%D8%B9-%D9%85%DB%8C-%D8%B4%D9%88%D8%AF?rssRedirect=c2hhaHJla2hhYmFyLmNvbQ%3D%3D&utm_source=shahrekhabar_com&utm_medium=rss&utm_campaign=rssreaders";
//    Height = "240";
//    Width = "120";
}

void ShowHTML(string BannerFile, string HashedData, string Height, string Width, string DomainURL, string HTML)
{
	regex r("action=\"\"");
	string clickInterface= "sms.sh?h=" + HashedData;
	string url = "action='http://click.8tad.ir/click/" + clickInterface + "'";
	string Res = regex_replace(HTML, r, url);
	cout<<"Content-Type:text/html; charset=utf-8\n\n";
	cout<<Res;
}


void ShowBanner(string BannerFile, string HashedData, string Height, string Width, string DomainURL, string statistical)
{
	string clickInterface= "cwp.sh?h=" + HashedData;
	cout<<"Content-Type:text/html; charset=utf-8\n\n";
//	cout<<"<html>\n";
//	cout<<"<body>\n";
	
	
	
	
	string s = "<html lang='fa'>";
	s = s + "<head>"+
	"    <meta charset='utf-8'>"+
	"    <meta name='robots' content='noindex,nofollow'>"+
	"    <style>   "+
	"	* {"+
	"        box-sizing: border-box"+
	"    }"+
	""+
	"    body {"+
	"        margin: 0;"+
	"        padding: 0;"+
	"        font-family: tahoma;"+
	"        font-size: 8pt"+
	"    }"+
	""+
	"    a {"+
	"        text-decoration: none"+
	"    }"+
	""+
	"    #ad-link img {"+
	"        max-width: 100%;"+
	"        max-height: 100%;"+
	"    }"+
	""+
	"    .ad-logo {"+
	"        position: absolute;"+
	"        left: 19px;"+
	"        z-index: 10;"+
	"        background-color: #ccc;"+
	"        opacity: 0.9;"+
	"		float: left;"+
	"		bottom: 0;"+
	"    }"+
	""+
	"    .ad-logo:hover #ad-logo-co {"+
	"        width: 35px;"+
	"        padding: 0 3px 1px;"+
	"        visibility: visible;"+
	"        opacity: 1;"+
	"        background-color: #fff;"+
	"    }"+
	""+
	"    .ad-logo:hover {"+
	"        opacity: 1;"+
	"        background-color: #fff;"+
	"    }"+
	""+
	"    #icon {"+
	"        float: right;"+
	"        border: 0;"+
	"        margin: 0;"+
	"        padding: 0;"+
	"    }"+
	""+
	"    #ad-logo-co {"+
	"        width: 0;"+
	"        overflow: hidden;"+
	"        float: right;"+
	"        border-bottom: 0;"+
	"        border-right: 0;"+
	"        height: 18px;"+
	"        line-height: 18px;"+
	"        white-space: nowrap;"+
	"        visibility: hidden;"+
	"        opacity: 0;"+
	"        -webkit-transition: .2s;"+
	"        transition: .2s;"+
	"        color: #324e6a;"+
	"        font-size: 11px;"+
	"    }"+
	""+
	"    #ad-close {"+
	"        width: 18px;"+
	"        height: 18px;"+
	"        display: block;"+
	"        position: absolute;"+
	"        left: 0px;"+
	"        z-index: 8;"+
	"        background-image: url('http://8tad.ir/static/frontend/images/close.png');"+
	"        background-position: center center;"+
	"        background-repeat: no-repeat;"+
	"        cursor: pointer;"+
	"        transition: .2s;"+
	"        background-color: #ccc;"+
	"        opacity: 0.9;"+
	"		bottom: 0;"+
	"    }"+
	""+
	"    #ad-close:hover {"+
	"        background-color: #fff;"+
	"    }"+
	""+
	"    body:hover #ad-close {"+
	"        opacity: 1"+
	"    } "+
	"	"+
	"	#ad-frame{"+
	"	   position: relative;"+
	"	   float:right;"+
	"    }"+
	"	"+
	"	#ad-link{"+
	"	 float:right;"+
	"	}"+
	"	</style>"+
	"</head>"+
	"<body>"+
	"<table style='width:100%; height:100%;' border='0' cellspacing='0' cellpadding='0'>"+
	"        <tr>"+
	"            <td style='vertical-align:middle;'>"+
	"<div id='ad-frame'>"+
	"<a href='http://click.8tad.ir/click/" + clickInterface + "' target='_blank' id='ad-link'><img src='http://8tad.ir/static/uploads/"+ BannerFile +"' width='100%' height='auto' border='0'></a>"+
	"    <div class='ad-logo'>"+
	"	<a title='سامانه هوشمند تبلیغات آنلاین'"+
	"                            href='http://8tad.ir/?utm_source=" + DomainURL + "&amp;utm_campaign=adsbutton&amp;utm_medium=adsbutton'"+
	"                            style=' border: 0; ' target='_blank'> <img"+
	"            src='http://8tad.ir/static/frontend/images/8tad.png' id='icon' alt='adbutton' width='18' height='18'>"+
	"        <div id='ad-logo-co'>هشتاد</div>"+
	"    </a>"+
	"	</div>"+
	"    <span id='ad-close' class=''></span>"+
	"	</div>"+
	"	            </td>"+
	"        </tr>"+
	"    </table>"+
	"<script>!(function (w, d) {"+
	"    d.getElementById('ad-close').onclick = function () {"+
	"        var frame = d.getElementById('ad-frame');"+
	"        frame.parentNode.removeChild(frame);"+
	"    };"+
	"})(this, document);</script>"+
		

	"</body>"+
	"</html>";
	
//	string s = "<a href='http://click.8tad.ir/click/" + clickInterface + "' target='_blank'>" +
//		"<img src='http://8tad.ir/static/uploads/"+ BannerFile +"' alt='MISSING JPG' width='" + Width + "' height='" + Height + "' />" +
//		"</a>";
//	string s = "<a href='http://31.184.132.157:4444/cgi-bin/" + clickInterface + "' target='_blank'>" +
//		"<img src='http://8tad.ir/static/uploads/"+ BannerFile +"' alt='MISSING JPG' width='" + Width + "' height='" + Height + "' />" +
//		"</a>";
//	string s = "<a href='http://127.0.0.1/cgi-bin/" + clickInterface + "' target='_blank'>" +
//		"<img src='http://127.0.0.1/"+ BannerFile +"' alt='MISSING JPG' width='" + Width + "' height='" + Height + "' />" +
//		"</a>";
	if(BannerFile != "")
		cout<<s;
	
//	cout<<"<br>" + statistical + "<br>";
	
//	cout<<"</body>\n";
//	cout<<"</html>\n";
}

string GetAdCoreCookie(cgicc::CgiEnvironment CE)
{
	vector<HTTPCookie> allCookies = CE.getCookieList();
	int l = allCookies.size();
	for(int i = 0; i < l; i++)
	{
		HTTPCookie co = allCookies.back();
		allCookies.pop_back();
		if(co.getName() == "8tad")
		{
			return co.getValue();
		}
	}
	return "";
}