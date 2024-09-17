#include <iostream>
#include "tcpmodule.h"
#include "ssh.h"
#include <shellapi.h>
using namespace std;

//please finish this for me -_-

vector<string> connect(string ip, string port)
{
    WSADATA wsa_data;
    SOCKADDR_IN addr;
    int result;
    char buffer[512];
    char* to_return;

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
        return vector<string> {"1"};
    }
    std::cout << "[Homeye] (info) Connected to server!" << endl;
    HideConsole();

    recv(server, buffer, sizeof(buffer), 0);
    string clean_txt = regex_replace(buffer, std::regex("[^a-zA-Z0-9 ]"), "");
    closesocket(server);
    WSACleanup();
    return split(clean_txt);
}

int main()
{
    string ip = "169.254.1.1";
    string port = "3467";
    string portv2 = "3468";
    string ipv2;
    string hostloader;
    bool usingv2 = false;

    cout << "[Homeye] (info) Hello :3 !" << endl;
    cout << "[Homeye] (info) Installing windows RNDIS driver..." << endl;
    int returnCode = system("pnputil /add-driver .driver/RNDIS.inf /install");
    if (returnCode == 0) {
        cout << "[Homeye] (info) Successfully installed" << endl;
    }
    else {
        cout << "[Homeye] (warning) Error installing driver. If your system does not have it, please install it manually" << endl;
        cout << "[Homeye] (warning) Driver path : .driver / RNDIS.inf" << endl;
    }
    cout << "[Homeye] (info) Sending \"run\" message to usb module" << endl;
    system("echo \"\" > .run");

    while (true) {
        cout << "[Homeye] (info) Trying to connect homeye module..." << endl;
        vector<string> result = connect(ip, port);
        if (result[0] != "1") {
            cout << "[Homeye] (module)" << " ";
            for (string element : result) {
                cout << element << " ";
            }
            cout << endl;
            ip = result[0];
            ipv2 = result[1];
            port = result[2];
            portv2 = result[3];
            hostloader = result[4];
            if (!usingv2) {
                string startweb = "http://" + ip + ":" + port + "/";
                string stemp = string(startweb.begin(), startweb.end());
                PCSTR sw = stemp.c_str();
                ShellExecute(0, 0, sw, 0, 0, SW_SHOW);
            }
            else {
                string startweb = "http://" + ipv2 + ":" + port + "/";
                string stemp = string(startweb.begin(), startweb.end());
                PCSTR sw = stemp.c_str();
                ShellExecute(0, 0, sw, 0, 0, SW_SHOW);
            }
            break;
        }

        Sleep(5000);
    }

    stage2(ip, portv2);
    system("pause");

    return 0;
}