#include "ssh.h"

void openssh(string host, int port, string username, string password)
{
    CkSsh ssh;

    const char* hostname = host.c_str();

    bool success = ssh.Connect(hostname, port);
    if (success != true) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    ssh.put_IdleTimeoutMs(5000);

    success = ssh.AuthenticatePw(username.c_str(), password.c_str());
    if (success != true) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    int channelNum;
    channelNum = ssh.OpenSessionChannel();
    if (channelNum < 0) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    const char* termType = "dumb";
    int widthInChars = 120;
    int heightInChars = 40;
    int pixWidth = 0;
    int pixHeight = 0;
    success = ssh.SendReqPty(channelNum, termType, widthInChars, heightInChars, pixWidth, pixHeight);
    if (success != true) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    success = ssh.SendReqShell(channelNum);
    if (success != true) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    int i = 0;

    while (true) {
        int n;
        int pollTimeoutMs = 2000;
        n = ssh.ChannelReadAndPoll(channelNum, pollTimeoutMs);
        if (n < 0) {
            cout << ssh.lastErrorText() << "\r\n";
            return;
        }

        const char* cmdOutput = ssh.getReceivedText(channelNum, "ansi");
        if (ssh.get_LastMethodSuccess() != true) {
            cout << ssh.lastErrorText() << "\r\n";
            return;
        }

        if (i == 0) {
            std::istringstream input(cmdOutput);
            list<string> out_;
            string out;

            for (std::string line; getline(input, line);)
                out_.push_back(line);

            for (string& line : out_) {
                out += (line + "\n");
            }
            string a = out_.back();
            a.pop_back();

            cout << a << flush;
            cout << " ";
        }
        else {
            std::istringstream input(cmdOutput);
            list<string> out_;
            string out;

            for (std::string line; getline(input, line);)
                out_.push_back(line);

            out_.pop_front();
            out_.pop_back();

            for (string& line : out_) {
                out += (line + "\n");
            }

            out.pop_back();
            string a = out_.back();
            a.pop_back();

            cout << out;
            cout << a;
        }

        string command;
        getline(cin, command);
        if (command == "exit") {
            break;
        }
        command += "\r\n";

        success = ssh.ChannelSendString(channelNum, command.data(), "ansi");
        if (success != true) {
            cout << ssh.lastErrorText() << "\r\n";
            return;
        }
        i++;
    }

    success = ssh.ChannelSendClose(channelNum);
    if (success != true) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    success = ssh.ChannelReceiveToClose(channelNum);
    if (success != true) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    const char* cmdOutput = ssh.getReceivedText(channelNum, "ansi");
    if (ssh.get_LastMethodSuccess() != true) {
        cout << ssh.lastErrorText() << "\r\n";
        return;
    }

    cout << cmdOutput << "\r\n";

    ssh.Disconnect();
}