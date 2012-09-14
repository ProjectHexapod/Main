################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/static_web_pages.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/static_web_pages.c 

OBJS += \
./Sources/Applications/main_c.obj \
./Sources/Applications/static_web_pages_c.obj 

OBJS_QUOTED += \
"./Sources/Applications/main_c.obj" \
"./Sources/Applications/static_web_pages_c.obj" 

C_DEPS += \
./Sources/Applications/main_c.d \
./Sources/Applications/static_web_pages_c.d 

OBJS_OS_FORMAT += \
./Sources/Applications/main_c.obj \
./Sources/Applications/static_web_pages_c.obj 

C_DEPS_QUOTED += \
"./Sources/Applications/main_c.d" \
"./Sources/Applications/static_web_pages_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/main_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c
	@echo 'Building file: $<'
	@echo 'Executing target #84 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/main.args" -o "Sources/Applications/main_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/main_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/main.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Applications/static_web_pages_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/static_web_pages.c
	@echo 'Building file: $<'
	@echo 'Executing target #85 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/static_web_pages.args" -o "Sources/Applications/static_web_pages_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/static_web_pages_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/static_web_pages.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


