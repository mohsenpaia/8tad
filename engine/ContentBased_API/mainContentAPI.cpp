//publishers_website_
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
void GetData(string &IPAdress, string &UserResolution, string &UserOS, string &SiteURL, string &Height, string &Width, string &Cookies, string &SiteID, string &strCount, string &Element);
void ShowBanner(list<ContentPackage> SelectedBanners, string SiteURL, string UserResolution, string UserQuery, string Debugging, string count);
string GetAdCoreCookie(cgicc::CgiEnvironment CE);
string MakeOutputJavascript(string ElementID, string SiteURL, list<ContentPackage> Banners, string UserResolution, string Count);
void ResponceToContentRequest();
/*
 * 
 */
string DatabaseIP = "vm";

int main(int argc, char** argv) {
	ResponceToContentRequest();
	return 0;
}

void ResponceToContentRequest()
{
	string IPAddress = "", UserResolution = "", UserOS = "", SiteURL = "", Height = "", Width = "", Debugging = "", Cookies = "", SiteID = "", strCount = "0", Element = "";
	GetData(IPAddress, UserResolution, UserOS, SiteURL, Height, Width, Cookies, SiteID, strCount, Element);
	int realCount = 1;
	if(strCount == "4x1" || strCount == "1x4")
		realCount = 4;
	else
		realCount = 1;
	AdEngine engine(DatabaseIP);
	SiteURL = engine.RedisSmembersFirstOne(engine.WebsiteToID + SiteID);
	list<ContentPackage> BannerIDs = engine.FindSuitableBannerContent(IPAddress, UserResolution, UserOS, SiteURL, stoi(Height), stoi(Width), Debugging, Cookies, realCount);

//	BannerID = engine.FindSuitableBannerAdSense("31.214.154.91", "", "Mozilla/5.0-(Windows-NT-10.0;-Win64;-x64)-AppleWebKit/537.36-(KHTML,-like-Gecko)-Chrome/58.0.3029.110-Safari/537.36", "http://estekhdam.8tag.ir/search?q=%D9%BE%D8%B1%D8%B3%D9%BE%D9%88%D9%84%DB%8C%D8%B3", stoi("90"), stoi("970"), BannerFile, BannerSite, Debugging, "");
//	BannerID = engine.FindSuitableBannerAdSense("178.252.144.18", "300x600", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "estekhdam.8tag.ir/", stoi("300"), stoi("600"), BannerFile, BannerSite, Debugging, "");
	if(BannerIDs.size() != 0)
	{
		ShowBanner(BannerIDs, SiteURL, UserResolution, Element, Debugging, strCount);
	}
}

void GetData(string &IPAddress, string &UserResolution, string &UserOS, string &SiteURL, string &Height, string &Width, string &Cookies, string &SiteID, string &Count, string &Element)
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
    
    fi = scriptData.getElement("host_id");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       SiteID = **fi;
    
    fi = scriptData.getElement("element_id");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       Element = **fi;
 
    fi = scriptData.getElement("user_os");  
    if( !fi->isEmpty() && fi != (*scriptData).end())
       UserOS = **fi;
    
    fi = scriptData.getElement("user_resolution");  
    if( !fi->isEmpty() && fi != (*scriptData).end())
       UserResolution = **fi;
    
    fi = scriptData.getElement("site_url");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       SiteURL = **fi;    
    
    fi = scriptData.getElement("count");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       Count = **fi;
    
    fi = scriptData.getElement("banner_height");
    if( !fi->isEmpty() && fi != (*scriptData).end())
       Height = **fi;
    
    fi = scriptData.getElement("banner_width");  
    if( !fi->isEmpty() && fi != (*scriptData).end())
       Width = **fi;
    
    
    IPAddress = "31.214.172.118";
    UserOS = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36";
    UserResolution = "2";
    SiteURL = "http://takaroosi.com/%D8%A8%D8%B1%D8%AA%D8%B1%DB%8C%D9%86-%D8%A7%DB%8C%D8%AF%D9%87-%D9%87%D8%A7%DB%8C-%D8%AD%D9%84%D9%82%D9%87-%D9%86%D8%A7%D9%85%D8%B2%D8%AF%DB%8C-%D9%88-%D8%A7%D8%B2%D8%AF%D9%88%D8%A7%D8%AC/";
    Height = "150";
    Width = "225";
    Count = "1x4";
    SiteID = "100";
    Element = "1";
}

void ShowBanner(list<ContentPackage> SelectedBanners, string SiteURL, string UserResolution, string Element, string Debugging, string Count)
{
	cout<<"Content-Type:text/html; charset=utf-8\n\n";
	string ReturnValue = MakeOutputJavascript(Element, SiteURL, SelectedBanners, UserResolution, Count);
	cout<<ReturnValue;
}

string MakeOutputJavascript(string ElementID, string SiteURL, list<ContentPackage> Banners, string UserResolution, string Count)
{
	string html1x4 = "<div id='js-native-8tad-content-ad' class='native-8tad-content-ad'>";
	html1x4 = html1x4 + "<style>" +
"        .ad-logo {" +
"            z-index: 10;" +
"			opacity: 0.9;" +
"			float: left;" +
"        }" +
"        .ad-logo:hover #ad-logo-co {" +
"            width: 35px;" +
"            padding: 0 3px 1px;" +
"            visibility: visible;" +
"            opacity: 1;" +
"			background-color: #fff;" +
"        }" +
"		.ad-logo:hover{" +
"		    opacity: 1;" +
"			background-color: #fff;" +
"		}" +
"		" +
"		.ad-logo img{" +
"		  width: 18px !important;" +
"		  height: 18px !imporatnt;" +
"		}" +
"        #icon {" +
"            float: right;" +
"            border: 0;" +
"            margin: 0;" +
"            padding: 0;" +
"        }" +
"        #ad-logo-co {" +
"            width: 0;" +
"            overflow: hidden;" +
"            float: right;" +
"            border-bottom: 0;" +
"            border-right: 0;" +
"            height: 18px;" +
"			line-height: 18px;" +
"            white-space: nowrap;" +
"            visibility: hidden;" +
"            opacity: 0;" +
"            -webkit-transition: .2s;" +
"            transition: .2s;" +
"			color: #324e6a;" +
"        }" +
"		.native-8tad-content-ad {" +
"            direction: rtl;" +
"            text-align: right;" +
"            border-radius: 0;" +
"            font-size: 12px;		" +
"			background: #fff;" +
"            border-top: 2px solid #a0a3a8;" +
"            padding: 1rem 1.25rem;" +
"            box-shadow: 0 1px 1px #b8bec9;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-heading {" +
"            margin-bottom: 5px;" +
"            border-radius: 0;" +
"            position: relative;" +
"			padding: 0;" +
"            background: transparent;" +
"            border-bottom: none;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-item a {" +
"            overflow: hidden;" +
"            font-weight: normal;" +
"			color: #606369;" +
"            font-size: 13px;" +
"            margin-bottom: 5px;" +
"        }" +
"		" +
"		.native-8tad-content-ad .native-8tad-ad-logo-label {" +
"            color: #606369;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-content .item-img {" +
"            -webkit-transform: scale(1);" +
"            -ms-transform: scale(1);" +
"            transform: scale(1);" +
"            -webkit-transition: transform 350ms ease;" +
"            -ms-transition: transform 350ms ease;" +
"            transition: transform 350ms ease;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-content:hover .native-8tad-ad-content-title {" +
"            color: #1e73be; " +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-img {" +
"            width: 32px;" +
"            vertical-align: middle;" +
"            margin-left: 10px;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-title {" +
"            float: right;" +
"			font-size: 1rem;" +
"            margin-bottom: 1em;" +
"            font-weight: 500;" +
"            color: #606369;" +
"            margin-top: 0;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-native-8tad {" +
"            float: left;" +
"            font-weight: bold;" +
"            direction: ltr;" +
"			margin-left: 5px;" +
"			height: 18px;" +
"			line-height: 18px;" +
"			font-size: 10px;" +
"            /*margin-top: 5px*/" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-native-8tad span, .native-8tad-content-ad .native-8tad-ad-native-8tad a {" +
"            vertical-align: middle;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-native-8tad span {" +
"            transition: opacity 200ms ease-in;" +
"            width: 80px;" +
"            text-align: left;" +
"        }" +
"        " +
"        .native-8tad-content-ad img {" +
"            width: 100%;" +
"        }" +
"        .native-8tad-content-ad a {" +
"            text-decoration: none;" +
"            color: #000;" +
"        }" +
"        .native-8tad-content-ad ul, .native-8tad-content-ad li {" +
"            margin: 0;" +
"            padding: 0;" +
"            list-style-type: none;" +
"        }" +
"        .native-8tad-content-ad li {" +
"            padding: 10px;" +
"            font-weight: bold;" +
"            font-size: 14px;" +
"        }" +
"        .native-8tad-content-ad li a {" +
"            display: block;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-clearfix:before, .native-8tad-content-ad .native-8tad-ad-clearfix:after {" +
"            content: ' ';" +
"            display: table;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-clearfix:after {" +
"            clear: both;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid {" +
"            display: block;" +
"            position: relative;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid, .native-8tad-content-ad .native-8tad-ad-block-grid * {" +
"            box-sizing: border-box;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid .bg-item {" +
"            float: right;" +
"            list-style: none;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid--slider {" +
"            margin-right: 0;" +
"            margin-left: 0;" +
"        }" +
"        .native-8tad-ad-with-col-1.native-8tad-ad-logo-label {" +
"            display: none;" +
"        }" +
"        .native-8tad-ad-with-col-1.native-8tad-ad-title {" +
"            font-size: 12px;" +
"        }" +
"        @media (min-width: 0px) {" +
"            .native-8tad-ad-xsmall-block-grid-1.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-1.is-not-center .bg-item:nth-of-type(1n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-1 .bg-item {" +
"                width: 100%;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-2.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-2.is-not-center .bg-item:nth-of-type(2n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-2 .bg-item {" +
"                width: 50%;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-3.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-3.is-not-center .bg-item:nth-of-type(3n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-3 .bg-item {" +
"                width: 33.33333%;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-4.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-4.is-not-center .bg-item:nth-of-type(4n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-4 .bg-item {" +
"                width: 25%;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-5.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-5.is-not-center .bg-item:nth-of-type(5n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-5 .bg-item {" +
"                width: 20%;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-6.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-6.is-not-center .bg-item:nth-of-type(6n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-xsmall-block-grid-6 .bg-item {" +
"                width: 16.66667%;" +
"            }" +
"        }" +
"        @media (min-width: 321px) {" +
"            .native-8tad-ad-small-block-grid-1.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-small-block-grid-1.is-not-center .bg-item:nth-of-type(1n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-small-block-grid-1 .bg-item {" +
"                width: 100%;" +
"            }" +
"            .native-8tad-ad-small-block-grid-2.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-small-block-grid-2.is-not-center .bg-item:nth-of-type(2n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-small-block-grid-2 .bg-item {" +
"                width: 50%;" +
"            }" +
"            .native-8tad-ad-small-block-grid-3.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-small-block-grid-3.is-not-center .bg-item:nth-of-type(3n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-small-block-grid-3 .bg-item {" +
"                width: 33.33333%;" +
"            }" +
"            .native-8tad-ad-small-block-grid-4.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-small-block-grid-4.is-not-center .bg-item:nth-of-type(4n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-small-block-grid-4 .bg-item {" +
"                width: 25%;" +
"            }" +
"            .native-8tad-ad-small-block-grid-5.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-small-block-grid-5.is-not-center .bg-item:nth-of-type(5n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-small-block-grid-5 .bg-item {" +
"                width: 20%;" +
"            }" +
"            .native-8tad-ad-small-block-grid-6.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-small-block-grid-6.is-not-center .bg-item:nth-of-type(6n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-small-block-grid-6 .bg-item {" +
"                width: 16.66667%;" +
"            }" +
"        }" +
"        @media (min-width: 480px) {" +
"            .native-8tad-ad-medium-block-grid-1.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-1.is-not-center .bg-item:nth-of-type(1n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-1 .bg-item {" +
"                width: 100%;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-2.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-2.is-not-center .bg-item:nth-of-type(2n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-2 .bg-item {" +
"                width: 50%;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-3.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-3.is-not-center .bg-item:nth-of-type(3n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-3 .bg-item {" +
"                width: 33.33333%;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-4.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-4.is-not-center .bg-item:nth-of-type(4n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-4 .bg-item {" +
"                width: 25%;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-5.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-5.is-not-center .bg-item:nth-of-type(5n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-5 .bg-item {" +
"                width: 20%;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-6.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-6.is-not-center .bg-item:nth-of-type(6n + 1) {" +
"                clear: both;" +
"            }" +
"            .native-8tad-ad-medium-block-grid-6 .bg-item {" +
"                width: 16.66667%;" +
"            }" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-item.card2 a {" +
"            float: right !important;;" +
"            width: 30% !important;" +
"            margin-left: 5%;" +
"        }" +
"        .native-8tad-content-ad .native-8tad-ad-item.card2 a.native-8tad-ad-content-title {" +
"            width: 60% !important;" +
"            float: right;" +
"        }" +
"        .bg-item native-8tad-ad-item card2 {" +
"            padding-bottom: 0 !important;" +
"        }" +
"        @media screen and (max-width: 992px) {" +
"            .native-8tad-content-ad .native-8tad-ad-item.card2 a {" +
"                width: 100%;" +
"            }" +
"            .card2 .native-8tad-ad-content-title {" +
"                width: 100% !important;" +
"                float: right;" +
"            }" +
"        }" +
"    </style>" +
"	" +
"    <div class='native-8tad-ad-heading native-8tad-ad-clearfix'>" +
"        <span class='native-8tad-ad-title '>مطالب پیشنهادی از سراسر وب</span>" +
"        " +
"		<div class='ad-logo'>" +
"			<a title='سامانه هوشمند تبلیغات آنلاین' href='http://8tad.ir/?utm_source=" + SiteURL + 
				"&amp;utm_campaign=nativeadsbutton&amp;utm_medium=nativeadsbutton' style=' border: 0; ' target='_blank'>" +
"			<div id='ad-logo-co'>هشتاد</div> " +
"			<img src='http://8tad.ir/static/frontend/images/8tad.png' id='icon' alt='adbutton' width='18' height='18'> " +
"			</a>" +
"		</div>" +
"		" +
"		<span class='native-8tad-ad-native-8tad'>" +
"          <span class='native-8tad-ad-logo-label '>پیشنهاد توسط</span>" +
"        </span>" +
"    </div>" +
"    <ul class='native-8tad-ad-clearfix native-8tad-ad-block-grid native-8tad-ad-xsmall-block-grid-1 native-8tad-ad-small-block-grid-2 native-8tad-ad-medium-block-grid-4 is-not-center'>";

	
	string html4x1 = "<div id='js-native-8tad-content-ad' class='native-8tad-content-ad'>";
	html4x1 = html4x1 + "    <style>" +
"        .ad-logo {" +
"            z-index: 10;" +
"			opacity: 0.9;" +
"			float: left;" +
"        }" +
"        .ad-logo:hover #ad-logo-co {" +
"            width: 35px;" +
"            padding: 0 3px 1px;" +
"            visibility: visible;" +
"            opacity: 1;" +
"			background-color: #fff;" +
"        }" +
"		.ad-logo:hover{" +
"		    opacity: 1;" +
"			background-color: #fff;" +
"		}" +
"		" +
"		.ad-logo img{" +
"		  width: 18px !important;" +
"		  height: 18px !imporatnt;" +
"		}" +
"        #icon {" +
"            float: right;" +
"            border: 0;" +
"            margin: 0;" +
"            padding: 0;" +
"        }" +
"        #ad-logo-co {" +
"            width: 0;" +
"            overflow: hidden;" +
"            float: right;" +
"            border-bottom: 0;" +
"            border-right: 0;" +
"            height: 18px;" +
"			line-height: 18px;" +
"            white-space: nowrap;" +
"            visibility: hidden;" +
"            opacity: 0;" +
"            -webkit-transition: .2s;" +
"            transition: .2s;" +
"			color: #324e6a;" +
"        }" +
"		.native-8tad-content-ad {" +
"            direction: rtl;" +
"            text-align: right;" +
"            border-radius: 0;" +
"            font-size: 12px;		" +
"			background: #fff;" +
"            border-top: 2px solid #a0a3a8;" +
"            padding: 1rem 1.25rem;" +
"            box-shadow: 0 1px 1px #b8bec9;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-heading {" +
"            margin-bottom: 5px;" +
"            border-radius: 0;" +
"            position: relative;" +
"			padding: 0;" +
"            background: transparent;" +
"            border-bottom: none;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-item a {" +
"            overflow: hidden;" +
"            font-weight: normal;" +
"			color: #606369;" +
"            font-size: 13px;" +
"            margin-bottom: 5px;" +
"        }" +
"		" +
"		.native-8tad-content-ad .native-8tad-ad-logo-label {" +
"            color: #606369;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-content .item-img {" +
"            -webkit-transform: scale(1);" +
"            -ms-transform: scale(1);" +
"            transform: scale(1);" +
"            -webkit-transition: transform 350ms ease;" +
"            -ms-transition: transform 350ms ease;" +
"            transition: transform 350ms ease;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-content:hover .native-8tad-ad-content-title {" +
"            color: #1e73be; " +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-img {" +
"            width: 32px;" +
"            vertical-align: middle;" +
"            margin-left: 10px;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-title {" +
"            float: right;" +
"			font-size: 1rem;" +
"            margin-bottom: 1em;" +
"            font-weight: 500;" +
"            color: #606369;" +
"            margin-top: 0;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-native-8tad {" +
"            float: left;" +
"            font-weight: bold;" +
"            direction: ltr;" +
"			margin-left: 5px;" +
"			height: 18px;" +
"			line-height: 18px;" +
"			font-size: 10px;" +
"            /*margin-top: 5px*/" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-native-8tad span, .native-8tad-content-ad .native-8tad-ad-native-8tad a {" +
"            vertical-align: middle;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-native-8tad span {" +
"            transition: opacity 200ms ease-in;" +
"            width: 80px;" +
"            text-align: left;" +
"        }" +
"" +
"        " +
"        .native-8tad-content-ad img {" +
"            width: 100%;" +
"        }" +
"" +
"        .native-8tad-content-ad a {" +
"            text-decoration: none;" +
"            color: #000;" +
"        }" +
"" +
"        .native-8tad-content-ad ul, .native-8tad-content-ad li {" +
"            margin: 0;" +
"            padding: 0;" +
"            list-style-type: none;" +
"        }" +
"" +
"        .native-8tad-content-ad li {" +
"            padding: 10px;" +
"            font-weight: bold;" +
"            font-size: 14px;" +
"        }" +
"" +
"        .native-8tad-content-ad li a {" +
"            display: block;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-clearfix:before, .native-8tad-content-ad .native-8tad-ad-clearfix:after {" +
"            content: ' ';" +
"            display: table;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-clearfix:after {" +
"            clear: both;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid {" +
"            display: block;" +
"            position: relative;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid, .native-8tad-content-ad .native-8tad-ad-block-grid * {" +
"            box-sizing: border-box;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid .bg-item {" +
"            float: right;" +
"            list-style: none;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-block-grid--slider {" +
"            margin-right: 0;" +
"            margin-left: 0;" +
"        }" +
"" +
"        .native-8tad-ad-with-col-1.native-8tad-ad-logo-label {" +
"            display: none;" +
"        }" +
"" +
"        .native-8tad-ad-with-col-1.native-8tad-ad-title {" +
"            font-size: 12px;" +
"        }" +
"" +
"        @media (min-width: 0px) {" +
"            .native-8tad-ad-xsmall-block-grid-1.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-1.is-not-center .bg-item:nth-of-type(1n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-1 .bg-item {" +
"                width: 100%;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-2.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-2.is-not-center .bg-item:nth-of-type(2n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-2 .bg-item {" +
"                width: 50%;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-3.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-3.is-not-center .bg-item:nth-of-type(3n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-3 .bg-item {" +
"                width: 33.33333%;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-4.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-4.is-not-center .bg-item:nth-of-type(4n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-4 .bg-item {" +
"                width: 25%;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-5.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-5.is-not-center .bg-item:nth-of-type(5n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-5 .bg-item {" +
"                width: 20%;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-6.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-6.is-not-center .bg-item:nth-of-type(6n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-xsmall-block-grid-6 .bg-item {" +
"                width: 16.66667%;" +
"            }" +
"        }" +
"" +
"        @media (min-width: 321px) {" +
"            .native-8tad-ad-small-block-grid-1.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-1.is-not-center .bg-item:nth-of-type(1n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-1 .bg-item {" +
"                width: 100%;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-2.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-2.is-not-center .bg-item:nth-of-type(2n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-2 .bg-item {" +
"                width: 50%;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-3.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-3.is-not-center .bg-item:nth-of-type(3n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-3 .bg-item {" +
"                width: 33.33333%;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-4.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-4.is-not-center .bg-item:nth-of-type(4n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-4 .bg-item {" +
"                width: 25%;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-5.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-5.is-not-center .bg-item:nth-of-type(5n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-5 .bg-item {" +
"                width: 20%;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-6.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-6.is-not-center .bg-item:nth-of-type(6n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-small-block-grid-6 .bg-item {" +
"                width: 16.66667%;" +
"            }" +
"        }" +
"" +
"        @media (min-width: 480px) {" +
"            .native-8tad-ad-medium-block-grid-1.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-1.is-not-center .bg-item:nth-of-type(1n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-1 .bg-item {" +
"                width: 100%;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-2.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-2.is-not-center .bg-item:nth-of-type(2n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-2 .bg-item {" +
"                width: 50%;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-3.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-3.is-not-center .bg-item:nth-of-type(3n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-3 .bg-item {" +
"                width: 33.33333%;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-4.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-4.is-not-center .bg-item:nth-of-type(4n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-4 .bg-item {" +
"                width: 25%;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-5.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-5.is-not-center .bg-item:nth-of-type(5n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-5 .bg-item {" +
"                width: 20%;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-6.is-not-center .bg-item:nth-of-type(1n) {" +
"                clear: none;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-6.is-not-center .bg-item:nth-of-type(6n + 1) {" +
"                clear: both;" +
"            }" +
"" +
"            .native-8tad-ad-medium-block-grid-6 .bg-item {" +
"                width: 16.66667%;" +
"            }" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-item.card2 a {" +
"            float: right !important;;" +
"            width: 30% !important;" +
"            margin-left: 5%;" +
"        }" +
"" +
"        .native-8tad-content-ad .native-8tad-ad-item.card2 a.native-8tad-ad-content-title {" +
"            width: 60% !important;" +
"            float: right;" +
"        }" +
"" +
"        .bg-item native-8tad-ad-item card2 {" +
"            padding-bottom: 0 !important;" +
"        }" +
"" +
"        @media screen and (max-width: 992px) {" +
"            .native-8tad-content-ad .native-8tad-ad-item.card2 a {" +
"                width: 100%;" +
"            }" +
"" +
"            .card2 .native-8tad-ad-content-title {" +
"                width: 100% !important;" +
"                float: right;" +
"            }" +
"        }" +
"    </style>" +
"    <div class='native-8tad-ad-heading native-8tad-ad-clearfix'>" +
"        <span class='native-8tad-ad-title '>مطالب پیشنهادی از سراسر وب</span>" +
"        " +
"		<div class='ad-logo'>" +
"			<a title='سامانه هوشمند تبلیغات آنلاین' href='http://8tad.ir/?utm_source=" + SiteURL +
				"&amp;utm_campaign=nativeadsbutton&amp;utm_medium=nativeadsbutton' style=' border: 0; ' target='_blank'>" +
"			<div id='ad-logo-co'>هشتاد</div> " +
"			<img src='http://8tad.ir/static/frontend/images/8tad.png' id='icon' alt='adbutton' width='18' height='18'> " +
"			</a>" +
"		</div>" +
"		" +
"		<span class='native-8tad-ad-native-8tad'>" +
"          <span class='native-8tad-ad-logo-label '>پیشنهاد توسط</span>" +
"        </span>" +
"" +
"    </div>" +
"    <ul class='native-8tad-ad-clearfix native-8tad-ad-block-grid native-8tad-ad-xsmall-block-grid-1 native-8tad-ad-small-block-grid-2 native-8tad-ad-medium-block-grid-1 is-not-center'>";

	
	AdEngine engine(DatabaseIP);
	for (ContentPackage elem : Banners) {
		string RedisURL = engine.ConvertURLtoRedisFormat(SiteURL);
		string Data = RedisURL + "_" + elem.Height + "_" + elem.Width + "_" + UserResolution + "_" + elem.BannerID + "_" + engine.ConvertURLtoRedisFormat(elem.BannerWebSite);
		hash<string> hs;
		elem.HashedData = to_string(hs(Data));
		string clickInterface = "http://click.8tad.ir/click/cwp.sh?h=" + elem.HashedData;
		engine.RedisSet("hashedData_" + elem.HashedData, Data);
		
		html1x4 = html1x4 +
			"<li class='bg-item native-8tad-ad-item'> " +
			"<div class='native-8tad-ad-content'> " +
			"<a href='" + clickInterface + "'" +
			"target='_blank' rel='nofollow'><img class='item-img' alt='" + elem.Title + "' src='http://8tad.ir/static/uploads/" + elem.BannerFile + "'></a> " +
			"<a href='" + clickInterface + "'" +
			"class='nativ-e-8tad-ad-content-title' target='_blank' rel='nofollow'>" + elem.Title + "</a> " +
			"</div> " +
			"</li>";
		
		html4x1 = html4x1 +
			"<li class='bg-item native-8tad-ad-item'> " +
			"<div class='native-8tad-ad-content'> " +
			"<a href='" + clickInterface + "'" +
			"target='_blank' rel='nofollow'><img class='item-img' alt='" + elem.Title + "' src='http://8tad.ir/static/uploads/" + elem.BannerFile + "'></a> " +
			"<a href='" + clickInterface + "'" +
			"class='nativ-e-8tad-ad-content-title' target='_blank' rel='nofollow'>" + elem.Title + "</a> " +
			"</div> " +
			"</li>";
	}
	
	html1x4 = html1x4 + "</ul>" +
		"</div>";
	
	html4x1 = html4x1 + "    </ul>" +
		"</div>";
	
	string correctHTML = ((Count == "4x1") ? html4x1 : html1x4);
	
	
	string Result = "(function () {";
	Result = Result +
		"html =\"" + correctHTML + "\";" +
		"document.getElementById('" + ElementID + "').innerHTML = (html);" +
		"})();";
	
	return Result;
}

string GetAdCoreCookie(cgicc::CgiEnvironment CE)
{
	vector<HTTPCookie> allCookies = CE.getCookieList();
	int l = allCookies.size();
	for(int i = 0; i < l; i++)
	{
		HTTPCookie co = allCookies.back();
		allCookies.pop_back();
		if(co.getName() == "adcore")
		{
			return co.getValue();
		}
	}
	return "";
}