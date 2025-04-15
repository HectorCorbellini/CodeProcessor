#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

int main(int argc, char *argv[]) {
    // Path to the Python interpreter (relative to the executable)
    const char *python_exe = "python\\python.exe";
    
    // Path to the main script (relative to the executable)
    const char *script = "main.py";
    
    // Build the command
    char command[512];
    snprintf(command, sizeof(command), "\"%s\" \"%s\"", python_exe, script);
    
    // Display a message
    printf("Launching Code Processor...\n");
    
    // Execute the command
    system(command);
    
    return 0;
}
