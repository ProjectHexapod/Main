################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/FTP Server/ftp_server.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/FTP\ Server/ftp_server.c \

OBJS += \
./Sources/Applications/FTP\ Server/ftp_server_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/FTP Server/ftp_server_c.obj" \

C_DEPS += \
./Sources/Applications/FTP\ Server/ftp_server_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/FTP\ Server/ftp_server_c.obj \

C_DEPS_QUOTED += \
"./Sources/Applications/FTP Server/ftp_server_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/FTP\ Server/ftp_server_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/FTP\ Server/ftp_server.c
	@echo 'Building file: $<'
	@echo 'Executing target #95 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/FTP Server/ftp_server.args" -o "Sources/Applications/FTP Server/ftp_server_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/FTP\ Server/ftp_server_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/FTP\ Server/ftp_server.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


