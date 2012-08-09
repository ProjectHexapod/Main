################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/APPLICATIONS/WEB/http_cgi.c" \

C_SRCS += \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/WEB/http_cgi.c \

OBJS += \
./Sources/Applications/Web\ Server/CGI/http_cgi_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/Web Server/CGI/http_cgi_c.obj" \

C_DEPS += \
./Sources/Applications/Web\ Server/CGI/http_cgi_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/Web\ Server/CGI/http_cgi_c.obj \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Web\ Server/CGI/http_cgi_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/WEB/http_cgi.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Web Server/CGI/http_cgi.args" -o "Sources/Applications/Web Server/CGI/http_cgi_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Web\ Server/CGI/http_cgi_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/WEB/http_cgi.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


