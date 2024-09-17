#include "utils.h"

void HideConsole()
{
    ::ShowWindow(::GetConsoleWindow(), SW_HIDE);
}

void ShowConsole()
{
    ::ShowWindow(::GetConsoleWindow(), SW_SHOW);
}

bool IsConsoleVisible()
{
    return ::IsWindowVisible(::GetConsoleWindow()) != FALSE;
}

vector<string> split(string to_split)
{
    string s;
    vector<string> v;
    string str(to_split);
    //cout << "\"" << str << "\"" << endl;
    //str.pop_back();
    stringstream ss(str);

    while (getline(ss, s, ' ')) {
        v.push_back(s);
    }

    return v;
}

static std::string implode(const std::vector<std::string> elems, char delim)
{
    std::string s;

    for (std::vector<std::string>::const_iterator ii = elems.begin(); ii != elems.end(); ++ii)
    {
        s += (*ii);
        if (ii + 1 != elems.end()) {
            s += delim;
        }
    }

    return s;
}

vector<string> split2(string s, string splitter) {
    vector<string> res;
    int pos = 0;
    while (pos < s.size()) {
        pos = s.find(splitter);
        res.push_back(s.substr(0, pos));
        s.erase(0, pos + 3);
    }
    return res;
}
