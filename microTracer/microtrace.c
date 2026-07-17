#include "microtrace.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <unistd.h>


void tracee(char* cmd[])
{
  execvp(cmd[0], cmd);
}

void t_pid(int pid){
  if(ptrace(PTRACE_ATTACH, pid, NULL, NULL)<0){
    die("error attaching to process");
  }
}

void show_syscall(unsigned int syscall_no, unsigned int syscall_ret){
  char* syscall_name = syscall_table[syscall_no];
  char* return_prefix = "";
  if(syscall_ret > 15){
    return_prefix = "0x";
  }
  printf("%-15s = %s%x\n", syscall_name, return_prefix, syscall_ret);
}

void tracer(int child_pid){
  int child_status;
  wait(&child_status);
  int syscall_count = 0;
  enum syscall_state syscall_state = BEFORE_SYSCALL;
  struct user_regs_struct tracee_regs;
  while(1){

    if(ptrace(PTRACE_SYSCALL, child_pid, NULL, NULL)<0){
      die("error tracing syscalls");
    }
    wait(&child_status);
    syscall_count += 1;

    if(WIFEXITED(child_status)){
      printf("syscall count=%d\n", syscall_count);
      printf("child status=%d\n", child_status);
      break;
    }

    if(ptrace(PTRACE_GETREGS, child_pid, NULL, &tracee_regs)<0){
      die("error reading registers");
    }
    if(syscall_state == AFTER_SYSCALL){
      unsigned int current_syscall_no = tracee_regs.orig_rax;
      unsigned int current_syscall_return = tracee_regs.rax;
      show_syscall(current_syscall_no, current_syscall_return);
      syscall_state = BEFORE_SYSCALL;
    }
    else{
      syscall_state = AFTER_SYSCALL;
    }

  }
}

int main(int argc, char* argv[]){
  if(strcmp(argv[1], "-p")==0)
  {
    int pid = atoi(argv[2]);
    t_pid(pid);
    tracer(pid);
  }
  else{
    int pid = fork();
    switch(pid){
      case -1:
        die("error forking");
        break;
      case 0:
        tracee(argv+1);
        break;
      default:
        tracer(pid);
        break;
    }
  }
  return 0;
}
