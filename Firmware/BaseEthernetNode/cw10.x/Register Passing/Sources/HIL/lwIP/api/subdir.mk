################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_lib.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_msg.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/err.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netbuf.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netdb.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netifapi.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/sockets.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/tcpip.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_lib.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_msg.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/err.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netbuf.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netdb.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netifapi.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/sockets.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/tcpip.c \

OBJS += \
./Sources/HIL/lwIP/api/api_lib_c.obj \
./Sources/HIL/lwIP/api/api_msg_c.obj \
./Sources/HIL/lwIP/api/err_c.obj \
./Sources/HIL/lwIP/api/netbuf_c.obj \
./Sources/HIL/lwIP/api/netdb_c.obj \
./Sources/HIL/lwIP/api/netifapi_c.obj \
./Sources/HIL/lwIP/api/sockets_c.obj \
./Sources/HIL/lwIP/api/tcpip_c.obj \

OBJS_QUOTED += \
"./Sources/HIL/lwIP/api/api_lib_c.obj" \
"./Sources/HIL/lwIP/api/api_msg_c.obj" \
"./Sources/HIL/lwIP/api/err_c.obj" \
"./Sources/HIL/lwIP/api/netbuf_c.obj" \
"./Sources/HIL/lwIP/api/netdb_c.obj" \
"./Sources/HIL/lwIP/api/netifapi_c.obj" \
"./Sources/HIL/lwIP/api/sockets_c.obj" \
"./Sources/HIL/lwIP/api/tcpip_c.obj" \

C_DEPS += \
./Sources/HIL/lwIP/api/api_lib_c.d \
./Sources/HIL/lwIP/api/api_msg_c.d \
./Sources/HIL/lwIP/api/err_c.d \
./Sources/HIL/lwIP/api/netbuf_c.d \
./Sources/HIL/lwIP/api/netdb_c.d \
./Sources/HIL/lwIP/api/netifapi_c.d \
./Sources/HIL/lwIP/api/sockets_c.d \
./Sources/HIL/lwIP/api/tcpip_c.d \

OBJS_OS_FORMAT += \
./Sources/HIL/lwIP/api/api_lib_c.obj \
./Sources/HIL/lwIP/api/api_msg_c.obj \
./Sources/HIL/lwIP/api/err_c.obj \
./Sources/HIL/lwIP/api/netbuf_c.obj \
./Sources/HIL/lwIP/api/netdb_c.obj \
./Sources/HIL/lwIP/api/netifapi_c.obj \
./Sources/HIL/lwIP/api/sockets_c.obj \
./Sources/HIL/lwIP/api/tcpip_c.obj \

C_DEPS_QUOTED += \
"./Sources/HIL/lwIP/api/api_lib_c.d" \
"./Sources/HIL/lwIP/api/api_msg_c.d" \
"./Sources/HIL/lwIP/api/err_c.d" \
"./Sources/HIL/lwIP/api/netbuf_c.d" \
"./Sources/HIL/lwIP/api/netdb_c.d" \
"./Sources/HIL/lwIP/api/netifapi_c.d" \
"./Sources/HIL/lwIP/api/sockets_c.d" \
"./Sources/HIL/lwIP/api/tcpip_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/HIL/lwIP/api/api_lib_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_lib.c
	@echo 'Building file: $<'
	@echo 'Executing target #61 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/api_lib.args" -o "Sources/HIL/lwIP/api/api_lib_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/api_lib_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_lib.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/api/api_msg_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_msg.c
	@echo 'Building file: $<'
	@echo 'Executing target #62 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/api_msg.args" -o "Sources/HIL/lwIP/api/api_msg_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/api_msg_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/api_msg.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/api/err_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/err.c
	@echo 'Building file: $<'
	@echo 'Executing target #63 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/err.args" -o "Sources/HIL/lwIP/api/err_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/err_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/err.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/api/netbuf_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netbuf.c
	@echo 'Building file: $<'
	@echo 'Executing target #64 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/netbuf.args" -o "Sources/HIL/lwIP/api/netbuf_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/netbuf_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netbuf.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/api/netdb_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netdb.c
	@echo 'Building file: $<'
	@echo 'Executing target #65 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/netdb.args" -o "Sources/HIL/lwIP/api/netdb_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/netdb_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netdb.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/api/netifapi_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netifapi.c
	@echo 'Building file: $<'
	@echo 'Executing target #66 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/netifapi.args" -o "Sources/HIL/lwIP/api/netifapi_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/netifapi_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/netifapi.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/api/sockets_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/sockets.c
	@echo 'Building file: $<'
	@echo 'Executing target #67 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/sockets.args" -o "Sources/HIL/lwIP/api/sockets_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/sockets_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/sockets.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/api/tcpip_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/tcpip.c
	@echo 'Building file: $<'
	@echo 'Executing target #68 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/api/tcpip.args" -o "Sources/HIL/lwIP/api/tcpip_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/api/tcpip_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/api/tcpip.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


