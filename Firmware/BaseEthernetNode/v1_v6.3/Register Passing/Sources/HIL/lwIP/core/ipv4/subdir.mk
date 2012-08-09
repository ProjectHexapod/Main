################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/autoip.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/icmp.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/igmp.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/inet.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/ip.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c" \

C_SRCS += \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/autoip.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/icmp.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/igmp.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/inet.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c \

OBJS += \
./Sources/HIL/lwIP/core/ipv4/autoip_c.obj \
./Sources/HIL/lwIP/core/ipv4/icmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/igmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj \

OBJS_QUOTED += \
"./Sources/HIL/lwIP/core/ipv4/autoip_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/icmp_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/igmp_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/inet_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/ip_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj" \

C_DEPS += \
./Sources/HIL/lwIP/core/ipv4/autoip_c.d \
./Sources/HIL/lwIP/core/ipv4/icmp_c.d \
./Sources/HIL/lwIP/core/ipv4/igmp_c.d \
./Sources/HIL/lwIP/core/ipv4/inet_c.d \
./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.d \
./Sources/HIL/lwIP/core/ipv4/ip_c.d \
./Sources/HIL/lwIP/core/ipv4/ip_addr_c.d \
./Sources/HIL/lwIP/core/ipv4/ip_frag_c.d \

OBJS_OS_FORMAT += \
./Sources/HIL/lwIP/core/ipv4/autoip_c.obj \
./Sources/HIL/lwIP/core/ipv4/icmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/igmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj \


# Each subdirectory must supply rules for building sources it contributes
Sources/HIL/lwIP/core/ipv4/autoip_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/autoip.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/autoip.args" -o "Sources/HIL/lwIP/core/ipv4/autoip_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/autoip_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/autoip.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/icmp_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/icmp.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/icmp.args" -o "Sources/HIL/lwIP/core/ipv4/icmp_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/icmp_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/icmp.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/igmp_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/igmp.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/igmp.args" -o "Sources/HIL/lwIP/core/ipv4/igmp_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/igmp_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/igmp.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/inet.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/inet.args" -o "Sources/HIL/lwIP/core/ipv4/inet_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/inet.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/inet_chksum.args" -o "Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_chksum_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/ip.args" -o "Sources/HIL/lwIP/core/ipv4/ip_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/ip_addr.args" -o "Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_addr_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/ip_frag.args" -o "Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_frag_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


