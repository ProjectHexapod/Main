################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Configuration Interface/serial_configuration.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Configuration\ Interface/serial_configuration.c 

OBJS += \
./Sources/Applications/Configuration\ Interface/serial_configuration_c.obj 

OBJS_QUOTED += \
"./Sources/Applications/Configuration Interface/serial_configuration_c.obj" 

C_DEPS += \
./Sources/Applications/Configuration\ Interface/serial_configuration_c.d 

OBJS_OS_FORMAT += \
./Sources/Applications/Configuration\ Interface/serial_configuration_c.obj 

C_DEPS_QUOTED += \
"./Sources/Applications/Configuration Interface/serial_configuration_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Configuration\ Interface/serial_configuration_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Configuration\ Interface/serial_configuration.c
	@echo 'Building file: $<'
	@echo 'Executing target #86 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Configuration Interface/serial_configuration.args" -o "Sources/Applications/Configuration Interface/serial_configuration_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Configuration\ Interface/serial_configuration_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Configuration\ Interface/serial_configuration.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


