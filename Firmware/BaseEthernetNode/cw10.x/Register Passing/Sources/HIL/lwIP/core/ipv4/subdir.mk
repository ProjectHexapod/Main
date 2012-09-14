################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/autoip.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/icmp.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/igmp.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/autoip.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/icmp.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/igmp.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c 

OBJS += \
./Sources/HIL/lwIP/core/ipv4/autoip_c.obj \
./Sources/HIL/lwIP/core/ipv4/icmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/igmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj 

OBJS_QUOTED += \
"./Sources/HIL/lwIP/core/ipv4/autoip_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/icmp_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/igmp_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/inet_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/ip_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj" \
"./Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj" 

C_DEPS += \
./Sources/HIL/lwIP/core/ipv4/autoip_c.d \
./Sources/HIL/lwIP/core/ipv4/icmp_c.d \
./Sources/HIL/lwIP/core/ipv4/igmp_c.d \
./Sources/HIL/lwIP/core/ipv4/inet_c.d \
./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.d \
./Sources/HIL/lwIP/core/ipv4/ip_c.d \
./Sources/HIL/lwIP/core/ipv4/ip_addr_c.d \
./Sources/HIL/lwIP/core/ipv4/ip_frag_c.d 

OBJS_OS_FORMAT += \
./Sources/HIL/lwIP/core/ipv4/autoip_c.obj \
./Sources/HIL/lwIP/core/ipv4/icmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/igmp_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_c.obj \
./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj \
./Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj 

C_DEPS_QUOTED += \
"./Sources/HIL/lwIP/core/ipv4/autoip_c.d" \
"./Sources/HIL/lwIP/core/ipv4/icmp_c.d" \
"./Sources/HIL/lwIP/core/ipv4/igmp_c.d" \
"./Sources/HIL/lwIP/core/ipv4/inet_c.d" \
"./Sources/HIL/lwIP/core/ipv4/inet_chksum_c.d" \
"./Sources/HIL/lwIP/core/ipv4/ip_c.d" \
"./Sources/HIL/lwIP/core/ipv4/ip_addr_c.d" \
"./Sources/HIL/lwIP/core/ipv4/ip_frag_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/HIL/lwIP/core/ipv4/autoip_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/autoip.c
	@echo 'Building file: $<'
	@echo 'Executing target #51 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/autoip.args" -o "Sources/HIL/lwIP/core/ipv4/autoip_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/autoip_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/autoip.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/icmp_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/icmp.c
	@echo 'Building file: $<'
	@echo 'Executing target #52 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/icmp.args" -o "Sources/HIL/lwIP/core/ipv4/icmp_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/icmp_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/icmp.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/igmp_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/igmp.c
	@echo 'Building file: $<'
	@echo 'Executing target #53 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/igmp.args" -o "Sources/HIL/lwIP/core/ipv4/igmp_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/igmp_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/igmp.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet.c
	@echo 'Building file: $<'
	@echo 'Executing target #54 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/inet.args" -o "Sources/HIL/lwIP/core/ipv4/inet_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c
	@echo 'Building file: $<'
	@echo 'Executing target #55 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/inet_chksum.args" -o "Sources/HIL/lwIP/core/ipv4/inet_chksum_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/inet_chksum_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/inet_chksum.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip.c
	@echo 'Building file: $<'
	@echo 'Executing target #56 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/ip.args" -o "Sources/HIL/lwIP/core/ipv4/ip_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c
	@echo 'Building file: $<'
	@echo 'Executing target #57 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/ip_addr.args" -o "Sources/HIL/lwIP/core/ipv4/ip_addr_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_addr_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_addr.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c
	@echo 'Building file: $<'
	@echo 'Executing target #58 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/core/ipv4/ip_frag.args" -o "Sources/HIL/lwIP/core/ipv4/ip_frag_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/core/ipv4/ip_frag_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/core/ipv4/ip_frag.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


