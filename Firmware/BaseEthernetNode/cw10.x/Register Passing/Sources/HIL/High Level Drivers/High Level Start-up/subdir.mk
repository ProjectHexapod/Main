################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/High Level Drivers/High Level Startup/mcu_init.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/High\ Level\ Drivers/High\ Level\ Startup/mcu_init.c \

OBJS += \
./Sources/HIL/High\ Level\ Drivers/High\ Level\ Start-up/mcu_init_c.obj \

OBJS_QUOTED += \
"./Sources/HIL/High Level Drivers/High Level Start-up/mcu_init_c.obj" \

C_DEPS += \
./Sources/HIL/High\ Level\ Drivers/High\ Level\ Start-up/mcu_init_c.d \

OBJS_OS_FORMAT += \
./Sources/HIL/High\ Level\ Drivers/High\ Level\ Start-up/mcu_init_c.obj \

C_DEPS_QUOTED += \
"./Sources/HIL/High Level Drivers/High Level Start-up/mcu_init_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/HIL/High\ Level\ Drivers/High\ Level\ Start-up/mcu_init_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/High\ Level\ Drivers/High\ Level\ Startup/mcu_init.c
	@echo 'Building file: $<'
	@echo 'Executing target #73 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/High Level Drivers/High Level Start-up/mcu_init.args" -o "Sources/HIL/High Level Drivers/High Level Start-up/mcu_init_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/High\ Level\ Drivers/High\ Level\ Start-up/mcu_init_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HIL/High\ Level\ Drivers/High\ Level\ Startup/mcu_init.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


