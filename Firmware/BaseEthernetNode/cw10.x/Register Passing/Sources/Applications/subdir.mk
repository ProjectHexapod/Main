################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/defaults.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/defaults.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c 

OBJS += \
./Sources/Applications/defaults_c.obj \
./Sources/Applications/main_c.obj 

OBJS_QUOTED += \
"./Sources/Applications/defaults_c.obj" \
"./Sources/Applications/main_c.obj" 

C_DEPS += \
./Sources/Applications/defaults_c.d \
./Sources/Applications/main_c.d 

OBJS_OS_FORMAT += \
./Sources/Applications/defaults_c.obj \
./Sources/Applications/main_c.obj 

C_DEPS_QUOTED += \
"./Sources/Applications/defaults_c.d" \
"./Sources/Applications/main_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/defaults_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/defaults.c
	@echo 'Building file: $<'
	@echo 'Executing target #11 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/defaults.args" -o "Sources/Applications/defaults_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/defaults_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/defaults.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Applications/main_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c
	@echo 'Building file: $<'
	@echo 'Executing target #12 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/main.args" -o "Sources/Applications/main_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/main_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


