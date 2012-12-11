################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c" \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c 

S_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/mcf5xxx.s 

S_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/mcf5xxx.s" 

OBJS += \
./Project\ Settings/Startup\ Code/exceptions_c.obj \
./Project\ Settings/Startup\ Code/mcf5xxx_s.obj \
./Project\ Settings/Startup\ Code/startcf_c.obj 

OBJS_QUOTED += \
"./Project Settings/Startup Code/exceptions_c.obj" \
"./Project Settings/Startup Code/mcf5xxx_s.obj" \
"./Project Settings/Startup Code/startcf_c.obj" 

C_DEPS += \
./Project\ Settings/Startup\ Code/exceptions_c.d \
./Project\ Settings/Startup\ Code/startcf_c.d 

OBJS_OS_FORMAT += \
./Project\ Settings/Startup\ Code/exceptions_c.obj \
./Project\ Settings/Startup\ Code/mcf5xxx_s.obj \
./Project\ Settings/Startup\ Code/startcf_c.obj 

C_DEPS_QUOTED += \
"./Project Settings/Startup Code/exceptions_c.d" \
"./Project Settings/Startup Code/startcf_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Project\ Settings/Startup\ Code/exceptions_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c
	@echo 'Building file: $<'
	@echo 'Executing target #13 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Project Settings/Startup Code/exceptions.args" -o "Project Settings/Startup Code/exceptions_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Project\ Settings/Startup\ Code/exceptions_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Project\ Settings/Startup\ Code/mcf5xxx_s.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/mcf5xxx.s
	@echo 'Building file: $<'
	@echo 'Executing target #14 $<'
	@echo 'Invoking: ColdFire Assembler'
	"$(CF_ToolsDirEnv)/mwasmmcf" @@"Project Settings/Startup Code/mcf5xxx.args" -o "Project Settings/Startup Code/mcf5xxx_s.obj" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Project\ Settings/Startup\ Code/startcf_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c
	@echo 'Building file: $<'
	@echo 'Executing target #15 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Project Settings/Startup Code/startcf.args" -o "Project Settings/Startup Code/startcf_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Project\ Settings/Startup\ Code/startcf_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


