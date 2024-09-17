#include <iostream>
#include <vector> 
#include <windows.h>
#include <stdlib.h>
#include <stdio.h>
#include <sstream>
#include <string>
#include <regex>

using namespace std;

void HideConsole();
void ShowConsole();
bool IsConsoleVisible();
static std::string implode(const std::vector<std::string> elems, char delim);
vector<string> split2(string s, string splitter);