#define _WIN32_WINNT 0x600

#include "json.hpp"
#ifdef _WIN32
	#include <winsock2.h>
	#include <ws2tcpip.h>
#endif
#include "utils.h"
#include "ssh.h"

#define DEFAULT_BUFLEN 512

using json = nlohmann::json;

void stage2(string ip, string port);
vector<string> split(string to_split);