#include "tcpmodule.h"

void stage2(string ip, string port)
{
	const char* logo = R"(                                                                                                              
        ,--,                                                                                                  
      ,--.'|                                    ____                                                          
   ,--,  | :                                  ,'  , `.                                                        
,---.'|  : '           ,---.               ,-+-,.' _ |                                                        
|   | : _' |          '   ,'\           ,-+-. ;   , ||                                                        
:   : |.'  |         /   /   |         ,--.'|'   |  ||           ,---.                .--,            ,---.   
|   ' '  ; :        .   ; ,. :        |   |  ,', |  |,          /     \             /_ ./|           /     \  
'   |  .'. |        '   | |: :        |   | /  | |--'          /    /  |         , ' , ' :          /    /  | 
|   | :  | '        '   | .; :        |   : |  | ,            .    ' / |        /___/ \: |         .    ' / | 
'   : |  : ;        |   :    |        |   : |  |/             '   ;   /|         .  \  ' |         '   ;   /| 
|   | '  ,/          \   \  /         |   | |`-'              '   |  / |          \  ;   :         '   |  / | 
;   : ;--'            `----'          |   ;/                  |   :    |           \  \  ;         |   :    | 
|   ,/                                '---'                    \   \  /             :  \  \         \   \  /  
'---'                                                           `----'               \  ' ;          `----'   
                                              Homeye Project                          `--`                    )";

	if (IsConsoleVisible()) {
		HideConsole();
	}

	while (true) {
		std::cout << "[Homeye] (info) Trying stage2..." << endl;
		WSADATA wsa_data;
		SOCKADDR_IN addr;
		int result;
		char buffer[512];
		char* to_return;
		string message;

		WSAStartup(MAKEWORD(2, 0), &wsa_data);
		const auto server = socket(AF_INET, SOCK_STREAM, 0);

		string stemp = string(ip.begin(), ip.end());
		PCSTR sw = stemp.c_str();
		InetPton(AF_INET, sw, &addr.sin_addr.s_addr);

		addr.sin_family = AF_INET;
		addr.sin_port = htons(stoi(port));

		result = connect(server, reinterpret_cast<SOCKADDR*>(&addr), sizeof(addr));
		if (result == SOCKET_ERROR) {
			closesocket(server);
			WSACleanup();
			Sleep(5000);
			continue;
		}
		std::cout << "[Homeye] (info) Connected to server!" << endl;

		while (true) {
			while (true) {
				recv(server, buffer, sizeof(buffer), 0);
				message += buffer;
				std::cout << message << endl;
				if (message.find('}') != string::npos) {
					std::cout << "escaped" << endl;
					break;
				}
				else {
					std::cout << message.back() << endl;
				}
			}
			json jmsg = json::parse(message);
			string type = jmsg["type"];
			if (type == "error") {
				string msg = jmsg["msg"];
				//ShowWindow(GetConsoleWindow(), SW_SHOW);
				ShowConsole();
				std::cout << "[Homeye] (error) " << msg << endl;
				system("pause");
			}
			else if (type == "ssh") {
				string hostname = jmsg["ip"];
				int port = jmsg["port"];
				string username = jmsg["user"];
				string password = jmsg["password"];
				system("cls");
				std::cout << logo << endl << endl;
				ShowConsole();
				openssh(hostname, port, username, password);
				HideConsole();
				system("cls");
			}

			message = "";
			memset(buffer, 0, 512);
		}
	}
}