#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

int main() {
    const char *filename = "test_file.txt";
    const char *message = "Hello, SystemCallExplorer!\n";
    
    // Open file for writing (create if doesn't exist)
    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    
    // Write data to file
    ssize_t bytes_written = write(fd, message, strlen(message));
    if (bytes_written == -1) {
        perror("write");
        close(fd);
        return 1;
    }
    
    printf("Written %zd bytes to %s\n", bytes_written, filename);
    
    // Close the file
    if (close(fd) == -1) {
        perror("close");
        return 1;
    }
    
    // Now read the file back
    fd = open(filename, O_RDONLY);
    if (fd == -1) {
        perror("open for reading");
        return 1;
    }
    
    char buffer[256];
    ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
    if (bytes_read == -1) {
        perror("read");
        close(fd);
        return 1;
    }
    
    buffer[bytes_read] = '\0';
    printf("Read %zd bytes: %s", bytes_read, buffer);
    
    close(fd);
    
    // Clean up
    if (unlink(filename) == -1) {
        perror("unlink");
        return 1;
    }
    
    printf("File operations completed successfully!\n");
    return 0;
}