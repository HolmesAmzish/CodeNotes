# Makefile 示例

# 编译器
CC = gcc

# 编译选项
CFLAGS = -Wall

# 目标可执行文件
TARGET = program

# 源文件
SRCS = main.c hello.c

# 生成的目标文件
OBJS = $(SRCS:.c=.o)

# 默认目标
all: $(TARGET)

# 编译目标文件
$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET)

# 编译 .c 文件为 .o 文件
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# 清理目标
clean:
	rm -f $(OBJS) $(TARGET)
