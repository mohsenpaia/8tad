/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   AdEngine.cpp
 * Author: rera
 * 
 * Created on February 28, 2017, 6:00 AM
 */

#include "AdEngine.hpp"

ElapsedTime AdEngine::runTime;

AdEngine::AdEngine()
{
	RedisServerIPs[0] = "127.0.0.1";
	RedisServerIPs[1] = "127.0.0.1";
	ElasticIPPorts[0] = "http://127.0.0.1:9200/";
	ElasticIPPorts[1] = "http://192.168.0.113:9200/";
	ElasticIPPorts[2] = "http://192.168.0.131:9200/";
//	RedisServerIPs[0] = "192.168.156.22";
//	RedisServerIPs[1] = "192.168.156.24";
//	ElasticIPPorts[0] = "http://127.0.0.1:9200/";
//	ElasticIPPorts[1] = "http://192.168.156.22:9200/";
//	ElasticIPPorts[2] = "http://192.168.156.24:9200/";
	RedisPort = 6379;
	cWrite = redisConnectWithTimeout(RedisServerIPs[0].c_str(), RedisPort, timeout);
	cRead = redisConnectWithTimeout("127.0.0.1", RedisPort, timeout);
	InitializeVariables();
}

AdEngine::AdEngine(string Mode)
{
	if(Mode == "vm")
	{
		RedisServerIPs[0] = "127.0.0.1";
		RedisServerIPs[1] = "127.0.0.1";
		ElasticIPPorts[0] = "http://127.0.0.1:9200/";
		ElasticIPPorts[1] = "http://192.168.0.113:9200/";
		ElasticIPPorts[2] = "http://192.168.0.131:9200/";
	}
	else
	{
		RedisServerIPs[0] = "127.0.0.1";
		RedisServerIPs[1] = "127.0.0.1";
		ElasticIPPorts[0] = "http://192.168.156.42:9200/";
		ElasticIPPorts[1] = "http://192.168.156.42:9200/";
		ElasticIPPorts[2] = "http://127.0.0.1:9200/";
	}
	RedisPort = 6379;
	cWrite = redisConnectWithTimeout(RedisServerIPs[0].c_str(), RedisPort, timeout);
	cRead = redisConnectWithTimeout("127.0.0.1", RedisPort, timeout);
	InitializeVariables();
}

AdEngine::AdEngine(string RMIP, string RSIP, int RPort, string EMainIPPort, string ESecondIPPort)
{
	RedisServerIPs[0] = EMainIPPort;
	RedisServerIPs[1] = ESecondIPPort;
	ElasticIPPorts[0] = RMIP;
	ElasticIPPorts[1] = RSIP;
	RedisPort = RPort;
	cWrite = redisConnectWithTimeout(RedisServerIPs[0].c_str(), RedisPort, timeout);
	cRead = redisConnectWithTimeout("127.0.0.1", RedisPort, timeout);
	InitializeVariables();
}

AdEngine::AdEngine(ElapsedTime &runTime1)
{
	clock_t t = clock();
	
	RedisServerIPs[0] = "127.0.0.1";
	RedisServerIPs[1] = "127.0.0.1";
	ElasticIPPorts[0] = "http://127.0.0.1:9200/";
	ElasticIPPorts[1] = "http://192.168.0.113:9200/";
	ElasticIPPorts[2] = "http://192.168.0.131:9200/";
//	RedisServerIPs[0] = "192.168.156.22";
//	RedisServerIPs[1] = "192.168.156.24";
//	ElasticIPPorts[0] = "http://127.0.0.1:9200/";
//	ElasticIPPorts[1] = "http://192.168.156.22:9200/";
//	ElasticIPPorts[2] = "http://192.168.156.24:9200/";
	RedisPort = 6379;
	cWrite = redisConnectWithTimeout(RedisServerIPs[0].c_str(), RedisPort, timeout);
	cRead = redisConnectWithTimeout("127.0.0.1", RedisPort, timeout);
	InitializeVariables();
	
	t = clock() - t;
	runTime.Initialization += ((double)t/CLOCKS_PER_SEC);
}

//In order to communicate with UI, some prefixes for redis has been defined.
void AdEngine::InitializeVariables()
{
	//Shared
	BannerSite = "campaign_landing_page_url_";
	ClickCost = "campaign_click_price_";
	BannerCoef = "campaign_coef_";
	CampaignTotalBudget = "campaign_total_budget_";
	CampaignVariableDailyBudget = "campaign_variable_daily_budget_";
	CampaignConstantDailyBudget = "campaign_daily_budget_";
	LocationPrefix = "campaign_targeted_geography_";
	OSPrefix = "campaign_targeted_operating_system_";
	BannerSizePrefix = "campaign_banner_size_";
	Time0to8 = "campaign_playtime_00_08";
	Time8to4 = "campaign_playtime_08_16";
	Time4to0 = "campaign_playtime_16_24";
	CampaignBlockList = "campaigns_blocked_website_";
	PublisherBlockList = "publisher_blocked_website_";
	WebsiteBlockList = "website_blocked_campaigns_";
	Campaignstr = "campaign_";
	Bannerstr = "_banner_";
	HTMLstr = "_html_";
	CampaignsForKeywordPrefix = "campaign_targeted_keyword_";
	KeywordsForCampaignPrefix = "campaign_targeted_keywords_";
	WebsiteToID = "publishers_website_";
	RegisteredWebsitesAdWords = "publishers_website_search_engine";
	RegisteredWebsitesAdSense = "publishers_website_banner";
	PublisherSubjectPrefix = "publisher_website_subject_";
	CampaignSubjectPrefix = "campaign_targeted_subject_";
	SiteClassPrefix = "publisher_website_grade_";
	CampaignClassPrefix = "campaign_network_";
	AdSenseDefaultBanner = "campaign_default_adsense";
	AdWordsDefaultBanner = "campaign_default_adwords";
	AllAdWordsCampaigns = "campaign_adwords_list";
	AllContentCampaigns = "campaign_content_list";
	ShowAdSenseLog = "showAdSenseLog";
	ClickAdSenseLog = "clickAdSenseLog";
	ShowAdWordsLog = "showAdWordsLog";
	ClickAdWordsLog = "clickAdWordsLog";
	DeactivatedBanners = "campaign_deactivate";
	PublisherTotalBenefit = "publisher_website_total_benefit_";
	PublisherBenefitPercentage = "publisher_website_percentage_";
	PublisherAllURLsBenfit = "publisher_total_benefit_";
	LandingPageToCampaign = "campaign_landing_page_campaign_";
	CampaignRetargetting = "campaign_retargeting";
	CampaignType = "campaign_type_";
	CampaignCTR = "campaign_ctr_";
	minCTR = "campaign_minimum_ctr";
	maxCTR = "campaign_maximum_ctr";
	minBudget = "campaign_minimum_budget";
	maxBudget = "campaign_maximum_budget";
	minCampCoef = "campaign_minimum_coef";
	maxCampCoef = "campaign_maximum_coef";
	minCost = "campaign_minimum_cost";
	maxCost = "campaign_maximum_cost";
	
	//Engine Variables
	PendingWebsites = "pendingURLs";
	PendingWebsitesLists = "pendingURLsLists";
	ElasticWebPageContentCount = "elasticWebPageContentCount";
	ElasticShowAdSenseLogCount = "elasticShowAdSenseLogCount";
	ElasticShowAdWordsLogCount = "elasticShowAdWordsLogCount";
	ElasticClickAdSenseLogCount = "elasticClickAdSenseLogCount";
	ElasticClickAdWordsLogCount = "elasticClickAdWordsLogCount";
	ShowAdSenseLogCount = "showCountAdSenseLog";
	ClickAdSenseLogCount = "clickCountAdSenseLog";
	ShowAdWordsLogCount = "showCountAdWordsLog";
	ClickAdWordsLogCount = "clickCountAdWordsLog";
	CampaignPrefix = "campaignID";
	CampaignsForURL = "campaignsForURL_";
	ElasticLogIndex = "logs";
	ElasticShowAdSenseLogType = ShowAdSenseLog;
	ElasticClickAdSenseLogType = ClickAdSenseLog;
	ElasticShowAdWordsLogType = ShowAdWordsLog;
	ElasticClickAdWordsLogType = ClickAdWordsLog;
	ElasticWebpageIndex = "webpage";
	ElasticHTMLContentType = "HTMLContent";
	CrawledWebpages = "crawledWebpages";
	CollaborativePrefix = "collaborative_";
	
//	LoadIPNumbertoCityPairs();
	//LoadIP2LocationFromRedis();
	timespec ts;
	unsigned int seed = 0;
	clock_gettime(CLOCK_REALTIME, &ts);
	PendingListCount = 5;
	ElasticServerCount = 3;
	RedisServerCount = 2;
	seed += ts.tv_nsec;
	chrono::milliseconds ms = chrono::duration_cast< chrono::milliseconds >(chrono::system_clock::now().time_since_epoch());
	seed += ms.count();
//	int seed = static_cast<int>(time(0));
	srand(seed);
}

AdEngine::~AdEngine() {
	redisFree(cRead);
	redisFree(cWrite);
	IPNumbertoCityConverter = NULL;
	delete IPNumbertoCityConverter;
}

unsigned long int AdEngine::IPv4AddresstoIPNumber(string IPAddress)
{
    string w, x, y, z;
    int IPLength = IPAddress.length();
    int i = 0;
    while(i < IPLength && IPAddress[i] != '.'){
        w += IPAddress[i];
        i++;
    }
    i++;
    while(i < IPLength && IPAddress[i] != '.'){
        x += IPAddress[i];
        i++;
    }
    i++;
    while(i < IPLength && IPAddress[i] != '.'){
        y += IPAddress[i];
        i++;
    }
    i++;
    for (; i < IPLength; i++) {
        z += IPAddress[i];
    }
    int wi, xi, yi, zi;
    wi = xi = yi = zi = 0;
    
    try
    {
	wi = stoi(w, NULL, 10);
	xi = stoi(x, NULL, 10);
	yi = stoi(y, NULL, 10);
	zi = stoi(z, NULL, 10);
    }
    catch(std::exception &e)
    {
	    
    }
    
    unsigned long int Result = 0;
    Result = (16777216LL) * wi;
    Result += 65536*xi;
    Result += 256*yi;
    Result += zi;
    
    return Result;
}

string AdEngine::IPNumbertoIPv4Address(unsigned long int IPNumber)
{
    unsigned long int wi, xi, yi, zi;
    wi = int ( IPNumber / 16777216 ) % 256;
    xi = int ( IPNumber / 65536    ) % 256;
    yi = int ( IPNumber / 256      ) % 256;
    zi = IPNumber % 256;

    string w = to_string(wi);
    string x = to_string(xi);
    string y = to_string(yi);
    string z = to_string(zi);
    
    string Result = w + "." + x + "." + y + "." + z;
    
    return Result;
}

void AdEngine::LoadIP2LocationToRedis()
{
	string Line = "";
	ifstream pairFile("IP-Final.csv");
	int l = 1;
	while (getline(pairFile, Line)) {
		regex r(" ");
		list<string> sLine = strSplit(Line, ',');
		string minIP, maxIP, CountryCode, CountryName, Region, State;
		minIP = sLine.back();
		sLine.pop_back();
		maxIP = sLine.back();
		sLine.pop_back();
		CountryCode = sLine.back();
		sLine.pop_back();
		CountryName = sLine.back();
		sLine.pop_back();
		Region = sLine.back();
		sLine.pop_back();
		State = sLine.front();
		sLine.pop_front();
		State = State.erase(State.length() - 1, 1);
		State = regex_replace(State, r, "-");
//		string Command = "ZADD IP2Location " ;
////		Command += to_string(l) + " " + minIP + "_" + maxIP + "_" + CountryCode + "_" + CountryName + "_" + Region + "_" + State;
//		Command += to_string(l) + " " + minIP + "_" + State;
		l++;
//		redisCommand(c, Command.c_str());
		
		RedisSet("IPs_" + minIP, State);
	}
	
	LineCount = l;
	pairFile.close();
}

void AdEngine::LoadIP2LocationFromRedis()
{
	string Command = "EXISTS IP2Location";
	redisReply * res = (redisReply *)redisCommand(cRead, Command.c_str());
	if(res->integer == 0)
		LoadIP2LocationToRedis();
	Command = "ZRANGE IP2Location 0 -1";
	res = (redisReply *)redisCommand(cRead, Command.c_str());
	IPNumbertoCityConverter = new IP2LocationDT[res->elements];
	LineCount = res->elements;
	int size = res->elements;
	for(int i = 0; i < size; i++)
	{
		string Entry = res->element[i]->str;
		list<string> sLine = strSplit(Entry, '_');
		string minIP, maxIP="7", CountryCode="", CountryName="", Region = "", State;
		minIP = sLine.back();
		sLine.pop_back();
//		maxIP = sLine.back();
//		sLine.pop_back();
//		CountryCode = sLine.back();
//		sLine.pop_back();
//		CountryName = sLine.back();
//		sLine.pop_back();
//		//Region = sLine.back();
//		//sLine.pop_back();
		State = sLine.front();
		sLine.pop_front();

		
		IP2LocationDT newEntry;
		newEntry.minIP = stol(minIP);
		newEntry.maxIP = stol(maxIP);
		newEntry.Country_Code = CountryCode;
		newEntry.Country_Name = CountryName;
		newEntry.Region = Region;
		newEntry.State = State;
		IPNumbertoCityConverter[i] = newEntry;
		
	}
}

string AdEngine::GetIPLowerBound(unsigned long int theIP)
{
	string Result = "";
	unsigned long int IPNumber = theIP;
	int l = 0;
	int h = IPLowerBoundCount;
	while (l <= h) {
		unsigned long int lnum = IPLowerBounds[l];
		if(lnum == IPNumber)
		{
			Result = to_string(IPLowerBounds[l]);
			break;
		}
		int mid = (l + h) / 2;
		unsigned long int midNum = IPLowerBounds[mid];
		if(midNum < IPNumber)
		    l = mid + 1;
		else
		    h = mid - 1;
	}
	Result = to_string(IPLowerBounds[l - 1]);
	return Result;
}

string AdEngine::NewIP2Location(string IPAddress)
{
	unsigned long int IPNumber = IPv4AddresstoIPNumber(IPAddress);
	string LowerBound = GetIPLowerBound(IPNumber);
	string CommandParameter = "IPs_" + LowerBound;
	string City = RedisGet(CommandParameter);
	if(City == "")
	{
		LoadIP2LocationToRedis();
		LowerBound = GetIPLowerBound(IPNumber);
		City = RedisGet(CommandParameter);
	}
	if(City == "NotIran")
		City = "not_iran";
	if(City == "-")
		City = "not_iran";
	return City;
}

void AdEngine::LoadIPNumbertoCityPairs()
{
	LineCount = 0;
	string Line = "";
	
	std::ifstream f("IP-Final.csv");
	std::string line;
	for (; std::getline(f, line); ++LineCount);
	f.close();
	ifstream pairFile("IP-Final.csv");
	int l = 1;
	
	IPNumbertoCityConverter = new IP2LocationDT[LineCount];
	
	while (getline(pairFile, Line)) {
		
		list<string> sLine = strSplit(Line, ',');
		string minIP, maxIP, CountryCode, CountryName, Region, State;
		minIP = sLine.back();
		sLine.pop_back();
		maxIP = sLine.back();
		sLine.pop_back();
		CountryCode = sLine.back();
		sLine.pop_back();
		CountryName = sLine.back();
		sLine.pop_back();
		Region = sLine.back();
		sLine.pop_back();
		State = sLine.front();
		sLine.pop_front();
		State = State.erase(State.length() - 1, 1);

		IP2LocationDT newEntry;
		newEntry.minIP = stol(minIP);
		newEntry.maxIP = stol(maxIP);
		newEntry.Country_Code = CountryCode;
		newEntry.Country_Name = CountryName;
		newEntry.Region = Region;
		newEntry.State = State;
		IPNumbertoCityConverter[l] = newEntry;
		l++;
	}
}

double AdEngine::ValueNormalizer(double value, double min, double max, double bound)
{
	double Result = (value - min) / (max - min);
	Result = (Result * (bound - 1)) + 1;
	return Result;
}


list<string> AdEngine::strSplit(string s, char schar)
{
	list<string> Result;
	string tmp = "";
	int l = 0;
	while (l < s.length()) {
	    if(s[l] == schar)
	    {
		Result.push_front(tmp);
		tmp = "";
	    }
	    else
	    {
		tmp += s[l];
	    }
	    l++;
	}
	Result.push_front(tmp);
	return Result;
}

string AdEngine::IP2Location(string IPAddress)
{
	string Result = "";
	unsigned long int IPNumber = IPv4AddresstoIPNumber(IPAddress);
	int l = 1;
	int h = LineCount;
	while (l <= h) {
		unsigned long int lnum = IPNumbertoCityConverter[l].minIP;
		if(lnum == IPNumber)
		{
			Result = IPNumbertoCityConverter[l].State;
			break;
		}
		int mid = (l + h) / 2;
		unsigned long int midNum = IPNumbertoCityConverter[mid].minIP;
		if(midNum < IPNumber)
		    l = mid + 1;
		else
		    h = mid - 1;
	}
	if(IPNumbertoCityConverter[l - 1].State == "-")
		Result = "all";
	else
	{
		Result = IPNumbertoCityConverter[l - 1].State;
		regex r(" ");
		Result = regex_replace(Result, r, "-");
	}
	if(Result == "NotIran")
		Result = "not_iran";
	return Result;
}

AdwordsPackage AdEngine::GetAdwordsBanner(string BannerID)
{
	AdwordsPackage AP;
	AP.Title = RedisSmembersFirstOne(Campaignstr + BannerID + "_title");
	AP.Description = RedisSmembersFirstOne(Campaignstr + BannerID + "_description");
	AP.Email = RedisSmembersFirstOne(Campaignstr + BannerID + "_email");
	AP.Phone = RedisSmembersFirstOne(Campaignstr + BannerID + "_phone");
	AP.Address = RedisSmembersFirstOne(Campaignstr + BannerID + "_address");
	AP.Website = RedisSmembersFirstOne(BannerSite + BannerID);
	AP.BannerID = BannerID;
	return AP;
}

ContentPackage AdEngine::GetContentBanner(string BannerID, string size, int Width, int Height)
{
	ContentPackage CP;
	CP.Title = RedisSmembersFirstOne(Campaignstr + BannerID + "_native_title");
	string Query = Campaignstr + BannerID + Bannerstr + size;
	CP.BannerFile = RedisSmembersFirstOne(Query);
	CP.BannerWebSite = GetBannerSite(BannerID);
	CP.BannerID = BannerID;
	CP.Width = to_string(Width);
	CP.Height = to_string(Height);
	return CP;
}

list<AdwordsPackage> AdEngine::FindSuitableBannerAdWords(string IPAddress, string UserResolution, string UserOS, string SiteURL, string UserQuery,
	string &Debugging, string UserName, string Password, int Size, string &Error, string Cookies, string apiAddress)
{
	string HomeURL = ExtractRootURL(SiteURL);
	string RedisURL = ConvertURLtoRedisFormat(SiteURL);
	string DomainURL = GetRawURL(HomeURL);
	if(IsRegisteredWebsite(DomainURL, RegisteredWebsitesAdWords) == false)
	{
		list<AdwordsPackage> finalResult;
		Error = "{\"Error 143\" : \"Your Website is not a legal website. Please first register in http://8tad.ir/!\"}";
		//string defau = RedisSmembersFirstOne(AdWordsDefaultBanner);
//		AdwordsPackage AW = GetAdwordsBanner(defau);
		SaveAdWordsShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, "Illegal", UserQuery);
		//finalResult.push_front(AW);
//		finalResult.push_front(Ress);
		return finalResult;
	}

	//authentication
	string rightUser = RedisSmembersFirstOne("publisher_username_" + DomainURL);
	string rightPass = RedisSmembersFirstOne("publisher_password_" + DomainURL);
	if(UserName != rightUser || rightPass != Password)
	{
		list<AdwordsPackage> finalResult;
		Error = "{\"Error 678\" : \"The username and/or password for domain " + DomainURL + " is/are wrong!\"}";
		SaveAdWordsShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, "WrongPass", UserQuery);
		return finalResult;
	}
	

	Error = "";	

	//city filter
	string citySet = NewIP2Location(IPAddress);
	Debugging += "City: " + citySet + " ";
	citySet = LocationPrefix + citySet;

	//time filter
	string timeSet = ResolveTime();
	Debugging += "Time: " + timeSet + " ";

	//os filter
	string osSet = GetOS(UserOS);
	Debugging += "OS: " + osSet + " ";
	osSet = OSPrefix + osSet;
	
	//query
	list<string> allKeywordsSets = GetRootQuery(UserQuery, apiAddress);

	
	//subject filter
	string subjectSet = PublisherSubjectPrefix + DomainURL;
	redisReply *Subjects = RedisSmembers(subjectSet);
	int l = 0;
	if(Subjects != NULL && Subjects->elements > 0)
		l = Subjects->elements;
	subjectSet = "";
	Debugging += "Subjects: ";
	for(int i = 0; i < l; i++)
	{
		subjectSet += CampaignSubjectPrefix + string(Subjects->element[i]->str) + " ";
		Debugging += string(Subjects->element[i]->str) + " ";
	}
		
	//class filter
	string siteClass = RedisSmembersFirstOne(SiteClassPrefix + DomainURL);
	Debugging += "Grade of publisher: " + siteClass + " ";
	string classSet = CampaignClassPrefix + siteClass;
	
	int len = allKeywordsSets.size();
	
	list<redisReply *> Result;
	string RetargettingQuery = Retargetting(Cookies);
	for(list<string>::iterator it = allKeywordsSets.begin(); it != allKeywordsSets.end(); it++)
	{
		string Query = citySet + " " + timeSet + " " + osSet + " " + subjectSet + " " + AllAdWordsCampaigns + " " + classSet + " " + *it;
		redisReply *tmp = RedisSinter(RetargettingQuery + " " + Query);
		if(tmp == NULL || tmp->elements == 0)
			Result.push_back(RedisSinter(Query));
		else
			Result.push_back(tmp);
	}

	if(!IsFoundAnyAdwordsCampaign(Result))
	{
		list<AdwordsPackage> finalResult;
		string defau = RedisSmembersFirstOne(AdWordsDefaultBanner);
//		AdwordsPackage AW = GetAdwordsBanner(defau);
		SaveAdWordsShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, UserQuery);
//		finalResult.push_front(AW);
		return finalResult;	
	}
	
	
	//redisReply *Blocks = RedisSmembers(BlockList + SiteURL);
	redisReply *DeactivatedAndBlocks = RedisSunion(CampaignBlockList + DomainURL, DeactivatedBanners);
	list<string> allBanners = DifferencesofRepliesAdWordsModified(Result, DeactivatedAndBlocks, DomainURL);
	if(allBanners.size() == 0)
	{
		list<AdwordsPackage> finalResult;
		string defau = RedisSmembersFirstOne(AdWordsDefaultBanner);
//		AdwordsPackage AW = GetAdwordsBanner(defau);
		SaveAdWordsShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, UserQuery);
//		finalResult.push_front(AW);
		return finalResult;
	}
	
	
	list<string> Selected = RouletteWheelAdWords(allBanners, Size);
	int size = Selected.size();
	if(size > 1)
		Selected = SortAdWordsResults(Selected);
	//getting .jpg or .gif corresponding to banner
	list<AdwordsPackage> finalResult;
	for(int i = 0; i < size; i++)
	{
		string banner = Selected.front();
		Selected.pop_front();
		AdwordsPackage AW = GetAdwordsBanner(banner);
		SaveAdWordsShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, banner, UserQuery);
		finalResult.push_front(AW);
	}
	return finalResult;
}

bool AdEngine::IsFoundAnyAdwordsCampaign(list<redisReply *> ResultFiltering)
{
	for (list<redisReply *>::iterator it = ResultFiltering.begin(); it != ResultFiltering.end(); it++)
		if((*it)->elements > 0)
			return true;
	return false;
}


string AdEngine::FindSuitableBannerAdSense(string IPAddress, string UserResolution, string UserOS, string SiteURL, int BannerHeight, int BannerWidth, string &BannerFile, string &BannerWebSite, string &Debugging, string Cookies)
{
	clock_t t = clock();
	string HomeURL = ExtractRootURL(SiteURL);
	string RedisURL = ConvertURLtoRedisFormat(SiteURL);
	string DomainURL = GetRawURL(HomeURL);
	t = clock() - t;
	runTime.cleanURl += ((double)t/CLOCKS_PER_SEC);
	
	if(IsRegisteredWebsite(DomainURL, RegisteredWebsitesAdSense) == false)
	{
		string defau = RedisSmembersFirstOne(AdSenseDefaultBanner);
		BannerFile = RedisSmembersFirstOne(Campaignstr + defau + Bannerstr + to_string(BannerWidth) + "x" + to_string(BannerHeight));
		BannerWebSite = RedisSmembersFirstOne(BannerSite + defau);
		
		t = clock();
		SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, to_string(BannerWidth) + "x" + to_string(BannerHeight));
		t = clock() - t;
		runTime.saveLog += ((double)t/CLOCKS_PER_SEC);
		
		return defau;
	}
	
	//city filter
	t = clock();
	string citySet = NewIP2Location(IPAddress);
	Debugging = "City: " + citySet + "<br>";
	citySet = LocationPrefix + citySet;
	t = clock() - t;
	runTime.Ip2Location += ((double)t/CLOCKS_PER_SEC);

	//time filter
	t = clock();
	string timeSet = ResolveTime();
	Debugging += "Time: " + timeSet + "<br>";
	t = clock() - t;
	runTime.ResolveTime += ((double)t/CLOCKS_PER_SEC);

	//os filter
	t = clock();
	string osSet = GetOS(UserOS);
	Debugging += "OS: " + osSet + "<br>";
	osSet = OSPrefix + osSet;
	t = clock() - t;
	runTime.getOs += ((double)t/CLOCKS_PER_SEC);
	
	//subject filter
	t = clock();
	string subjectSet = PublisherSubjectPrefix + DomainURL;
	redisReply *Subjects = RedisSmembers(subjectSet);
	int l = 0;
	if(Subjects != NULL && Subjects->elements > 0)
		l = Subjects->elements;
	subjectSet = "";
	Debugging += "Subjects:<br>";
	for(int i = 0; i < l; i++)
	{
		subjectSet += CampaignSubjectPrefix + string(Subjects->element[i]->str) + " ";
		Debugging += string(Subjects->element[i]->str) + "<br>";
	}
	t = clock() - t;
	runTime.getSubjects += ((double)t/CLOCKS_PER_SEC);
	
	//size filter
	string size = to_string(BannerWidth) + "x" + to_string(BannerHeight);
	Debugging += "Size of iframe: " + size + "<br>";
	string sizeSet = BannerSizePrefix + size;

	//class filter
	string siteClass = RedisSmembersFirstOne(SiteClassPrefix + DomainURL);
	Debugging += "Grade of publisher: " + siteClass + "<br>";
	string classSet = CampaignClassPrefix + siteClass;
	
	//website content Filter
	t = clock();
	string keyUrl = CampaignsForURL + RedisURL;
	redisReply *tmpres = RedisSmembers(keyUrl);
	//RedisSadd(PendingWebsites, RedisURL);
	AddWebsiteToPendingWebsites(RedisURL);
	if(tmpres == NULL || tmpres->elements == 0)
		keyUrl = "";
	t = clock() - t;
	runTime.getKeys += ((double)t/CLOCKS_PER_SEC);
	
	string QueryKeyword = citySet + " " + timeSet + " " + osSet + " " + subjectSet + " " + sizeSet + " " + keyUrl + " " + classSet;
	RedisSet("query", QueryKeyword);
	redisReply * ResultFilteringKeywords = RedisSinter(QueryKeyword);
	redisReply *Result = NULL;
	
//	if(ResultFiltering == NULL || (int)ResultFiltering->elements == 0)
//	{
		string QueryNoKeywords = citySet + " " + timeSet + " " + osSet + " " + subjectSet + " " + sizeSet + " " + classSet;
		redisReply *ResultFilteringNoKeywords = RedisSinter(QueryNoKeywords);
//	}
	
	if(ResultFilteringNoKeywords == NULL || (int)ResultFilteringNoKeywords->elements == 0)
	{
		string defau = RedisSmembersFirstOne(AdSenseDefaultBanner);
		BannerFile = RedisSmembersFirstOne(Campaignstr + defau + Bannerstr + to_string(BannerWidth) + "x" + to_string(BannerHeight));
		BannerWebSite = RedisSmembersFirstOne(BannerSite + defau);
		t = clock();
		SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, size);
		t = clock() - t;
		runTime.saveLog += ((double)t/CLOCKS_PER_SEC);
		return defau;	
	}
	
	t = clock();
	string RetargettingQuery = Retargetting(Cookies);
	Result = RedisSinter(RetargettingQuery + " " + QueryKeyword);
	t = clock() - t;
	runTime.Retargeting += ((double)t/CLOCKS_PER_SEC);
	
	if(Result == NULL || Result->elements == 0)
		Result = ResultFilteringKeywords;

	//redisReply *Blocks = RedisSmembers(BlockList + SiteURL);
	t = clock();
	redisReply *DeactivatedAndBlocks = RedisSunion(CampaignBlockList + DomainURL, DeactivatedBanners + " " + WebsiteBlockList + DomainURL);
	list<string> allBanners = DifferencesofRepliesAdSense(Result, DeactivatedAndBlocks, RedisURL, DomainURL);
	list<string> allBannersNoKeywords = DifferencesofRepliesAdSenseNoKeywords(ResultFilteringNoKeywords, DeactivatedAndBlocks, RedisURL, DomainURL);
	t = clock() - t;
	runTime.diffofReply += ((double)t/CLOCKS_PER_SEC);
	t = clock();
	string Selected = RouletteWheelAdSense(allBanners, allBannersNoKeywords, RedisURL);
	t = clock() - t;
	runTime.RouletteTime += ((double)t/CLOCKS_PER_SEC);
	RedisSet("wptest", "Done");
	if(Selected == "")
	{
		string defau = RedisSmembersFirstOne(AdSenseDefaultBanner);
		BannerFile = RedisSmembersFirstOne(Campaignstr + defau + Bannerstr + to_string(BannerWidth) + "x" + to_string(BannerHeight));
		BannerWebSite = RedisSmembersFirstOne(BannerSite + defau);
		t = clock();
		SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, size);
		t = clock() - t;
		runTime.saveLog += ((double)t/CLOCKS_PER_SEC);
		return defau;
	}
	
	if(tmpres != NULL && tmpres->elements > 0)
	{
		Debugging += "Webpages Contains keywords: <br>";
		Debugging += "\t" + RedisGet("keyForURL_" + RedisURL + "_" + Selected) + "<br>";
	}
	
	//getting .jpg or .gif corresponding to banner
	string Query = "";
	Query = Campaignstr + Selected + Bannerstr + size;
	BannerFile = RedisSmembersFirstOne(Query);
	BannerWebSite = GetBannerSite(Selected);
	t = clock();
	SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, Selected, size);
	t = clock() - t;
	runTime.saveLog += ((double)t/CLOCKS_PER_SEC);
	return Selected;
}


list<ContentPackage> AdEngine::FindSuitableBannerContent(string IPAddress, string UserResolution, string UserOS, string SiteURL, int BannerHeight, int BannerWidth, string &Debugging, string Cookies, int Count)
{
	string HomeURL = ExtractRootURL(SiteURL);
	string RedisURL = ConvertURLtoRedisFormat(SiteURL);
	string DomainURL = GetRawURL(HomeURL);
	
	if(IsRegisteredWebsite(DomainURL, RegisteredWebsitesAdSense) == false)
	{
		string defau = "NoBanner";
		SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, to_string(BannerWidth) + "x" + to_string(BannerHeight));
		list<ContentPackage> tmp;
		return tmp;
	}
		

	string size = to_string(BannerWidth) + "x" + to_string(BannerHeight);
	Debugging += "Size of iframe: " + size + "<br>";
	string sizeSet = BannerSizePrefix + size;
	
	//city filter
	string citySet = NewIP2Location(IPAddress);
	Debugging += "City: " + citySet + " ";
	citySet = LocationPrefix + citySet;

	//time filter
	string timeSet = ResolveTime();
	Debugging += "Time: " + timeSet + " ";

	//os filter
	string osSet = GetOS(UserOS);
	Debugging += "OS: " + osSet + " ";
	osSet = OSPrefix + osSet;
	
	
	//subject filter
	string subjectSet = PublisherSubjectPrefix + DomainURL;
	redisReply *Subjects = RedisSmembers(subjectSet);
	int l = 0;
	if(Subjects != NULL && Subjects->elements > 0)
		l = Subjects->elements;
	subjectSet = "";
	Debugging += "Subjects: ";
	for(int i = 0; i < l; i++)
	{
		subjectSet += CampaignSubjectPrefix + string(Subjects->element[i]->str) + " ";
		Debugging += string(Subjects->element[i]->str) + " ";
	}
	
	//website content Filter
	string keyUrl = CampaignsForURL + RedisURL;
	redisReply *tmpres = RedisSmembers(keyUrl);
	//RedisSadd(PendingWebsites, RedisURL);
	AddWebsiteToPendingWebsites(RedisURL);
	if(tmpres == NULL || tmpres->elements == 0)
		keyUrl = "";
		
	//class filter
	string siteClass = RedisSmembersFirstOne(SiteClassPrefix + DomainURL);
	Debugging += "Grade of publisher: " + siteClass + " ";
	string classSet = CampaignClassPrefix + siteClass;
	
	string Query = citySet + " " + timeSet + " " + osSet + " " + subjectSet + " " + classSet + " " + keyUrl + " " + AllContentCampaigns;
	RedisSet("query", Query);
	redisReply * ResultFiltering = RedisSinter(Query);

	if(ResultFiltering == NULL || (int)ResultFiltering->elements == 0)
	{
		Query = citySet + " " + timeSet + " " + osSet + " " + subjectSet + " " + sizeSet + " " + classSet + " " + AllContentCampaigns;
		ResultFiltering = RedisSinter(Query);
	}
	
	if(ResultFiltering == NULL || (int)ResultFiltering->elements == 0)
	{
		string defau = "NoBanner";
		SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, size);
		list<ContentPackage> tmp;
		return tmp;	
	}

	
	string RetargettingQuery = Retargetting(Cookies);
	redisReply *Result = RedisSinter(RetargettingQuery + " " + Query);
	
	if(Result == NULL || Result->elements == 0)
		Result = ResultFiltering;
	
	//redisReply *Blocks = RedisSmembers(BlockList + SiteURL);
	redisReply *DeactivatedAndBlocks = RedisSunion(CampaignBlockList + DomainURL, DeactivatedBanners);
	list<string> allBanners = DifferencesofRepliesAdWords(ResultFiltering, DeactivatedAndBlocks, DomainURL);
	if(allBanners.size() == 0)
	{
		list<ContentPackage> finalResult;
		string defau = "NoBanner";
//		AdwordsPackage AW = GetAdwordsBanner(defau);
		SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, defau, size);
//		finalResult.push_front(AW);
		return finalResult;
	}
	
	
	list<string> Selected = RouletteWheelAdWords(allBanners, Count);
	int count = Selected.size();
	//getting .jpg or .gif corresponding to banner
	list<ContentPackage> finalResult;
	for(int i = 0; i < count; i++)
	{
		string banner = Selected.front();
		Selected.pop_front();
		ContentPackage AW = GetContentBanner(banner, size, BannerWidth, BannerHeight);
		SaveAdSenseShowLogtoRedis(IPAddress, UserResolution, UserOS, RedisURL, banner, size);
		finalResult.push_front(AW);
	}
	return finalResult;
}


void AdEngine::AddWebsiteToPendingWebsites(string newURL)
{
	bool isProcessing = RedisSismember(PendingWebsites, newURL);
	if(isProcessing == false)
	{
		int minLength = INT_MAX;
		int Selected = 1;
		for (int i = 0; i < PendingListCount; i++) {
			int tmp = RedisScard(PendingWebsitesLists + to_string(i + 1));
			if(tmp < minLength)
			{
				minLength = tmp;
				Selected = i + 1;
			}
		}
		RedisSadd(PendingWebsitesLists + to_string(Selected), newURL);
		RedisSadd(PendingWebsites, newURL);
	}
}

string AdEngine::RouletteWheelAdSense(list<string> allBanners, list<string> allBannersNoKeywords, string RedisURL)
{
	//list<string> allBanners = RedisReplytoList(reply);
	int k1 = allBanners.size() ;
	int k2 = allBannersNoKeywords.size();
	int k = k1 + k2;
	
	if(k == 0)
		return "";
	string strAllBanners[k];
	double value[k];
	int sum = 0;
	int index = 0;
	for(int i = 0; i < k1; i++)
	{
		string tmp = allBanners.back();
		strAllBanners[index] = tmp;
		allBanners.pop_back();
		string Key = ClickCost + tmp;
		tmp = RedisSmembersFirstOne(Key);
		if(tmp != "")
			value[index] = 2 * stod(tmp);
		else
			value[index] = 0;
		sum += value[index];
		index++;
	}
	for(int i = 0; i < k2; i++)
	{
		string tmp = allBannersNoKeywords.back();
		
		////////////////////////////
		double intCoef = 1, intCost = 1, intCTR = 1, intBudget = 1;
		string Coef = RedisSmembersFirstOne(BannerCoef + tmp);
		string strMinCoef = RedisSmembersFirstOne(minCampCoef);
		string strMaxCoef = RedisSmembersFirstOne(maxCampCoef);
		if(Coef != "" && strMaxCoef != "" && strMinCoef != "")
			intCoef = ValueNormalizer(stod(Coef), stod(strMinCoef), stod(strMaxCoef), 20);
		if(intCoef == INFINITY)
			intCoef = 1;
		string Cost = RedisSmembersFirstOne(ClickCost + tmp);
		string strMinCost = RedisSmembersFirstOne(minCost);
		string strMaxCost = RedisSmembersFirstOne(maxCost);
		if(Cost != "" && strMaxCost != "" && strMinCost != "")
			intCost = ValueNormalizer(stod(Cost), stod(strMinCost), stod(strMaxCost), 10);
		if(intCost == INFINITY)
			intCost = 1;
		string CTR = RedisSmembersFirstOne(CampaignCTR + tmp);
		string strMinCTR = RedisSmembersFirstOne(minCTR);
		string strMaxCTR = RedisSmembersFirstOne(maxCTR);
		if(CTR != "" && strMaxCTR != "" && strMinCTR != "")
			intCTR = ValueNormalizer(stod(CTR), stod(strMinCTR), stod(strMaxCTR), 10);
		if(intCTR == INFINITY)
			intCTR = 1;
		string Budget = RedisSmembersFirstOne(CampaignVariableDailyBudget + tmp);
		string strMinBudget = RedisSmembersFirstOne(minBudget);
		string strMaxBudget = RedisSmembersFirstOne(maxBudget);
		if(Budget != "" && strMaxBudget != "" && strMinBudget != "")
			intBudget = ValueNormalizer(stod(Budget), stod(strMinBudget), stod(strMaxBudget), 10);
		if(intBudget == INFINITY)
			intBudget = 1;
		////////////////////////////
		
		strAllBanners[index] = tmp;
		allBannersNoKeywords.pop_back();
//		string Key = ClickCost + tmp;
//		tmp = RedisSmembersFirstOne(Key);
//		if(tmp != "")
//			value[index] = stod(tmp);
//		else
//			value[index] = 0;
		
		value[index] = (intCoef * intCost * intCTR * intBudget);
		sum += value[index];
		index++;
	}
	double s = rand() % sum;
	int curr = 0;
	string Selected = "";
	for(int i = 0; i < k; i++)
	{
		if(s >= curr && s < curr + value[i])
		{
			redisReply *tr = RedisSmembers(KeywordsForCampaignPrefix + strAllBanners[i]);
			if(tr == NULL || tr->elements == 0)
				Selected = strAllBanners[i];
			if((tr != NULL && tr->elements > 0) && RedisSismember(CampaignsForURL + RedisURL, strAllBanners[i]) == true)
				Selected = strAllBanners[i];
		}
		curr += value[i];
	}
	return Selected;
}

list<string> AdEngine::RouletteWheelAdWords(list<string> allBanners, int size)
{
	//list<string> allBanners = RedisReplytoList(reply);
	int k = allBanners.size();
	if(k < size)
		return allBanners;
	string strAllBanners[k];
	double value[k];
	int sum = 0;
	for(int i = 0; i < k; i++)
	{
		string tmp = allBanners.back();
		strAllBanners[i] = tmp;
		allBanners.pop_back();
		string Key = ClickCost + tmp;
		tmp = RedisSmembersFirstOne(Key);
		if(tmp != "")
			value[i] = stod(tmp);
		else
			value[i] = 0;
		sum += value[i];
	}
	
	list<string> Selected;
	bool isSel[k] {false};
	for(int j = 0; j < size; j++)
	{
		int s = rand() % sum;
		int curr = 0;
		for(int i = 0; i < k; i++)
		{
			if(isSel[i] == false)
			{
				if(s >= curr && s < curr + value[i])
				{
					Selected.push_front(strAllBanners[i]);
					isSel[i] = true;
				}
			}
			else if(isSel[i] == true && s >= curr && s < curr + value[i])
				j--;
			curr += value[i];
		}
	}
	return Selected;
}

list<string> AdEngine::SortAdWordsResults(list<string> Entry)
{
	int size = Entry.size();
	string camp[size];
	double coefCost[size];
	for(int i = 0; i < size; i++)
	{
		string tmp = Entry.front();
		Entry.pop_front();
		double intCoef = 1, intCost = 1, intCTR = 1, intBudget = 1;
		string Coef = RedisSmembersFirstOne(BannerCoef + tmp);
		string strMinCoef = RedisSmembersFirstOne(minCampCoef);
		string strMaxCoef = RedisSmembersFirstOne(maxCampCoef);
		if(Coef != "" && strMaxCoef != "" && strMinCoef != "")
			intCoef = ValueNormalizer(stod(Coef), stod(strMinCoef), stod(strMaxCoef), 20);
		string Cost = RedisSmembersFirstOne(ClickCost + tmp);
		string strMinCost = RedisSmembersFirstOne(minCost);
		string strMaxCost = RedisSmembersFirstOne(maxCost);
		if(Cost != "" && strMaxCost != "" && strMinCost != "")
			intCost = ValueNormalizer(stod(Cost), stod(strMinCost), stod(strMaxCost), 10);
		string CTR = RedisSmembersFirstOne(CampaignCTR + tmp);
		string strMinCTR = RedisSmembersFirstOne(minCTR);
		string strMaxCTR = RedisSmembersFirstOne(maxCTR);
		if(CTR != "" && strMaxCTR != "" && strMinCTR != "")
			intCTR = ValueNormalizer(stod(CTR), stod(strMinCTR), stod(strMaxCTR), 10);
		string Budget = RedisSmembersFirstOne(CampaignVariableDailyBudget + tmp);
		string strMinBudget = RedisSmembersFirstOne(minBudget);
		string strMaxBudget = RedisSmembersFirstOne(maxBudget);
		if(Budget != "" && strMaxBudget != "" && strMinBudget != "")
			intBudget = ValueNormalizer(stod(Budget), stod(strMinBudget), stod(strMaxBudget), 10);
		coefCost[i] = intCoef * intCost * intCTR * intBudget;
		camp[i] = tmp;
	}
	for(int i = 0; i < size; i++)
	{
		double max = coefCost[i];
		int maxI = i;
		for(int j = i + 1; j < size; j++)
		{
			if(coefCost[j] > max)
			{
				max = coefCost[j];
				maxI = j;
			}
		}
		string tmp = camp[i];
		camp[i] = camp[maxI];
		camp[maxI] = tmp;
		double tmp1 = coefCost[i];
		coefCost[i] = max;
		coefCost[maxI] = tmp1;
	}
	list<string> Result;
	for(int i = 0; i < size; i++)
		Result.push_back(camp[i]);
	return Result;
}


string AdEngine::Retargetting(string Cookies)
{
	if(Cookies == "")
		return "";
	list<string> allCookies = strSplit(Cookies, '_');
	int l = allCookies.size();
//	redisReply *allCampaigns = RedisKeys(BannerSite + "*");
	RedisDel("temporaryRetargetting");
	for(int i = 0; i < l; i++)
	{
		string cook = allCookies.back();
		allCookies.pop_back();
		cook = ExtractRootURL(cook);
		cook = GetRawURL(cook);
		redisReply *allCampaigns = RedisKeys(LandingPageToCampaign + cook.substr(0, cook.length() - 1) + "*");
		string Res = "";
		redisReply *allRet = NULL;
		if(allCampaigns != NULL && allCampaigns->elements > 0)
			allRet = RedisSinter(string(allCampaigns->element[0]->str) + " " + CampaignRetargetting);
		if(allRet != NULL && allRet->elements > 0)
			for(int j = 0; j < allRet->elements; j++)
			{
	//			string landingURL = RedisSmembersFirstOne(allCampaigns->element[j]->str), sub = "";
	//			regex r(cook);
	//			smatch sm;
	//			bool found = regex_search(landingURL, sm, r);
	//			if(cook.length() <= landingURL.length())
	//				sub = landingURL.substr(0, cook.length());
	//			if(sub == cook)
	//			{
	//				string camp = string(allCampaigns->element[j]->str).substr(BannerSite.length(), string(allCampaigns->element[j]->str).npos);
				string camp = string(allRet->element[j]->str);
				RedisSadd("temporaryRetargetting", camp);
	//			}
			}
	}
	return "temporaryRetargetting";
}

list<string> AdEngine::DifferencesofRepliesAdSense(redisReply *Left, redisReply *Right, string RedisURL, string DomainURL)
{
	int l1 = Left->elements;
	list<string> Result;
	if(Right == NULL || (int)Right->elements == 0)
	{
		for(int i = 0; i < l1; i++)
		{
			if(HasEnoughCredit(Left->element[i]->str) == true)
				Result.push_back(Left->element[i]->str);
		}
		return Result;
	}
	int l2 = Right->elements;
	for(int i = 0; i < l1; i++)
	{
		int j = 0;
		for(;j < l2; j++)
		{
			if(string(Left->element[i]->str) == string(Right->element[j]->str))
				break;
			
		}
		if(j == l2 && (HasEnoughCredit(Left->element[i]->str) == true) && !IsBlocked(DomainURL, string(Left->element[i]->str)))
		{
			redisReply *tr = RedisSmembers(KeywordsForCampaignPrefix + string(Left->element[i]->str));
			if(tr == NULL || tr->elements == 0)
				Result.push_back(Left->element[i]->str);
			if((tr != NULL && tr->elements > 0) && RedisSismember(CampaignsForURL + RedisURL, string(Left->element[i]->str)) == true)
				Result.push_back(Left->element[i]->str);
		}
	}
	return Result;
}

list<string> AdEngine::DifferencesofRepliesAdSenseNoKeywords(redisReply *Left, redisReply *Right, string RedisURL, string DomainURL)
{
	int l1 = Left->elements;
	list<string> Result;
	if(Right == NULL || (int)Right->elements == 0)
	{
		for(int i = 0; i < l1; i++)
		{
			if(HasEnoughCredit(Left->element[i]->str) == true)
			{
				redisReply *tmpRes = RedisSmembers(KeywordsForCampaignPrefix + Left->element[i]->str);
				if(tmpRes == NULL || tmpRes->elements == 0)
					Result.push_back(Left->element[i]->str);
			}
		}
		return Result;
	}
	int l2 = Right->elements;
	for(int i = 0; i < l1; i++)
	{
		int j = 0;
		for(;j < l2; j++)
		{
			if(string(Left->element[i]->str) == string(Right->element[j]->str))
				break;
			
		}
		if(j == l2 && (HasEnoughCredit(Left->element[i]->str) == true) && !IsBlocked(DomainURL, string(Left->element[i]->str)))
		{	
			redisReply *tmpRes = RedisSmembers(KeywordsForCampaignPrefix + Left->element[i]->str);
			if(tmpRes == NULL || tmpRes->elements == 0)
			{
				redisReply *tr = RedisSmembers(KeywordsForCampaignPrefix + string(Left->element[i]->str));
				if(tr == NULL || tr->elements == 0)
					Result.push_back(Left->element[i]->str);
				if((tr != NULL && tr->elements > 0) && RedisSismember(CampaignsForURL + RedisURL, string(Left->element[i]->str)) == true)
					Result.push_back(Left->element[i]->str);
			}
		}
	}
	return Result;
}

list<string> AdEngine::DifferencesofRepliesAdWords(redisReply *Left, redisReply *Right, string DomainURL)
{
	int l1 = Left->elements;
	list<string> Result;
	if(Right == NULL || (int)Right->elements == 0)
	{
		for(int i = 0; i < l1; i++)
		{
			if(HasEnoughCredit(Left->element[i]->str) == true)
				Result.push_back(Left->element[i]->str);
		}
		return Result;
	}
	int l2 = Right->elements;
	for(int i = 0; i < l1; i++)
	{
		int j = 0;
		for(;j < l2; j++)
		{
			if(string(Left->element[i]->str) == string(Right->element[j]->str))
				break;
		}
		if(j == l2 && (HasEnoughCredit(Left->element[i]->str) == true) && !IsBlocked(DomainURL, string(Left->element[i]->str)))
			Result.push_back(Left->element[i]->str);
	}
	return Result;
}

list<string> AdEngine::DifferencesofRepliesAdWordsModified(list<redisReply *> Left, redisReply *Right, string DomainURL)
{
	list<string> allBanners = UnionOfRedisReplies(Left);
	list<string> Result;
	if(Right == NULL || (int)Right->elements == 0)
	{
		for(list<string>::iterator itt = allBanners.begin(); itt != allBanners.end(); itt++)
		{
			if(HasEnoughCredit(*itt) == true)
				Result.push_back(*itt);
		}
		return Result;
	}
	int l2 = Right->elements;
	for(list<string>::iterator itt = allBanners.begin(); itt != allBanners.end(); itt++)
	{
		int j = 0;
		for(;j < l2; j++)
		{
			if(string(*itt) == string(Right->element[j]->str))
				break;
		}
		if(j == l2 && (HasEnoughCredit(*itt) == true) && !IsBlocked(DomainURL, string(*itt)))
			Result.push_back(*itt);
	}
	return Result;
}

list<string> AdEngine::UnionOfRedisReplies(list<redisReply*> Result)
{
	list<string> Output;
	for(list<redisReply *>::iterator it = Result.begin(); it != Result.end(); it++)
		for(int i = 0; i < (*it)->elements; i++)
		{
			string camp = (*it)->element[i]->str;
			bool Exist = false;
			for(list<string>::iterator itt = Output.begin(); itt != Output.end(); itt++)
				if(*itt == camp)
				{
					Exist = true;
					break;
				}
			if(Exist == false)
				Output.push_back(camp);
		}
	return Output;
		
}


bool AdEngine::IsBlocked(string DomainURL, string CampaignID)
{
	string landing = RedisSmembersFirstOne(BannerSite + CampaignID);
	string domainLanding = ExtractRootURL(landing);
	domainLanding = GetRawURL(domainLanding);
	bool b = RedisSismember(PublisherBlockList + DomainURL, CampaignID);
	if(b)
		return true;
	return false;
}

list<string> AdEngine::RedisReplytoList(redisReply* reply)
{
	list<string> res;
	int i = 0;
	int k = reply->elements;
	while(i < k)
	{
		string data = reply->element[i]->str;
		res.push_front(data);
		i++;
	}
	return res;
}

string AdEngine::ResolveTime()
{
    time_t tmp = time(nullptr);
    tm *currTime = localtime(&tmp);
    string Result = "";
    if(currTime->tm_hour < 8)
        Result = Time0to8;
    else if(currTime->tm_hour < 16)
        Result = Time8to4;
    else
        Result = Time4to0;
    return Result;
}

////////////////////////////////////////////////////Elasticsearch Region///////////////////////////////////////////////////////////
string AdEngine::Elasticsearch_GetActiveServer()
{
	string curr = ElasticIPPorts[0];
	for (int i = 0; i < ElasticServerCount; i++) {
		string res = Elasticsearch_Request("", ElasticIPPorts[i], "", "");
		if(res != "")
		{
			curr = ElasticIPPorts[i];
			break; 
		}
	}
	return curr;
}

bool AdEngine::Elasticsearch_SaveSiteContents(string URL, string apiAddress)
{
	string Cont = GetWebsiteContent(URL);
	regex r1("\"");
	Cont = regex_replace(Cont, r1, "'");
	r1.assign("\n|\t|\r|\\\\");
	Cont = regex_replace(Cont, r1, " ");
	
	ofstream outf;
	outf.open("/home/rera/url.txt");
	outf<<Cont;
	outf.close();
	string Content = RequestToWebservice(apiAddress, "{\"url\": \"" + Cont + "\"}", "", "Content-Type: application/json", "");
	r1.assign("400 Bad Request");
	smatch sm;
	if(regex_search(Content, sm, r1))
		return true;
 	string cleanContent = "";
	json_error_t error;
	json_t *root = json_loads(Content.c_str(), 0, &error);
	if(json_is_object(root))
	{		
		json_t * status = json_object_get(root, "status");
		if(json_is_string(status))
		{
			string st = json_string_value(status);
			if(st == "yes")
			{
				json_t * text = json_object_get(root, "body");
				if(json_is_string(text))
					cleanContent = json_string_value(text);
			}
		}
	}	
		
//	string Content = GetWebsiteContent(URL);
	cout<<"Website Fetched..."<<endl;
//	string cleanContent = "";
//	cleanContent = HTMLToContent(Content);
	AssignBannersToURL(URL, cleanContent);
	cout<<"Campaign Assigned to Website..."<<endl;
	string tmpRes = RedisGet(ElasticWebPageContentCount);
	int counter = 0;
	if(tmpRes != "")
		counter = stoi(tmpRes);
	
	string tmp = JsonEscape(cleanContent);
	time_t tmp1 = time(nullptr);
	tm *currTime = localtime(&tmp1);
	string Day = to_string(currTime->tm_mday), Month = to_string(currTime->tm_mon + 1);
	string Hour = to_string(currTime->tm_hour), Min = to_string(currTime->tm_min);
	string Sec = to_string(currTime->tm_sec), Year = to_string(currTime->tm_year + 1900);
	Day = string(2 - Day.length(), '0') + Day;
	Hour = string(2 - Hour.length(), '0') + Hour;
	Month = string(2 - Month.length(), '0') + Month;
	Min = string(2 - Min.length(), '0') + Min;
	Sec = string(2 - Sec.length(), '0') + Sec;
	string RequestTime = Year + "-" + Month + "-" + Day + Hour + ":" + Min + ":" + Sec;
	
//	double now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
//	string RequestTime = to_string(now);
        regex r("\\-|\\.|\\/|\\:|\\?|\\+|\\*|\\||\\{|\\}|\\[|\\]|\\(|\\)");
        string elasticURL = regex_replace(URL, r, "_");
        
	string CleanContent = "{ \"SiteContent\" : \"" + tmp + "\", \"URL\" : \"" + elasticURL + "\", \"Time\" : \"" + RequestTime + "\"}";

	Elasticsearch_Add(ElasticWebpageIndex, ElasticHTMLContentType, counter + 1, CleanContent);
	cout<<"Website Saved in Elasticsearch..."<<endl;
	counter++;
	RedisSet(ElasticWebPageContentCount, to_string(counter));
	RedisSadd(CrawledWebpages, ConvertURLtoRedisFormat(URL));
	return true;
}

string AdEngine::Elasticsearch_Request(string Command, string URL, string Data, string Header)
{
	CURL *curl = curl_easy_init();
	CURLcode res;
	if(curl)
	{
		struct curl_slist *headers = NULL;
		headers = curl_slist_append(headers, Header.c_str());
		string Result = "";
		if(Header != "")
			curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
		curl_easy_setopt(curl, CURLOPT_URL, URL.c_str());
		if(Command != "")
			curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, Command.c_str());
		if(Data != "")
			curl_easy_setopt(curl, CURLOPT_POSTFIELDS, Data.c_str());
		curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &AdEngine::writeCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &Result);
		curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L); //tell curl to output its progress
		res = curl_easy_perform(curl);
		curl_easy_cleanup(curl);
		return Result;
	}
	return "";
	
}

void AdEngine::Elasticsearch_UpdateCampaignForURL(string URL, string CampaignID)
{
	string newURL = URL, Content = "";
//	if(URL.substr(0, 7) == "http://")
//		newURL = URL.substr(7, URL.npos);
//	if(URL.substr(0, 8) == "https://")
//		newURL = URL.substr(8, URL.npos);
//	regex r("/");
//	newURL = regex_replace(newURL, r, "*");
        
        regex r("\\-|\\.|\\/|\\:|\\?|\\+|\\*|\\||\\{|\\}|\\[|\\]|\\(|\\)");
        newURL = regex_replace(URL, r, "_");
        
	string ActiveServer = Elasticsearch_GetActiveServer();
	string ElasticURL = ActiveServer + ElasticWebpageIndex + "/_search?pretty";
	string Header = "Content-Type : application/json";
	string Query = "{\"query\": {\"wildcard\": {\"URL\": \"" + newURL + "\"}}}";
	string jsonRes = Elasticsearch_WebpageSearch(Query);
	json_error_t error;
	json_t *root = json_loads(jsonRes.c_str(), 0, &error);
	if(!json_is_object(root))
		return;
	json_t * hits = json_object_get(root, "hits");
	if(!json_is_object(hits))
		return;
	json_t * total = json_object_get(hits, "total");
	if(!json_is_integer(total))
		return;
	int count = json_integer_value(total);
	if(count > 0)
	{
		hits = json_object_get(hits, "hits");
		if(!json_is_array(hits))
			return;
		int k = json_array_size(hits);
		if(k > 0)
		{
			hits = json_array_get(hits, 0);
			json_t *source = json_object_get(hits, "_source");
			if(!json_is_object(source))
				return;
			json_t *SiteContent = json_object_get(source, "SiteContent");
			if(!json_is_string(SiteContent))
				return;
			Content = json_string_value(SiteContent);
			RedisSrem(CampaignsForURL + ConvertURLtoRedisFormat(URL), CampaignID);
			RedisDel("keyForURL_" + ConvertURLtoRedisFormat(URL) + "_" + CampaignID);
			AssignOneBannerToURL(URL, Content, CampaignID);
		}
	}
}

string AdEngine::Elasticsearch_WebpageSearch(string Query)
{
    string Result = "";
    CURLcode ret;
  CURL *hnd;
  struct curl_slist *slist1;

  slist1 = NULL;
  slist1 = curl_slist_append(slist1, "Content-Type: application/json");

  hnd = curl_easy_init();
  curl_easy_setopt(hnd, CURLOPT_URL, "localhost:9200/webpage/_search?pretty");
  curl_easy_setopt(hnd, CURLOPT_NOPROGRESS, 1L);
  curl_easy_setopt(hnd, CURLOPT_POSTFIELDS, Query.c_str());
  curl_easy_setopt(hnd, CURLOPT_POSTFIELDSIZE_LARGE, (curl_off_t)Query.size());
  curl_easy_setopt(hnd, CURLOPT_USERAGENT, "curl/7.47.0");
  curl_easy_setopt(hnd, CURLOPT_HTTPHEADER, slist1);
  curl_easy_setopt(hnd, CURLOPT_MAXREDIRS, 50L);
  curl_easy_setopt(hnd, CURLOPT_WRITEFUNCTION, &AdEngine::writeCallback);
  curl_easy_setopt(hnd, CURLOPT_WRITEDATA, &Result);
  curl_easy_setopt(hnd, CURLOPT_TCP_KEEPALIVE, 1L);

  /* Here is a list of options the curl code used that cannot get generated
     as source easily. You may select to either not use them or implement
     them yourself.

  CURLOPT_WRITEDATA set to a objectpointer
  CURLOPT_WRITEFUNCTION set to a functionpointer
  CURLOPT_READDATA set to a objectpointer
  CURLOPT_READFUNCTION set to a functionpointer
  CURLOPT_SEEKDATA set to a objectpointer
  CURLOPT_SEEKFUNCTION set to a functionpointer
  CURLOPT_ERRORBUFFER set to a objectpointer
  CURLOPT_STDERR set to a objectpointer
  CURLOPT_HEADERFUNCTION set to a functionpointer
  CURLOPT_HEADERDATA set to a objectpointer

  */

  ret = curl_easy_perform(hnd);
  curl_easy_cleanup(hnd);
  hnd = NULL;
  curl_slist_free_all(slist1);
  slist1 = NULL;
  return Result;
}

string AdEngine::Elasticsearch_GetTimeofRetrievingWebpage(string URL)
{
	string newURL = URL, Time = "";
//	if(URL.substr(0, 7) == "http://")
//		newURL = URL.substr(7, URL.npos);
//	if(URL.substr(0, 8) == "https://")
//		newURL = URL.substr(8, URL.npos);
//	regex r("/");
//	newURL = regex_replace(newURL, r, "*");
        regex r("\\-|\\.|\\/|\\:|\\?|\\+|\\*|\\||\\{|\\}|\\[|\\]|\\(|\\)");
        newURL = regex_replace(URL, r, "_");
        
	string ActiveServer = Elasticsearch_GetActiveServer();
	string ElasticURL = ActiveServer + ElasticWebpageIndex + "/_search?pretty";
	string Header = "Content-Type : application/json";
	string Query = "{\"query\": {\"wildcard\": {\"URL\": \"" + newURL + "\"}}}";
//	string jsonRes = Elasticsearch_Request("POST", ElasticURL, Query, Header);
        string jsonRes = Elasticsearch_WebpageSearch(Query);
	json_error_t error;
	json_t *root = json_loads(jsonRes.c_str(), 0, &error);
	if(!json_is_object(root))
		return "";
	json_t * hits = json_object_get(root, "hits");
	if(!json_is_object(hits))
		return "";
	json_t * total = json_object_get(hits, "total");
	if(!json_is_integer(total)) 
		return "";
	int count = json_integer_value(total);
	if(count > 0)
	{
		hits = json_object_get(hits, "hits");
		if(!json_is_array(hits))
			return "";
		int k = json_array_size(hits);
		if(k > 0)
		{
			hits = json_array_get(hits, 0);
			json_t *source = json_object_get(hits, "_source");
			if(!json_is_object(source))
				return "";
			json_t *TimeE = json_object_get(source, "Time");
			if(!json_is_string(TimeE))
				return "";
			Time = json_string_value(TimeE);
			return Time;
		}
	}
	return "";
}

int AdEngine::Elasticsearch_GetNumberOfDocsInSearchIndexType(string Index, string Type)
{
	string URL = "";
	string ActiveServer = Elasticsearch_GetActiveServer();
	if(Type != "")
		URL = ActiveServer + Index + "/" + Type + "/_count";
	else
		URL = ActiveServer + Index + "/_count";
	string Responce = GetWebsiteContent(URL);
	regex r("\\\"count\\\":(\\d)+");
	smatch sm, Res;
	regex_search(Responce, sm, r);
	r.assign("\\d+");
	string count = sm[0];
	regex_search(count, Res, r);
	string Result = Res[0];
	return stoi(Result);
}

void AdEngine::Elasticsearch_Add(string Index, string Type, int Id, string newDoc)
{
	CURL *curl;
	CURLcode res;
	string ActiveServer = Elasticsearch_GetActiveServer();
	string tmp = ActiveServer + Index + "/" + Type + "/" + to_string(Id) + "?pretty&pretty";
	char *URL = Strcpy(tmp);

	char *data = Strcpy(newDoc);
	curl = curl_easy_init();
	string ReqContent = "";
	if(curl) {
	     struct curl_slist *headers = NULL;
	     headers = curl_slist_append(headers, "Content-Type: application/json");
	     curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
	     curl_easy_setopt(curl, CURLOPT_URL, URL);
	     curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PUT");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &AdEngine::writeCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &ReqContent);
		curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L); //tell curl to output its progress
	     curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
	     res = curl_easy_perform(curl);
	     curl_easy_cleanup(curl);
	}
}

void AdEngine::Elasticsearch_SaveLogsFromRedis(string LogStatus, string ElasticLogStatus)
{
	redisReply *reply = RedisKeys(LogStatus + "*");
	string Index = ElasticLogIndex;
	string Type = LogStatus;
	if(reply != NULL && reply->elements > 0)
		for(int i = 0; i < reply->elements; i++)
		{
			string tmpRes = RedisGet(ElasticLogStatus);
			int counter = 0;
			if(tmpRes != "")
				counter = stoi(tmpRes);
			string LogKey = reply->element[i]->str;
			string Log = RedisGet(LogKey);
			list<string> data = strSplit(Log, '_');
			string IP = data.back();
			data.pop_back();
			string Resolution = data.back();
			data.pop_back();
			string OS = data.back();
			data.pop_back();
			string URL = ConvertRedisFormattoURL(data.back());
			data.pop_back();
			string siteID = RedisSmembersFirstOne(WebsiteToID + GetRawURL(ExtractRootURL(URL)));
			
			string Banner = data.back();
			data.pop_back();
			string Time = data.back();
			data.pop_back();
			string QueryOrSize = data.back();
			data.pop_back();
			string BannerClickCost = RedisSmembersFirstOne(ClickCost + Banner);
			string newDoc = "";
			string Location = "Unknown";
			if(IP != "")
				Location = NewIP2Location(IP);
			if(LogStatus == ShowAdSenseLog || LogStatus == ShowAdWordsLog)
				newDoc = "{ \"IPAddress\" : \"" + IP + 
					"\", \"UserResolution\" : \"" + Resolution + 
					"\", \"UserLocation\" : \"" + Location + 
					"\", \"SiteURL\" : \"" + URL +
					"\", \"SiteID\" : \"" + siteID +
					"\", \"UserOS\" : \"" + OS +
					"\", \"CampaignID\" : \"" + Banner +
					"\", \"ClickCost\" : \"" + BannerClickCost +
					"\", \"QueryOrSize\" : \"" + QueryOrSize +
					"\", \"Time\" : \"" + Time + "\" }";
			else if(LogStatus == ClickAdSenseLog)
			{
				string UserData = data.back();
				data.pop_back();
				string RealUnReal = data.back();
				data.pop_back();
				newDoc = "{ \"IPAddress\" : \"" + IP + 
					"\", \"UserResolution\" : \"" + Resolution + 
					"\", \"UserLocation\" : \"" + Location + 
					"\", \"SiteURL\" : \"" + URL +
					"\", \"SiteID\" : \"" + siteID +
					"\", \"UserOS\" : \"" + OS +
					"\", \"CampaignID\" : \"" + Banner +
					"\", \"ClickCost\" : \"" + BannerClickCost +
					"\", \"ClickStatus\" : \"" + RealUnReal +
					"\", \"QueryOrSize\" : \"" + QueryOrSize +
					"\", \"UserData\" : \"" + UserData +
					"\", \"Time\" : \"" + Time + "\" }";
			}
			else if(LogStatus == ClickAdWordsLog)
			{
				data.back();
				data.pop_back();
				string RealUnReal = data.back();
				data.pop_back();
				newDoc = "{ \"IPAddress\" : \"" + IP + 
					"\", \"UserResolution\" : \"" + Resolution + 
					"\", \"UserLocation\" : \"" + Location + 
					"\", \"SiteURL\" : \"" + URL +
					"\", \"SiteID\" : \"" + siteID +
					"\", \"UserOS\" : \"" + OS +
					"\", \"CampaignID\" : \"" + Banner +
					"\", \"ClickCost\" : \"" + BannerClickCost +
					"\", \"ClickStatus\" : \"" + RealUnReal +
					"\", \"QueryOrSize\" : \"" + QueryOrSize +
					"\", \"Time\" : \"" + Time + "\" }";
			}
			Elasticsearch_Add(Index, Type, counter + 1, newDoc);
//			string elURL = ElasticIPPort + Index + "/" + Type + "?pretty";
//			string s = Elasticsearch_Request("PUT", elURL, newDoc, "Content-Type : application/json");
			counter++;
			RedisSet(ElasticLogStatus, to_string(counter));
			RedisDel(LogKey);
		}
}

void AdEngine::Elasticsearch_Update()
{
	Elasticsearch_SaveLogsFromRedis(ShowAdSenseLog, ElasticShowAdSenseLogCount);
	Elasticsearch_SaveLogsFromRedis(ShowAdWordsLog, ElasticShowAdWordsLogCount);
	Elasticsearch_SaveLogsFromRedis(ClickAdSenseLog, ElasticClickAdSenseLogCount);
	Elasticsearch_SaveLogsFromRedis(ClickAdWordsLog, ElasticClickAdWordsLogCount);
	RedisSet(ShowAdSenseLogCount, "0");
	RedisSet(ClickAdSenseLogCount, "0");
	RedisSet(ShowAdWordsLogCount, "0");
	RedisSet(ClickAdWordsLogCount, "0");
}

bool AdEngine::Elasticsearch_CheckExistence(string Index)
{
	string ActiveServer = Elasticsearch_GetActiveServer();
	string URL = ActiveServer + Index + "?pretty";
	string res = Elasticsearch_Request("-IHEAD", URL, "", "");
	smatch sm;
	regex r("index_not_found_exception");
	if(res.size() < 10 || regex_search(res, sm, r))
		return false;
	return true;
}

void AdEngine::Elasticsearch_Initialize()
{
	string s = "{";
	string Mapping = "{ \"properties\" : " + s + 
				"\"CampaignID\" : {" +
					"\"type\" : \"text\"," +
					"\"index\": \"not_analyzed\"}," +
				"\"IPAddress\" : {" +
					"\"type\" : \"keyword\"," +
					"\"index\": \"not_analyzed\"}," +
				"\"UserLocation\" : {" +
					"\"type\" : \"keyword\"," +
					"\"index\": \"not_analyzed\"}," +
				"\"QueryOrSize\" : {" +
					"\"type\" : \"text\" }," +
				"\"SiteURL\" : {" + 
					"\"type\" : \"keyword\"," +
					"\"index\": \"not_analyzed\"}," +
				"\"UserData\" : {" + 
					"\"type\" : \"keyword\"," +
					"\"index\": \"not_analyzed\"}," +
				"\"SiteID\" : {" + 
					"\"type\" : \"keyword\"," +
					"\"index\": \"not_analyzed\"}," +
				"\"Time\" : {" +
					"\"type\" : \"date\", " +
					"\"format\": \"yyyy-MM-ddHH:mm:ss\" }, " + 
				"\"ClickCost\" : {" +
					"\"type\" : \"text\" }," +
				"\"UserOS\" : {" +
					"\"type\" : \"text\" }," +
				"\"UserResolution\" : {" +
					"\"type\" : \"text\" }" +
			" } }";
	string ActiveServer = Elasticsearch_GetActiveServer();
	string URL = ActiveServer + ElasticLogIndex + "?pretty";
	s = Elasticsearch_Request("PUT", URL, "", "");
	URL = ActiveServer + ElasticLogIndex + "/_mapping/" + ShowAdSenseLog + "?pretty";
	s = Elasticsearch_Request("PUT", URL, Mapping, "Content-type: application/json");
	URL = ActiveServer + ElasticLogIndex + "/_mapping/" + ShowAdWordsLog + "?pretty";
	s = Elasticsearch_Request("PUT", URL, Mapping, "Content-type: application/json");
	URL = ActiveServer + ElasticLogIndex + "/_mapping/" + ClickAdSenseLog + "?pretty";
	s = Elasticsearch_Request("PUT", URL, Mapping, "Content-type: application/json");
	URL = ActiveServer + ElasticLogIndex + "/_mapping/" + ClickAdWordsLog + "?pretty";
	s = Elasticsearch_Request("PUT", URL, Mapping, "Content-type: application/json");
	
	Mapping = "{ \"properties\" : " + s + 
			"\"SiteContent\" : {" +
				"\"type\" : \"text\" }," +
			"\"URL\" : {" + 
				"\"type\" : \"text\" ," + 
				"\"index\": \"not_analyzed\"},"
			"\"Time\" : {" +
				"\"type\" : \"date\"," +
				"\"format\": \"yyyy-MM-ddHH:mm:ss\"," + 
				"\"index\": \"not_analyzed\"}" +
		" } }";
	URL = ActiveServer + ElasticWebpageIndex + "?pretty";
	s = Elasticsearch_Request("PUT", URL, "", "");
	URL = ActiveServer + ElasticWebpageIndex + "/_mapping/" + ElasticHTMLContentType + "?pretty";
	s = Elasticsearch_Request("PUT", URL, Mapping, "Content-type: application/json");
}
////////////////////////////////////////////////////End of Elasticsearch Region////////////////////////////////////////////////////

string AdEngine::GetWebsiteContent(string URL)
{
	CURL *curl;
	CURLcode res;
	curl_global_init(CURL_GLOBAL_ALL); //pretty obvious
	curl = curl_easy_init();
	if(curl) {
		char *chURL = Strcpy(URL);
		string WebContent = "";
		curl_easy_setopt(curl, CURLOPT_URL, chURL);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &AdEngine::writeCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &WebContent);
		curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L); //tell curl to output its progress
		res = curl_easy_perform(curl);
		/* always cleanup */
		curl_easy_cleanup(curl);
		return WebContent;
	}
	return "";
}

string AdEngine::RequestToWebservice(string URL, string Data, string Command, string Header1, string Header2)
{
	CURL *curl = curl_easy_init();
	CURLcode res;
	if(curl)
	{
		struct curl_slist *headers = NULL;
		if(Header1 != "")
			headers = curl_slist_append(headers, Header1.c_str());
		if(Header2 != "")
			headers = curl_slist_append(headers, Header2.c_str());
		string Result = "";
		if(Header1 != "" || Header2 != "")
			curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
		curl_easy_setopt(curl, CURLOPT_URL, URL.c_str());

		if (Command != "")
			curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, Command.c_str());
		if(Data != "")
			curl_easy_setopt(curl, CURLOPT_POSTFIELDS, Data.c_str());
		curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &AdEngine::writeCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &Result);
		curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L); //tell curl to output its progress
		res = curl_easy_perform(curl);
		curl_easy_cleanup(curl);
		return Result;
	}
	return "";
	
}

void AdEngine::AssignBannersToURL(string URL, string Content)
{
	string ActiveServer = Elasticsearch_GetActiveServer();
	string url = ActiveServer + ElasticWebpageIndex + "/_search?pretty";
	string Data = "{\"from\" : 0, \"size\" : 1, \"query\" : {\"match\" : {\"URL\" : \"" + URL + "\"} } }";
	string Header = "Content-Type: application/json";
	redisReply *allBanners = RedisKeys(ClickCost + "*");
	int l = allBanners->elements;
	for(int i = 0; i < l; i++)
	{
		string CampaignID = string(allBanners->element[i]->str).substr(ClickCost.length(), string(allBanners->element[i]->str).npos);
		AssignOneBannerToURL(URL, Content, CampaignID);
	}
}

void AdEngine::AssignOneBannerToURL(string URL, string Content, string CampaignID)
{
	redisReply *bannerKeywords = RedisSmembers(KeywordsForCampaignPrefix + CampaignID);
	int s = 0, j;
	if(bannerKeywords != NULL)
		s = bannerKeywords->elements;
	for(j = 0; j < s; j++)
	{
		regex r("-");
		string Keyword = regex_replace(bannerKeywords->element[j]->str, r, " ");
		Keyword = " " + Keyword + " ";
		r.assign(Keyword);
		smatch sm;
		bool find = regex_search(Content, sm, r);
		if(find)
		{
			RedisSadd(CampaignsForURL + ConvertURLtoRedisFormat(URL), CampaignID);
			RedisSet("keyForURL_" + ConvertURLtoRedisFormat(URL) + "_" + CampaignID, bannerKeywords->element[j]->str);
			break;
		}
	}
}


/////////////////////////////////////////////////////////Redis Region////////////////////////////////////////////////////////
redisContext *AdEngine::ImprovedRedisConnectWrite()
{
	redisContext *ct = (redisContext *)redisConnectWithTimeout(RedisServerIPs[0].c_str(), RedisPort, timeout);
	redisReply *test = (redisReply *)redisCommand(ct, "PING");
	for (int i = 1; i < RedisServerCount; i++)
	{
		if(test == NULL || test->str == NULL || string(test->str) != "PONG")
		{
			ct = (redisContext *)redisConnectWithTimeout(RedisServerIPs[i].c_str(), RedisPort, timeout);
			test = (redisReply *)redisCommand(ct, "PING");
		}
		else
			break;
	}
	return ct;
}
redisContext *AdEngine::ImprovedRedisConnectRead()
{
	redisContext *ct = (redisContext *)redisConnectWithTimeout("127.0.0.1", RedisPort, timeout);
	redisReply *test = (redisReply *)redisCommand(ct, "PING");
	for (int i = 0; i < RedisServerCount; i++)
	{
		if(test == NULL || test->str == NULL || string(test->str) != "PONG")
		{
			ct = (redisContext *)redisConnectWithTimeout(RedisServerIPs[i].c_str(), RedisPort, timeout);
			test = (redisReply *)redisCommand(ct, "PING");
		}
		else
			break;
	}
	return ct;
}

redisReply * AdEngine::RedisSet(string Key, string Value)
{
	if(cWrite->err != 0)
	{
		redisFree(cWrite);
		cWrite = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cWrite = ImprovedRedisConnectWrite();
	}
	regex r(" ");
	string newValue = regex_replace(Value, r, "-");
	string command = "SET " + Key + " " + newValue;
	redisReply *reply = (redisReply *)redisCommand(cWrite, command.c_str());
	return reply;
}

redisReply * AdEngine::RedisSetWithFlag(string Key, string Value)
{
	if(cWrite->err != 0)
	{
		redisFree(cWrite);
		cWrite = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cWrite = ImprovedRedisConnectWrite();
	}
	string command = "SET " + Key + " " + Value;
	redisReply *reply = (redisReply *)redisCommand(cWrite, command.c_str());
	return reply;
}

redisReply *AdEngine::RedisSadd(string Key, string Value)
{
	if(cWrite->err != 0)
	{
		redisFree(cWrite);
		cWrite = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cWrite = ImprovedRedisConnectWrite();
	}
	string command = "SADD " + Key + " " + Value;
	redisReply *reply = (redisReply *)redisCommand(cWrite, command.c_str());
	return reply;
}

redisReply *AdEngine::RedisSaddNoSpace(string Key, string Value)
{
	if(cWrite->err != 0)
	{
		redisFree(cWrite);
		cWrite = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cWrite = ImprovedRedisConnectWrite();
	}
	regex r(" ");
	string newValue = regex_replace(Value, r, "-");
	string command = "SADD " + Key + " " + newValue;
	redisReply *reply = (redisReply *)redisCommand(cWrite, command.c_str());
	return reply;
}

string AdEngine::RedisGet(string Key)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cRead = ImprovedRedisConnectRead();
	}
	string command = "GET " + Key;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	if(reply == NULL || reply->str == NULL)
		return "";
	else
		return string(reply->str);
}

redisReply *AdEngine::RedisSmembers(string Key)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cRead = ImprovedRedisConnectRead();
	}
	string command = "SMEMBERS " + Key;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	return reply;
}

bool AdEngine::RedisSismember(string Key, string Member)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cRead = ImprovedRedisConnectRead();
	}
	string command = "SISMEMBER " + Key + " " + Member;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	if(reply != NULL && reply->integer == 1)
		return true;
	return false;
}

bool AdEngine::RedisExists(string Key)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
		cRead = ImprovedRedisConnectRead();
	}
	string command = "Exists " + Key;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	if(reply != NULL && reply->integer == 1)
		return true;
	return false;
}

string AdEngine::RedisSmembersFirstOne(string Key)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cRead = ImprovedRedisConnectRead();
	}
	string command = "SMEMBERS " + Key;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	if(reply == NULL || reply->elements == 0)
		return "";
	return reply->element[0]->str;
}

redisReply *AdEngine::RedisKeys(string Pattern)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cRead = ImprovedRedisConnectRead();
	}
	string command = "KEYS " + Pattern;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	return reply;
}

void AdEngine::RedisSrem(string Key, string Value)
{
	if(cWrite->err != 0)
	{
		redisFree(cWrite);
		cWrite = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cWrite = ImprovedRedisConnectWrite();
	}
	string command = "SREM " + Key + " " + Value;
	redisReply *reply = (redisReply *)redisCommand(cWrite, command.c_str());
}

void AdEngine::RedisDel(string Key)
{
	if(cWrite->err != 0)
	{
		redisFree(cWrite);
		cWrite = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cWrite = ImprovedRedisConnectWrite();
	}
	string command = "DEL " + Key;
	redisReply *reply = (redisReply *)redisCommand(cWrite, command.c_str());
}

redisReply *AdEngine::RedisSunion(string Key1, string Key2)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cRead = ImprovedRedisConnectRead();
	}
	string command = "SUNION " + Key1 + " " + Key2;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	return reply;
}

redisReply *AdEngine::RedisSinter(string Keys)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cRead = ImprovedRedisConnectRead();
	}
	string command = "SINTER " + Keys;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	return reply;
}


void AdEngine::RedisRemoveObsoleteKeys()
{
	if(cWrite->err != 0)
	{
		redisFree(cWrite);
		cWrite = NULL;
//		c = redisConnect(RedisIP.c_str(), RedisPort);
		cWrite = ImprovedRedisConnectWrite();
	}
	redisReply *desiredKeys = RedisKeys("hashed*");
	int l = desiredKeys->elements;
	for(int i = 0; i < l; i++)
	{
		RedisDel(desiredKeys->element[i]->str);
	}
}

int AdEngine::RedisScard(string Key)
{
	if(cRead->err != 0)
	{
		redisFree(cRead);
		cRead = NULL;
		cRead = ImprovedRedisConnectRead();
	}
	string command = "SCARD " + Key;
	redisReply *reply = (redisReply *)redisCommand(cRead, command.c_str());
	if(reply != NULL)
		return reply->integer;
	else
		return 0;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////
char *AdEngine::Strcpy(string Entry)
{
	int l = Entry.length();
	char *Result = new char[l + 1];
	for(int i = 0; i < l; i++)
		Result[i] = Entry[i];
	Result[l] = '\0';
	return Result;
}

size_t AdEngine::writeCallback(char* buf, size_t size, size_t nmemb, string * up)
{ //callback must have this declaration
    //buf is a pointer to the data that curl has for us
    //size*nmemb is the size of the buffer

    for (int c = 0; c<size*nmemb; c++)
    {
        up->push_back(buf[c]);
    }
    return size*nmemb; //tell curl how many bytes we handled
}

string AdEngine::JsonEscape(string Entry)
{
	string Result = "";
	for (int i = 0; i < Entry.length(); i++) {
		if (Entry[i] == '"' || Entry[i] == '\\' || ('\x00' <= Entry[i] && Entry[i] <= '\x1f')) {
			Result += "";
		} 
		else {
			Result += Entry[i];
		}
	}
    return Result;
}

bool AdEngine::IsRealClick(string URL, string UserIP, string UserResolution, string BannerID, string UserOS)
{
//	string Key = "cheat_" + URL + "_" + UserIP + "_" + UserOS + "_" + UserResolution + "_" + BannerID;
	string turl = ExtractRootURL(URL);
	string Key = "cheat_" + turl + "_" + UserIP + "_" + BannerID;
	string se = RedisGet(Key);
	if(se != "" && se != "ERR wrong number of arguments for 'get' command")
	{
		try
		{
			double co = stod(se);
			if(co >= 1)
				return false;
		}
		catch(exception &e)
		{
			return false;
		}
	}
	return true;
}

void AdEngine::UpdateCheat(string URL, string UserIP, string UserResolution, string BannerID, string UserOS)
{
//	string Key = "cheat_" + URL + "_" + UserIP + "_" + UserOS + "_" + UserResolution + "_" + BannerID;
	string turl = ExtractRootURL(URL);
	string Key = "cheat_" + turl + "_" + UserIP + "_" + BannerID;
	string se = RedisGet(Key);
	if(se == "")
		RedisSet(Key, "1");
	else
	{
		int i = stoi(se);
		RedisSet(Key, to_string(i + 1));
	}
}

bool AdEngine::IsAttack(string IPAdress)
{
	bool Result = false;
	int count = 0;
	string strCount = RedisGet("attack_" + IPAdress);
	if(strCount != "" && stoi(strCount) > 5)
		Result = true;
	count = (strCount != "") ? (stoi(strCount) + 1) : 1;
	RedisSet("attack_" + IPAdress, to_string(count));
	return Result;
}

void AdEngine::DeleteCheatsAndAttacks()
{
	string Key = "cheat_*";
	redisReply *AllCheats = RedisKeys(Key);
	if(AllCheats == NULL || AllCheats->elements == 0)
		return;
	int l = AllCheats->elements;
	for(int i = 0; i < l; i++)
	{
		RedisDel(AllCheats->element[i]->str);
	}
	Key = "attack_*";
	redisReply *AllAttacks = RedisKeys(Key);
	if(AllAttacks == NULL || AllAttacks->elements == 0)
		return;
	l = AllAttacks->elements;
	for(int i = 0; i < l; i++)
	{
		RedisDel(AllAttacks->element[i]->str);
	}
}

string AdEngine::RedirectWhenClick(string IPAddress, string UserResolution, string UserOS, string SiteURL, string BannerId, string QueryOrSize, bool AdSenseOrAdWords, string &Debugging, string UserData)
{
	string RealUnReal = "";
	regex r("_| ");
	string HomeURL = ExtractRootURL(SiteURL);
	HomeURL = GetRawURL(HomeURL);
	UserOS = regex_replace(UserOS, r, "-");
	if(IsRealClick(SiteURL, IPAddress, UserResolution, BannerId, UserOS) == true)
		RealUnReal = "Real";
	else
		RealUnReal = "UnReal";
	Debugging = "This click is " + RealUnReal + "<br>";
	if(AdSenseOrAdWords == true)
		SaveAdSenseClickLogtoRedis(IPAddress, UserResolution, UserOS, SiteURL, BannerId, QueryOrSize, RealUnReal, UserData);
	else if(AdSenseOrAdWords == false)
		SaveAdWordsClickLogtoRedis(IPAddress, UserResolution, UserOS, SiteURL, BannerId, QueryOrSize, RealUnReal);
	string Result = "";
	
	if(RealUnReal == "Real" && HasEnoughCredit(BannerId))
	{
		while(true)
		{
			redisReply *rR = RedisSetWithFlag("mutex_click", "grabbed NX EX 60");
			if(rR != NULL && rR->str != NULL && string(rR->str) == "OK")
				break;
		}
		string tmpDailyAsset = RedisSmembersFirstOne(CampaignVariableDailyBudget + BannerId);
		string tmpTotalAsset = RedisSmembersFirstOne(CampaignTotalBudget + BannerId);
		string tmpCost = RedisSmembersFirstOne(ClickCost + BannerId);
		if(tmpDailyAsset != "" && tmpTotalAsset != "" && tmpCost != "")
		{
			double newDailyAsset = stod(tmpDailyAsset);
			double newTotalAsset = stod(tmpTotalAsset);
			double CostOfClicks = stod(tmpCost);
			newDailyAsset = newDailyAsset - CostOfClicks;
			newTotalAsset = newTotalAsset - CostOfClicks;
			RedisDel(CampaignVariableDailyBudget + BannerId);
			RedisDel(CampaignTotalBudget + BannerId);
			RedisSadd(CampaignVariableDailyBudget + BannerId, to_string(newDailyAsset));
			RedisSadd(CampaignTotalBudget + BannerId, to_string(newTotalAsset));
			Result = RedisSmembersFirstOne(BannerSite + BannerId);
			UpdateCheat(SiteURL, IPAddress, UserResolution, BannerId, UserOS);
			string Percent = RedisSmembersFirstOne(PublisherBenefitPercentage + HomeURL);
			string websiteID = RedisSmembersFirstOne("publisher_id_website_" + HomeURL);
			if(Percent != "" && websiteID != "")
			{
				string TotalWebsiteBenefit = RedisSmembersFirstOne(PublisherTotalBenefit + HomeURL);
				if(TotalWebsiteBenefit != "")
				{
					double newBenefit = CostOfClicks * (stod(Percent) / 100) + stod(TotalWebsiteBenefit);
					RedisDel(PublisherTotalBenefit + HomeURL);
					RedisSadd(PublisherTotalBenefit + HomeURL, to_string(newBenefit));
				}
				else
				{
					double newBenefit = CostOfClicks * (stod(Percent) / 100);
					RedisSadd(PublisherTotalBenefit + HomeURL, to_string(newBenefit));
				}
				string TotalBenefit = RedisSmembersFirstOne(PublisherAllURLsBenfit + websiteID);
				if(TotalBenefit != "")
				{
					double newBenefit = CostOfClicks * (stod(Percent) / 100) + stod(TotalBenefit);
					RedisDel(PublisherAllURLsBenfit + websiteID);
					RedisSadd(PublisherAllURLsBenfit + websiteID, to_string(newBenefit));
				}
				else
				{
					int newBenefit = CostOfClicks * (stod(Percent) / 100);
					RedisSadd(PublisherAllURLsBenfit + websiteID, to_string(newBenefit));
				}
			}
//			RedisSadd(CollaborativePrefix + IPAddress + "_" + UserResolution + "_" + UserOS, BannerId);
		}
		RedisDel("mutex_click");
	}
	else
		Result = RedisSmembersFirstOne(BannerSite + BannerId);
	return Result;
}

string AdEngine::SendVerificationCode(string IPAddress, string UserResolution, string UserOS, string SiteURL, string BannerId, string QueryOrSize, string Mobile, string UserData)
{
	string RealUnReal = "";
	regex r("_| ");
	string HomeURL = ExtractRootURL(SiteURL);
	HomeURL = GetRawURL(HomeURL);
	UserOS = regex_replace(UserOS, r, "-");
	if(IsRealClick(SiteURL, IPAddress, UserResolution, BannerId, UserOS) == true)
		RealUnReal = "Real";
	else
		RealUnReal = "UnReal";
	
	SaveAdSenseClickLogtoRedis(IPAddress, UserResolution, UserOS, SiteURL, BannerId, QueryOrSize, RealUnReal, UserData);
	
	/////////////////Sending SMS////////////////////
	string Result = "";
	
	int Code = (rand() % 90000) + 10000;
	string strCode = "کد%20تایید:%20" + to_string(Code);
	string URL = "http://ip.sms.ir/SendMessage.ashx?user=09139610206&pass=84c527&text=" + strCode + "&to=" + Mobile + "&lineNo=30004505002814";
	string Token = RequestToWebservice(URL, "", "", "", "");
	RedisSet("smsresult", Token + "_" + URL);
	/////////////////////////////////////////////////
	
	if(RealUnReal == "Real" && HasEnoughCredit(BannerId))
	{
		while(true)
		{
			redisReply *rR = RedisSetWithFlag("mutex_click", "grabbed NX EX 60");
			if(rR != NULL && rR->str != NULL && string(rR->str) == "OK")
				break;
		}
		string tmpDailyAsset = RedisSmembersFirstOne(CampaignVariableDailyBudget + BannerId);
		string tmpTotalAsset = RedisSmembersFirstOne(CampaignTotalBudget + BannerId);
		string tmpCost = RedisSmembersFirstOne(ClickCost + BannerId);
		if(tmpDailyAsset != "" && tmpTotalAsset != "" && tmpCost != "")
		{
			double newDailyAsset = stod(tmpDailyAsset);
			double newTotalAsset = stod(tmpTotalAsset);
			double CostOfClicks = stod(tmpCost);
			newDailyAsset = newDailyAsset - CostOfClicks;
			newTotalAsset = newTotalAsset - CostOfClicks;
			RedisDel(CampaignVariableDailyBudget + BannerId);
			RedisDel(CampaignTotalBudget + BannerId);
			RedisSadd(CampaignVariableDailyBudget + BannerId, to_string(newDailyAsset));
			RedisSadd(CampaignTotalBudget + BannerId, to_string(newTotalAsset));
			Result = RedisSmembersFirstOne(BannerSite + BannerId);
			UpdateCheat(SiteURL, IPAddress, UserResolution, BannerId, UserOS);
			string Percent = RedisSmembersFirstOne(PublisherBenefitPercentage + HomeURL);
			string websiteID = RedisSmembersFirstOne("publisher_id_website_" + HomeURL);
			if(Percent != "" && websiteID != "")
			{
				string TotalWebsiteBenefit = RedisSmembersFirstOne(PublisherTotalBenefit + HomeURL);
				if(TotalWebsiteBenefit != "")
				{
					double newBenefit = CostOfClicks * (stod(Percent) / 100) + stod(TotalWebsiteBenefit);
					RedisDel(PublisherTotalBenefit + HomeURL);
					RedisSadd(PublisherTotalBenefit + HomeURL, to_string(newBenefit));
				}
				else
				{
					double newBenefit = CostOfClicks * (stod(Percent) / 100);
					RedisSadd(PublisherTotalBenefit + HomeURL, to_string(newBenefit));
				}
				string TotalBenefit = RedisSmembersFirstOne(PublisherAllURLsBenfit + websiteID);
				if(TotalBenefit != "")
				{
					double newBenefit = CostOfClicks * (stod(Percent) / 100) + stod(TotalBenefit);
					RedisDel(PublisherAllURLsBenfit + websiteID);
					RedisSadd(PublisherAllURLsBenfit + websiteID, to_string(newBenefit));
				}
				else
				{
					int newBenefit = CostOfClicks * (stod(Percent) / 100);
					RedisSadd(PublisherAllURLsBenfit + websiteID, to_string(newBenefit));
				}
			}
//			RedisSadd(CollaborativePrefix + IPAddress + "_" + UserResolution + "_" + UserOS, BannerId);
		}
		RedisDel("mutex_click");
	}
	else
		Result = RedisSmembersFirstOne(BannerSite + BannerId);
	return to_string(Code);
}

bool AdEngine::IsRegisteredWebsite(string URL, string whichService)
{
	bool isReg = RedisSismember(whichService, URL);
	if(isReg == true)
		return true;
	string newURL = URL;
	if(URL.length() > 8 && URL.substr(0, 8) == "https://")
	{
		if(URL.length() > 10 && URL[8] == 'w' && URL[9] == 'w' && URL[10] == 'w')
			newURL = newURL.substr(0, 8) + newURL.substr(12, newURL.npos);
		else
			newURL = newURL.insert(8, "www.");
	}
	else if(URL.substr(0, 7) == "http://")
	{
		if(URL.length() > 9 && URL[7] == 'w' && URL[8] == 'w' && URL[9] == 'w')
			newURL = newURL.substr(0, 7) + newURL.substr(11, newURL.npos);
		else
			newURL = newURL.insert(7, "www.");
	}
	isReg = RedisSismember(whichService, newURL);
	if(isReg == true)
		return true;
	return false;
}

string AdEngine::GetRawURL(string URL)
{
	string newURL = URL;
	if(URL.length() > 12 && URL.substr(0, 12) == "https://www.")
		newURL = newURL.substr(12, newURL.npos);
	else if(URL.length() > 11 && URL.substr(0, 11) == "http://www.")
		newURL = newURL.substr(11, newURL.npos);
	else if(URL.length() > 8 && URL.substr(0, 8) == "https://")
		newURL = newURL.substr(8, newURL.npos);
	else if(URL.length() > 7 && URL.substr(0, 7) == "http://")
		newURL = newURL.substr(7, newURL.npos);
	else if(URL.length() > 4 && URL.substr(0, 4) == "www.")
		newURL = newURL.substr(4, newURL.npos);
	string tmp = "";
	for(int i = 0; i < newURL.length(); i++)
		if(newURL[i] != '/' && newURL[i] != ':')
			tmp += newURL[i];
		else
			break;
	newURL = tmp;
	return newURL;
}

bool AdEngine::HasEnoughCredit(string BannerId)
{
	string dcre = RedisSmembersFirstOne(CampaignVariableDailyBudget + BannerId);
	if(dcre == "")
		BudgetReloading(BannerId);
	dcre = RedisSmembersFirstOne(CampaignVariableDailyBudget + BannerId);
	//string tcre = RedisSmembersFirstOne(CampaignTotalBudget + BannerId);
	string clickCost = RedisSmembersFirstOne(ClickCost + BannerId);
	double tcredit = 0, dcredit = 0, clickCost_ = 1;
//	if(tcre != "")
//		tcredit = stoi(tcre);
	if(dcre != "")
		dcredit = stod(dcre);
	if(clickCost != "")
		clickCost_ = stod(clickCost);
	if(dcredit < clickCost_)
		return false;
	return true;
}

void AdEngine::FetchPendingWebpages(int ListID, string apiAddress)
{
	redisReply *pending = RedisSmembers(PendingWebsitesLists + to_string(ListID));
	if(pending == NULL || pending->elements == 0)
		return;
	int i = 0;
	while(i < pending->elements)
	{
		string URL = ConvertRedisFormattoURL(pending->element[i]->str);
		bool Status = false;
		if(!RedisSismember(CrawledWebpages, pending->element[i]->str))
		{
			
			Status = Elasticsearch_SaveSiteContents(URL, apiAddress);
			cout<<"Website Saved Successfully, list # " + to_string(ListID) + "..."<<endl;
			if(Status == true)
			{
				RedisSrem(PendingWebsitesLists + to_string(ListID), pending->element[i]->str);
				RedisSrem(PendingWebsites, pending->element[i]->str);
			}
		}
		else
		{
			string URLFetchDate = Elasticsearch_GetTimeofRetrievingWebpage(URL);
			cout<<"Website reloaded, list # " + to_string(ListID) + "..."<<endl;
			redisReply * AllCampaigns = RedisKeys(ClickCost + "*");
			if(AllCampaigns != NULL)
			{
				for(int k = 0; k < AllCampaigns->elements; k++)
				{
					string prefix = "campaign_activate_date_";
                                        string Campaign = string(AllCampaigns->element[k]->str).substr(ClickCost.length());
					string CampaignInitiateDate = RedisSmembersFirstOne(prefix + Campaign);
					if(OccuredAfter(URLFetchDate, CampaignInitiateDate))
					{
						Elasticsearch_UpdateCampaignForURL(URL, Campaign);
					}
				}
			}
			RedisSrem(PendingWebsitesLists + to_string(ListID), pending->element[i]->str);
			RedisSrem(PendingWebsites, pending->element[i]->str);
		}
		i++;
	}
}


bool AdEngine::OccuredAfter(string FirstTime, string AfterTime)
{
	//yyyy-MM-ddHH:mm:ss
	if(FirstTime.length() != 18 || AfterTime.length() != 18)
		return false;
	int FYear = stoi(FirstTime.substr(0, 4));
	int FMonth = stoi(FirstTime.substr(5, 2));
	int FDay = stoi(FirstTime.substr(8, 2));
	int FHour = stoi(FirstTime.substr(10, 2));
	int FMinute = stoi(FirstTime.substr(13, 2));
	int FSec = stoi(FirstTime.substr(16, 2));
	int AYear = stoi(AfterTime.substr(0, 4));
	int AMonth = stoi(AfterTime.substr(5, 2));
	int ADay = stoi(AfterTime.substr(8, 2));
	int AHour = stoi(AfterTime.substr(10, 2));
	int AMinute = stoi(AfterTime.substr(13, 2));
	int ASec = stoi(AfterTime.substr(16, 2));
	if(FYear < AYear)
		return true;
	else if(FYear == AYear)
	{
		if(FMonth < AMonth)
			return true;
		else if(FMonth == AMonth)
		{
			if(FDay < ADay)
				return true;
			else if(FDay == ADay)
			{
				if(FHour < AHour)
					return true;
				else if(FHour == AHour)
				{
					if(FMinute < AMinute)
						return true;
					else if(FMinute == AMinute)
					{
						if(FSec < ASec)
							return true;
					}
				}
			}
		}
	}
	return false;
}


void AdEngine::SaveAdSenseShowLogtoRedis(string IPAddress, string UserResolution, string UserOS, string SiteURL, string BannerId, string Size)
{
	string res = RedisGet(ShowAdSenseLogCount);
	regex r("_| ");
	UserResolution = regex_replace(UserResolution, r, "-");
	UserOS = regex_replace(UserOS, r, "-");
	Size = regex_replace(Size, r, "-");
	SiteURL = regex_replace(SiteURL, r, "-");
	int counter = 0;
	if(res != "")
		counter = stoi(res);
	counter++;
	time_t tmp = time(nullptr);
	tm *currTime = localtime(&tmp);
	string Day = to_string(currTime->tm_mday), Month = to_string(currTime->tm_mon + 1);
	string Hour = to_string(currTime->tm_hour), Min = to_string(currTime->tm_min);
	string Sec = to_string(currTime->tm_sec), Year = to_string(currTime->tm_year + 1900);

	if(BannerId != "")
		UpdateCounterShowLog(GetRawURL(ExtractRootURL(SiteURL)), BannerId, Size, Hour, Day, Month, Year);

	Day = string(2 - Day.length(), '0') + Day;
	Hour = string(2 - Hour.length(), '0') + Hour;
	Month = string(2 - Month.length(), '0') + Month;
	Min = string(2 - Min.length(), '0') + Min;
	Sec = string(2 - Sec.length(), '0') + Sec;
	string RequestTime = Year + "-" + Month + "-" + Day + Hour + ":" + Min + ":" + Sec;
	
	
//	double now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
//	string RequestTime = to_string(now);
	
	string LogKey = ShowAdSenseLog + to_string(counter);
	string LogValue = IPAddress + "_" + UserResolution + "_" + UserOS + "_" + SiteURL + "_" + BannerId + "_" + RequestTime + "_" + Size;
//	RedisSet(LogKey, LogValue);
//	RedisSet(ShowAdSenseLogCount, to_string(counter));
}

void AdEngine::SaveAdSenseClickLogtoRedis(string IPAddress, string UserResolution, string UserOS, string SiteURL, string BannerId, string Size, string RealUnReal, string UserData)
{
	string res = RedisGet(ClickAdSenseLogCount);
	regex r("_| ");
	UserResolution = regex_replace(UserResolution, r, "-");
	UserOS = regex_replace(UserOS, r, "-");
	Size = regex_replace(Size, r, "-");
	SiteURL = regex_replace(SiteURL, r, "-");
	int counter = 0;
	if(res != "")
		counter = stoi(res);
	counter++;
	time_t tmp = time(nullptr);
	tm *currTime = localtime(&tmp);
	string Day = to_string(currTime->tm_mday), Month = to_string(currTime->tm_mon + 1);
	string Hour = to_string(currTime->tm_hour), Min = to_string(currTime->tm_min);
	string Sec = to_string(currTime->tm_sec), Year = to_string(currTime->tm_year + 1900);
	if(BannerId != "")
		UpdateCounterClickLog(GetRawURL(ExtractRootURL(SiteURL)), BannerId, Size, Hour, Day, Month, Year);

	Day = string(2 - Day.length(), '0') + Day;
	Hour = string(2 - Hour.length(), '0') + Hour;
	Month = string(2 - Month.length(), '0') + Month;
	Min = string(2 - Min.length(), '0') + Min;
	Sec = string(2 - Sec.length(), '0') + Sec;
	string RequestTime = Year + "-" + Month + "-" + Day + Hour + ":" + Min + ":" + Sec;
	
//	double now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
//	string RequestTime = to_string(now);
	
	string LogKey = ClickAdSenseLog + to_string(counter);
	string LogValue = IPAddress + "_" + UserResolution + "_" + UserOS + "_" + SiteURL + "_" + BannerId + "_" + RequestTime + "_" + Size + "_" + UserData + "_" + RealUnReal;
	RedisSet(LogKey, LogValue);
	RedisSet(ClickAdSenseLogCount, to_string(counter));
}

void AdEngine::SaveAdWordsShowLogtoRedis(string IPAddress, string UserResolution, string UserOS, string SiteURL, string BannerId, string UserQuery)
{
	string res = RedisGet(ShowAdWordsLogCount);
	regex r("_| ");
	UserResolution = regex_replace(UserResolution, r, "-");
	UserOS = regex_replace(UserOS, r, "-");
	UserQuery = regex_replace(UserQuery, r, "-");
	SiteURL = regex_replace(SiteURL, r, "-");
	int counter = 0;
	if(res != "")
		counter = stoi(res);
	counter++;
	time_t tmp = time(nullptr);
	tm *currTime = localtime(&tmp);
	string Day = to_string(currTime->tm_mday), Month = to_string(currTime->tm_mon + 1);
	string Hour = to_string(currTime->tm_hour), Min = to_string(currTime->tm_min);
	string Sec = to_string(currTime->tm_sec), Year = to_string(currTime->tm_year + 1900);
	if(BannerId != "")
		UpdateCounterShowLog(GetRawURL(ExtractRootURL(SiteURL)), BannerId, "AdWords", Hour, Day, Month, Year);

	Day = string(2 - Day.length(), '0') + Day;
	Hour = string(2 - Hour.length(), '0') + Hour;
	Month = string(2 - Month.length(), '0') + Month;
	Min = string(2 - Min.length(), '0') + Min;
	Sec = string(2 - Sec.length(), '0') + Sec;
	string RequestTime = Year + "-" + Month + "-" + Day + Hour + ":" + Min + ":" + Sec;
	
//	double now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
//	string RequestTime = to_string(now);
	string LogKey = ShowAdWordsLog + to_string(counter);
	string LogValue = IPAddress + "_" + UserResolution + "_" + UserOS + "_" + SiteURL + "_" + BannerId + "_" + RequestTime + "_" + UserQuery;
	RedisSet(LogKey, LogValue);
	RedisSet(ShowAdWordsLogCount, to_string(counter));
}

void AdEngine::SaveAdWordsClickLogtoRedis(string IPAddress, string UserResolution, string UserOS, string SiteURL, string BannerId, string UserQuery, string RealUnReal)
{
	string res = RedisGet(ClickAdWordsLogCount);
	regex r("_| ");
	UserResolution = regex_replace(UserResolution, r, "-");
	UserOS = regex_replace(UserOS, r, "-");
	UserQuery = regex_replace(UserQuery, r, "-");
	SiteURL = regex_replace(SiteURL, r, "-");
	int counter = 0;
	if(res != "")
		counter = stoi(res);
	counter++;
	time_t tmp = time(nullptr);
	tm *currTime = localtime(&tmp);
	string Day = to_string(currTime->tm_mday), Month = to_string(currTime->tm_mon + 1);
	string Hour = to_string(currTime->tm_hour), Min = to_string(currTime->tm_min);
	string Sec = to_string(currTime->tm_sec), Year = to_string(currTime->tm_year + 1900);

	if(BannerId != "")
		UpdateCounterClickLog(GetRawURL(ExtractRootURL(SiteURL)), BannerId, "AdWords", Hour, Day, Month, Year);

	Day = string(2 - Day.length(), '0') + Day;
	Hour = string(2 - Hour.length(), '0') + Hour;
	Month = string(2 - Month.length(), '0') + Month;
	Min = string(2 - Min.length(), '0') + Min;
	Sec = string(2 - Sec.length(), '0') + Sec;
	string RequestTime = Year + "-" + Month + "-" + Day + Hour + ":" + Min + ":" + Sec;
	
//	double now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
//	string RequestTime = to_string(now);
	
	string LogKey = ClickAdWordsLog + to_string(counter);
	string LogValue = IPAddress + "_" + UserResolution + "_" + UserOS + "_" + SiteURL + "_" + BannerId + "_" + RequestTime + "_" + UserQuery + "__" + RealUnReal;
	RedisSet(LogKey, LogValue);
	RedisSet(ClickAdWordsLogCount, to_string(counter));
}


void AdEngine::UpdateCounterShowLog(string URL, string Campaign, string Size, string Hour, string Day, string Month, string Year)
{
	while(true)
	{
		redisReply *rR = RedisSetWithFlag("mutex_update_show_counter", "grabbed NX EX 60");
		if(rR != NULL && rR->str != NULL && string(rR->str) == "OK")
			break;
	}
	string WebsiteID = RedisSmembersFirstOne(WebsiteToID + URL);
	string counterLog = "counterShowLog_" + WebsiteID + "_" + Campaign + "_" + Size + "_" + Hour + "_" + Day + "_" + Month + "_" + Year;
	string Counter = RedisGet(counterLog);
	if(Counter == "")
		Counter = "1";
	else
		Counter = to_string(stoi(Counter) + 1);
	RedisDel(counterLog);
	RedisSet(counterLog, Counter);
	RedisDel("mutex_update_show_counter");
}
void AdEngine::UpdateCounterClickLog(string URL, string Campaign, string Size, string Hour, string Day, string Month, string Year)
{
	while(true)
	{
		redisReply *rR = RedisSetWithFlag("mutex_update_click_counter", "grabbed NX EX 60");
		if(rR != NULL && rR->str != NULL && string(rR->str) == "OK")
			break;
	}
	string WebsiteID = RedisSmembersFirstOne(WebsiteToID + URL);
	string counterLog = "counterClickLog_" + WebsiteID + "_" + Campaign + "_" + Size + "_" + Hour + "_" + Day + "_" + Month + "_" + Year;
	string Counter = RedisGet(counterLog);
	if(Counter == "")
		Counter = "1";
	else
		Counter = to_string(stoi(Counter) + 1);
	RedisDel(counterLog);
	RedisSet(counterLog, Counter);
	RedisDel("mutex_update_click_counter");
}
bool AdEngine::InsertToMysql(string Table, string WebsiteID, string CampaignID, string Size, string Hour, string Day, string Month, string Year, string Counter, string ShowMysqlIP, string ClickMysqlIP)
{
	/*if(CampaignID == "")
		CampaignID = "-1";
	try {
		sql::Driver *driver;
		sql::Connection *con;
		sql::Statement *stmt;

		 Create a connection 
		driver = get_driver_instance();
		driver->threadInit();
		//A<~*8u7-
		con = driver->connect(MysqlIP, "root", "A<~*8u7-");
		/* Connect to the MySQL test database
		con->setSchema("advertiser");
		
		Hour = string(2 - Hour.length(), '0') + Hour;
		Month = string(2 - Month.length(), '0') + Month;
		Day = string(2 - Day.length(), '0') + Day;
		string RequestTime = Year + "-" + Month + "-" + Day + " " + Hour + ":00:00";
		
		string Query = "";
		if(Table == "ad_show_counter")
		{
			if(Size == "AdWords")
				Query = "INSERT INTO " + Table + "(ad_show_publisher_id, ad_show_campaign_id, ad_show_date_hour, ad_show_date_day, ad_show_date_month, ad_show_date_year, ad_show_counter, ad_show_date) VALUES (" + 
					WebsiteID + ", " + CampaignID + ", " + Hour + ", " + Day + ", " + Month + ", " + Year + ", " + Counter + ",'" + RequestTime + "')";
			else
				Query = "INSERT INTO " + Table + "(ad_show_publisher_id, ad_show_campaign_id, ad_show_banner_size, ad_show_date_hour, ad_show_date_day, ad_show_date_month, ad_show_date_year, ad_show_counter, ad_show_date) VALUES (" + 
					WebsiteID + ", " + CampaignID + ", '" + Size + "', " + Hour + ", " + Day + ", " + Month + ", " + Year + ", " + Counter + ",'" + RequestTime + "')";
		}
		else if(Table == "ad_click_counter")
		{
			if(Size == "AdWords")
				Query = "INSERT INTO " + Table + "(ad_click_publisher_id, ad_click_campaign_id, ad_click_date_hour, ad_click_date_day, ad_click_date_month, ad_click_date_year, ad_click_counter, ad_click_date) VALUES (" + 
					WebsiteID + ", " + CampaignID + ", " + Hour + ", " + Day + ", " + Month + ", " + Year + ", " + Counter + ",'" + RequestTime + "')";
			else
				Query = "INSERT INTO " + Table + "(ad_click_publisher_id, ad_click_campaign_id, ad_click_banner_size, ad_click_date_hour, ad_click_date_day, ad_click_date_month, ad_click_date_year, ad_click_counter, ad_click_date) VALUES (" + 
					WebsiteID + ", " + CampaignID + ", '" + Size + "', " + Hour + ", " + Day + ", " + Month + ", " + Year + ", " + Counter + ",'" + RequestTime + "')";
		}
		stmt = con->createStatement();
		stmt->execute((sql::SQLString)Query);
		stmt->close();
		delete stmt;
		con->close();
		delete con;
		driver->threadEnd();

	} catch (sql::SQLException &e) {
		string s = e.what();
		return false;
//		cout<<s;
	}
	return true;*/
	if(CampaignID == "" || CampaignID == "NoBanner" || CampaignID.length() > 4)
		return true;
	try {

		string tmpHour = string(2 - Hour.length(), '0') + Hour;
		string tmpMonth = string(2 - Month.length(), '0') + Month;
		string tmpDay = string(2 - Day.length(), '0') + Day;
		string RequestTime = Year + "-" + tmpMonth + "-" + tmpDay + " " + tmpHour + ":00:00";
		string Query = "", Res = "";

		if(Table == "ad_show_counter")
		{
			if(Size == "AdWords")
				Query = Query + "{\"ad_show_publisher_id\" : " + WebsiteID + ", " +
					"\"ad_show_campaign_id\" : " + CampaignID + ", " +
					"\"ad_show_date_hour\" : " + Hour + ", " +
					"\"ad_show_date_day\" : " + Day + ", " +
					"\"ad_show_date_month\" : " + Month + ", " +
					"\"ad_show_date_year\" : " + Year + ", " +
					"\"ad_show_counter\" : " + Counter + ", " +
					"\"ad_show_date\" : \"" + RequestTime + "\"}";
			else
				Query = Query + "{\"ad_show_publisher_id\" : " + WebsiteID + ", " +
					"\"ad_show_campaign_id\" : " + CampaignID + ", " +
					"\"ad_show_banner_size\" : \"" + Size + "\", " +
					"\"ad_show_date_hour\" : " + Hour + ", " +
					"\"ad_show_date_day\" : " + Day + ", " +
					"\"ad_show_date_month\" : " + Month + ", " +
					"\"ad_show_date_year\" : " + Year + ", " +
					"\"ad_show_counter\" : " + Counter + ", " +
					"\"ad_show_date\" : \"" + RequestTime + "\"}";
			Res = RequestToWebservice(ShowMysqlIP, Query, "", "Content-Type: application/json", "");
		}
		else if(Table == "ad_click_counter")
		{
			if(Size == "AdWords")
				Query = Query + "{\"ad_click_publisher_id\" : " + WebsiteID + ", " +
					"\"ad_click_campaign_id\" : " + CampaignID + ", " +
					"\"ad_click_date_hour\" : " + Hour + ", " +
					"\"ad_click_date_day\" : " + Day + ", " +
					"\"ad_click_date_month\" : " + Month + ", " +
					"\"ad_click_date_year\" : " + Year + ", " +
					"\"ad_click_counter\" : " + Counter + ", " +
					"\"ad_click_date\" : \"" + RequestTime + "\"}";
			else
				Query = Query + "{\"ad_click_publisher_id\" : " + WebsiteID + ", " +
					"\"ad_click_campaign_id\" : " + CampaignID + ", " +
					"\"ad_click_banner_size\" : \"" + Size + "\", " +
					"\"ad_click_date_hour\" : " + Hour + ", " +
					"\"ad_click_date_day\" : " + Day + ", " +
					"\"ad_click_date_month\" : " + Month + ", " +
					"\"ad_click_date_year\" : " + Year + ", " +
					"\"ad_click_counter\" : " + Counter + ", " +
					"\"ad_click_date\" : \"" + RequestTime + "\"}";
			Res = RequestToWebservice(ClickMysqlIP, Query, "", "Content-Type: application/json", "");
		}
		regex r("yes");
		smatch sm;
		bool b = regex_search(Res, sm, r);
		if (b)
			return true;
		else
		{
			RedisSaddNoSpace("norequests", Query);
			return false;
		}

	} catch (sql::SQLException &e) {
		string s = e.what();
		return false;
//		cout<<s;
	}
	return true;
}
void AdEngine::InsertCounterLogsToMysql(string ShowMysqlIP, string ClickMysqlIP)
{
	redisReply *reply = RedisKeys("counterShowLog_*");
	if(reply != NULL)
	{
		for(int i = 0; i < reply->elements; i++)
		{
			string key = reply->element[i]->str;
			string value = RedisGet(reply->element[i]->str);
			list<string> counterLog = strSplit(key, '_');
			//drop counterShowLog_ string
			counterLog.pop_back();
			string WebId = counterLog.back();
			counterLog.pop_back();
			string CampId = counterLog.back();
			counterLog.pop_back();
			string Size = counterLog.back();
			counterLog.pop_back();
			string Hour = counterLog.back();
			counterLog.pop_back();
			string Day = counterLog.back();
			counterLog.pop_back();
			string Month = counterLog.back();
			counterLog.pop_back();
			string Year = counterLog.back();
			counterLog.pop_back();
			bool IsSuccess = InsertToMysql("ad_show_counter", WebId, CampId, Size, Hour, Day, Month, Year, value, ShowMysqlIP, ClickMysqlIP);
			if(IsSuccess == true)
				RedisDel(key);
		}
	}
	reply = RedisKeys("counterClickLog_*");
	if(reply != NULL)
	{
		for(int i = 0; i < reply->elements; i++)
		{
			string key = reply->element[i]->str;
			string value = RedisGet(reply->element[i]->str);
			list<string> counterLog = strSplit(key, '_');
			counterLog.pop_back();
			string WebId = counterLog.back();
			counterLog.pop_back();
			string CampId = counterLog.back();
			counterLog.pop_back();
			string Size = counterLog.back();
			counterLog.pop_back();
			string Hour = counterLog.back();
			counterLog.pop_back();
			string Day = counterLog.back();
			counterLog.pop_back();
			string Month = counterLog.back();
			counterLog.pop_back();
			string Year = counterLog.back();
			counterLog.pop_back();
			bool IsSuccess = InsertToMysql("ad_click_counter", WebId, CampId, Size, Hour, Day, Month, Year, value, ShowMysqlIP, ClickMysqlIP);
			if(IsSuccess)
				RedisDel(key);
		}
	}
}




string AdEngine::ConvertURLtoRedisFormat(string URL)
{
	regex r("%");
	string s = regex_replace(URL, r, "**");
	return s;
}

string AdEngine::ConvertRedisFormattoURL(string RedisFormat)
{
	regex r("\\*\\*");
	string s = regex_replace(RedisFormat, r, "%");
	return s;
}

string AdEngine::GetBannerSite(string BannerID)
{
	string Key = BannerSite + BannerID;
	string Site = RedisSmembersFirstOne(Key);
	return Site;
}

string AdEngine::HTMLToContent(string HTML)
{
	regex r1("<body");
	smatch sm;
	int st = 0;
	bool b = regex_search(HTML, sm, r1);
	if(b)
		st = sm.position(0);
	HTML = HTML.substr(st, HTML.length());
	r1.assign("\r\n");
	string Res = HTML;
	Res = regex_replace(Res, r1, " ");
	int k = Res.length();
	
	regex r2("\n");
	Res = regex_replace(Res, r2, " ");
	k = Res.length();
	
	regex r3("\r");
	Res = regex_replace(Res, r3, " ");
	k = Res.length();
	
	regex r4("\t");
	Res = regex_replace(Res, r4, " ");
	k = Res.length();
	
	r4.assign("( +)");
	Res = regex_replace(Res, r4, " ");
	k = Res.length();
	////////////////
	
//	regex r111("(<a.*?</a>)");
//	Res = regex_replace(Res,r111, " ");
//	k = Res.length();
//	regex r122("<script.*?</script>");
//	Res = regex_replace(Res,r122, " ");
//	k = Res.length();
//	regex r113("<ul.*?</ul>");
//	Res = regex_replace(Res,r113, " ");
//	k = Res.length();
	/////////////////
//	regex r115("(<!--.*?-->)");
//	Res = regex_replace(Res, r115, " ");
//	k = Res.length();
	
	regex r6("(،)|(%)|(})|(\\|)|(\\{)|([)|(])");
	Res = regex_replace(Res, r6, " ");
	k = Res.length();
	
//	regex r9("(<li.*?</li>)");
//	Res = regex_replace(Res, r9, " ");
//	k = Res.length();
	
//	regex r10("(<h\\d.*?</h\\d>)");
//	Res = regex_replace(Res, r10, " ");
//	k = Res.length();
	
//	regex r11("(<footer.*?</footer>)");
//	Res = regex_replace(Res, r11, " ");
//	k = Res.length();
//	
//	regex r12("(<script.*?</script>)");
//	Res = regex_replace(Res, r12, " ");
//	k = Res.length();
	
//	regex r13("(<header>.*?</header>)");
//	Res = regex_replace(Res, r13, " ");
//	k = Res.length();
	
	regex r14("( )( )+|(\t+)");
	Res = regex_replace(Res, r14, " ");
	k = Res.length();
	
//	regex r15("(<h\\d.*?</h\\d>)");
//	Res = regex_replace(Res, r15, " ");
//	k = Res.length();
	
//	regex r7("<head.*?</head>");
//	Res = regex_replace(Res, r7, " ");
//	k = Res.length();
	
//	regex r16("([a-zA-Z0-9])");
//	Res = regex_replace(Res, r16, "");
//	k = Res.length();
	
	r14.assign("(=|\"|-|>|<|/|:|;|_|\\!|'|\\(|\\)|\\*|،|,|\\(|\\)|\\&|\\$|\\+|\\.|#)");
	Res = regex_replace(Res, r14, "");
	k = Res.length();

	
	
	r14.assign("( +)|(\t+)");
	Res = regex_replace(Res, r14, " ");
	k = Res.length();
	
	return Res;
}

string AdEngine::ExtractRootURL(string SiteURL)
{
	regex r("http(s?)://(.*?)/");
	smatch Res;
	regex_search(SiteURL, Res, r);
	if(Res[0] != "")
		return Res[0];
	else
		return SiteURL;
}

string AdEngine::GetOS(string UserAgent)
{
	regex os("\\(.*?\\)");
	smatch sm;
	regex_search(UserAgent, sm, os);
	string s = sm[0];
	regex win("Windows");
	regex linux("Linux");
	regex iPhone("iPhone");
	regex android("Android");
	regex mac("Macintosh");
	regex iPad("iPad");
	regex mobile("Mobile");
	
	if(regex_search(s, sm, iPad))
		return "iPad";
	if(regex_search(s, sm, mac))
		return "Mac";
	if(regex_search(s, sm, iPhone))
		return "iPhone";
	else if(regex_search(s, sm, android))
		if(regex_search(UserAgent, sm, mobile))
			return "Android";
		else
			return "Tablet";
	else if(regex_search(s, sm, win))
		return "Windows";
	else if(regex_search(s, sm, linux))
		return "Linux";
	return "";
}

void AdEngine::BudgetReloading(bool status)
{
	redisReply *allCampaigns = RedisKeys(CampaignTotalBudget + "*");
	int l = 0;
	if(allCampaigns != NULL && allCampaigns->elements > 0)
		l = allCampaigns->elements;
	for(int i = 0 ; i < l; i++)
	{
		string banner = string(allCampaigns->element[i]->str).substr(CampaignTotalBudget.length(), string(allCampaigns->element[i]->str).length());
		string total = RedisSmembersFirstOne(CampaignTotalBudget + banner);
		string vdaily = RedisSmembersFirstOne(CampaignVariableDailyBudget + banner);
		string cdaily = RedisSmembersFirstOne(CampaignConstantDailyBudget + banner);
		//status = true, Now is the end of day, all daily budgets must be reloaded
		if(status == true)
		{
			vdaily = "";	
			if(total != "" && cdaily != "")
			{
				if(stod(total) > stod(cdaily))
					vdaily = cdaily;
				else
					vdaily = total;
				RedisDel(CampaignVariableDailyBudget + banner);
				redisReply *checkSuccess = RedisSadd(CampaignVariableDailyBudget + banner, vdaily);
				if(checkSuccess != NULL)
				{
					time_t tmp = time(nullptr);
					tm *currTime = localtime(&tmp);
					int cday = currTime->tm_yday;
					RedisSet("LastBudgetUpdate", to_string(cday));
				}
			}
			
		}
		//this is the first run of offline module. Existing vdaily variables should not be altered
		else
		{
			if((vdaily == ""))
			{
				if(total != "" && cdaily != "")
				{
					if(stod(total) > stod(cdaily))
						vdaily = cdaily;
					else
						vdaily = total;
				}
				else
					vdaily = "0";

				RedisDel(CampaignVariableDailyBudget + banner);
				redisReply *checkSuccess = RedisSadd(CampaignVariableDailyBudget + banner, vdaily);
				if(checkSuccess != NULL)
				{
					time_t tmp = time(nullptr);
					tm *currTime = localtime(&tmp);
					int cday = currTime->tm_yday;
					RedisSet("LastBudgetUpdate", to_string(cday));
				}
			}
		}
	}
}

void AdEngine::BudgetReloading(string CampaignID)
{
	string S = RedisSmembersFirstOne(CampaignVariableDailyBudget + CampaignID);
	if(S == "")
	{
		string banner = CampaignID;
		string total = RedisSmembersFirstOne(CampaignTotalBudget + banner);
		string vdaily = "";
		string cdaily = RedisSmembersFirstOne(CampaignConstantDailyBudget + banner);
		if(total != "" && cdaily != "")
		{
			if(stod(total) > stod(cdaily))
				vdaily = cdaily;
			else
				vdaily = total;
		}
		else
			vdaily = "0";
		RedisDel(CampaignVariableDailyBudget + banner);
		RedisSadd(CampaignVariableDailyBudget + banner, vdaily);
	}
}

string AdEngine::Normalizer(string Entry)
{
	regex r("[ًٌٍَُِّْٰٖٓٔـۖۚٴ]+");
        // Remove Useless Characters
        string text = regex_replace(Entry, r, "");
	r.assign("[\u200b\u200d\u202b\u202c\u202e\u202d\ufeff\ufe0f]+");
        text = regex_replace(text, r, "");
        // Unify Different Half Distance, Space, and New Line Characters
	r.assign("[\u200c\u00ac\u200f\u200e\u202a\u009d\u2029\u0086\u0097\u0090\u0093\u0098\u009e\u206f\u206d]+|(&zwnj;)+");
        text = regex_replace(text, r, "\xE2\x80\x8C");
	r.assign("[\r\n]+");
        text = regex_replace(text, r, "\n");
        
        // Unify Alphabet Characters
	r.assign("[ﺍﺎٱ]");
        text = regex_replace(text, r, "ا");
	r.assign("[ٱﺁ]");
        text = regex_replace(text, r, "آ");
	r.assign("[ﺏﺐﺒﺑ]");
        text = regex_replace(text, r, "ب");
	r.assign("[ﭙﭘﭗ]");
        text = regex_replace(text, r, "پ");
	r.assign("[ﺕﺗﺖﺘ]");
        text = regex_replace(text, r, "ت");
	r.assign("[ﺚﺛﺜ]");
        text = regex_replace(text, r, "ث");
	r.assign("[ﺞﺠﺟﺝ]");
        text = regex_replace(text, r, "ج");
	r.assign("[ﭻﭽﭼ]");
        text = regex_replace(text, r, "چ");
	r.assign("[ﺤﺣﺢ]");
        text = regex_replace(text, r, "ح");
	r.assign("[ﺨﺧﺦ]");
        text = regex_replace(text, r, "خ");
	r.assign("[ﺩﺪ]");
        text = regex_replace(text, r, "د");
	r.assign("[ﺬﺫ]");
        text = regex_replace(text, r, "ذ");
	r.assign("[ﺭﺮ]");
        text = regex_replace(text, r, "ر");
	r.assign("[ﺰﺯ]");
        text = regex_replace(text, r, "ز");
	r.assign("[ﮊ]");
        text = regex_replace(text, r, "ژ");
	r.assign("[ﺲﺱﺴﺳ]");
        text = regex_replace(text, r, "س");
	r.assign("[ﺵﺶﺸﺷ]");
        text = regex_replace(text, r, "ش");
	r.assign("[ﺺﺼﺻ]");
        text = regex_replace(text, r, "ص");
	r.assign("[ﺿﻀﺽ]");
        text = regex_replace(text, r, "ض");
	r.assign("[ﻂﻄﻃ]");
        text = regex_replace(text, r, "ط");
	r.assign("[ﻈﻇ]");
        text = regex_replace(text, r, "ظ");
	r.assign("[ﻊﻌﻋﻉ]");
        text = regex_replace(text, r, "ع");
	r.assign("[ﻎﻐﻏﻍ]");
        text = regex_replace(text, r, "غ");
	r.assign("[ﻑﻒﻔﻓ]");
        text = regex_replace(text, r, "ف");
	r.assign("[ﻕﻖﻘﻗ]");
        text = regex_replace(text, r, "ق");
	r.assign("[ﻜﻛﮎﮏﮑﮐكڪﻚګ]");
        text = regex_replace(text, r, "ک");
	r.assign("[ﮓﮒﮕﮔ]");
        text = regex_replace(text, r, "گ");
	r.assign("[ﻝﻞﻠﻟ]");
        text = regex_replace(text, r, "ل");
	r.assign("[ﻡﻢﻤﻣ]");
        text = regex_replace(text, r, "م");
	r.assign("[ﻦﻥﻨﻧ]");
        text = regex_replace(text, r, "ن");
	r.assign("[ۆﻭﻮۊ]");
        text = regex_replace(text, r, "و");
	r.assign("[ەھﻬﻩﻫﻪﮤۀةہ]");
        text = regex_replace(text, r, "ه");
	r.assign("[ﻱﻲﻯﻴﻰﻳﯼﯽﯾﯿيىےێې]");
        text = regex_replace(text, r, "ی");
	r.assign("ﻻ|ﻼ");
        text = regex_replace(text, r, "لا");
        return text;
}

list<string> AdEngine::GetRootQuery(string Query, string apiAddress)
{
	string newQueryJson = RequestToWebservice(apiAddress, "{\"text\":\"" + Query + "\"}", "",
		"Content-Type: application/json", "");
	string newQuery = "";
	json_error_t error;
	json_t *root = json_loads(newQueryJson.c_str(), 0, &error);
	if(!json_is_object(root))
		newQuery = " " + Query + " ";
	else
	{		
		json_t * status = json_object_get(root, "status");
		if(json_is_string(status))
		{
			string st = json_string_value(status);
			if(st == "yes")
			{
				json_t * text = json_object_get(root, "body");
				if(json_is_string(text))
					newQuery = json_string_value(text);
			}
			else
				newQuery = " " + Query + " ";
		}
		else
			newQuery = " " + Query + " ";
	}
	list<string> Result;
	redisReply *res = RedisKeys(CampaignsForKeywordPrefix + "*");
	for (int i = 0; i < res->elements; i++) {
		string elem = string(res->element[i]->str).substr(CampaignsForKeywordPrefix.length(), string(res->element[i]->str).npos);
		regex r("-");
		elem = regex_replace(elem, r, " ");
		elem = " " + elem + " ";
		r.assign(elem);
		smatch sm;
		bool b = regex_search(newQuery, sm, r);
		if (b)
			Result.push_back(string(res->element[i]->str));
	}
	return Result;
}