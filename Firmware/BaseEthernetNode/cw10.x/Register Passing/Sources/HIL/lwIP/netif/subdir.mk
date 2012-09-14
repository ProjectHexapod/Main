################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/etharp.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/ethernetif.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/loopif.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/slipif.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/etharp.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/ethernetif.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/loopif.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/slipif.c 

OBJS += \
./Sources/HIL/lwIP/netif/etharp_c.obj \
./Sources/HIL/lwIP/netif/ethernetif_c.obj \
./Sources/HIL/lwIP/netif/loopif_c.obj \
./Sources/HIL/lwIP/netif/slipif_c.obj 

OBJS_QUOTED += \
"./Sources/HIL/lwIP/netif/etharp_c.obj" \
"./Sources/HIL/lwIP/netif/ethernetif_c.obj" \
"./Sources/HIL/lwIP/netif/loopif_c.obj" \
"./Sources/HIL/lwIP/netif/slipif_c.obj" 

C_DEPS += \
./Sources/HIL/lwIP/netif/etharp_c.d \
./Sources/HIL/lwIP/netif/ethernetif_c.d \
./Sources/HIL/lwIP/netif/loopif_c.d \
./Sources/HIL/lwIP/netif/slipif_c.d 

OBJS_OS_FORMAT += \
./Sources/HIL/lwIP/netif/etharp_c.obj \
./Sources/HIL/lwIP/netif/ethernetif_c.obj \
./Sources/HIL/lwIP/netif/loopif_c.obj \
./Sources/HIL/lwIP/netif/slipif_c.obj 

C_DEPS_QUOTED += \
"./Sources/HIL/lwIP/netif/etharp_c.d" \
"./Sources/HIL/lwIP/netif/ethernetif_c.d" \
"./Sources/HIL/lwIP/netif/loopif_c.d" \
"./Sources/HIL/lwIP/netif/slipif_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/HIL/lwIP/netif/etharp_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/etharp.c
	@echo 'Building file: $<'
	@echo 'Executing target #14 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/netif/etharp.args" -o "Sources/HIL/lwIP/netif/etharp_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/netif/etharp_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/etharp.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/netif/ethernetif_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/ethernetif.c
	@echo 'Building file: $<'
	@echo 'Executing target #15 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/netif/ethernetif.args" -o "Sources/HIL/lwIP/netif/ethernetif_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/netif/ethernetif_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/ethernetif.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/netif/loopif_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/loopif.c
	@echo 'Building file: $<'
	@echo 'Executing target #16 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/netif/loopif.args" -o "Sources/HIL/lwIP/netif/loopif_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/netif/loopif_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/loopif.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/HIL/lwIP/netif/slipif_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/slipif.c
	@echo 'Building file: $<'
	@echo 'Executing target #17 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/lwIP/netif/slipif.args" -o "Sources/HIL/lwIP/netif/slipif_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/lwIP/netif/slipif_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HIL/lwIP/src/netif/slipif.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


