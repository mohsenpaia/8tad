/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: rera
 *
 * Created on April 16, 2017, 3:00 PM
 */

#include <cstdlib>
#include <curl/curl.h>
#include <unistd.h>
#include <thread>

#include "../AdEngine/AdEngine.hpp"

using namespace std;

/*
 * 
 */

AdEngine AE("not-vm");

void CheckExistence()
{
	time_t tmp = time(nullptr);
	tm *currTime = localtime(&tmp);
	int day = currTime->tm_yday;
	int Hour = currTime->tm_hour;
	int Minute = currTime->tm_min;
	string LastUpdate = AE.RedisGet("LastBudgetUpdate");
	if(LastUpdate == "")
		AE.RedisSet("LastBudgetUpdate", to_string(day));
	LastUpdate = AE.RedisGet("LastMysqlUpdate");
	if(LastUpdate == "")
		AE.RedisSet("LastMysqlUpdate", to_string(Hour));
	LastUpdate = AE.RedisGet("LastCheatUpdate");
	if(LastUpdate == "")
		AE.RedisSet("LastCheatUpdate", to_string(Minute));
}

int main(int argc, char** argv)
{
//	string SW = "false";
//	bool SWitch = false;
//	if(argv[1] != NULL)
//	{
//		SW = argv[1];
//		if(SW == "true")
//		{
//			cout << "mode: update all budgets: " + SW + "\n";
//			SWitch = true;
//		}
//	}
//	AdEngine AE;
	CheckExistence();
	time_t tmp = time(nullptr);
	tm *currTime = localtime(&tmp);
	int day = currTime->tm_yday;
	int Hour = currTime->tm_hour;
	int Minute = currTime->tm_min;
	//AE.BudgetReloading(true, SW);
	cout<<"Starting offline processes..."<<endl;
//	while(true)
//	{
		if(AE.Elasticsearch_CheckExistence(AE.ElasticLogIndex) == false)
			AE.Elasticsearch_Initialize();
		AE.Elasticsearch_Update();
	
		tmp = time(nullptr);
		currTime = localtime(&tmp);
		int cday = currTime->tm_yday;
		int lday = cday;
		string LastUpdate = AE.RedisGet("LastBudgetUpdate");
		if(LastUpdate != "")
			lday = stoi(LastUpdate);
		if(lday != cday)
		{
			AE.RedisRemoveObsoleteKeys();
			AE.BudgetReloading(true);
			day = cday;
		}
		LastUpdate = AE.RedisGet("LastMysqlUpdate");
		Minute = currTime->tm_min;
		if(LastUpdate != "")
			Minute = stoi(LastUpdate);
		int cmin = currTime->tm_min;
		if(cmin != Minute)
		{
//			string MysqlIP = "tcp://127.0.0.1:3306";
			string ShowMysqlIP = "http://127.0.0.1:2222/reports/api/show/counter";
			string ClickMysqlIP = "http://127.0.0.1:2222/reports/api/click/counter";
//			string MysqlIP = "http://8tad.ir/api/show/counter";
			AE.InsertCounterLogsToMysql(ShowMysqlIP, ClickMysqlIP);
			AE.RedisSet("LastMysqlUpdate", to_string(cmin));
		}
		LastUpdate = AE.RedisGet("LastCheatUpdate");
		Hour = currTime->tm_hour;
		if(LastUpdate != "")
			Hour = stoi(LastUpdate);
		int chour = currTime->tm_hour;
		if(Hour != chour)
		{
			AE.DeleteCheatsAndAttacks();
			AE.RedisSet("LastCheatUpdate", to_string(chour));
		}
		cout<<"End, Bye..."<<endl;
//		sleep(10);
//	}
	return 0;
}