################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c \

S_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/mcf5xxx.s \

S_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/mcf5xxx.s" \

OBJS += \
./Project\ Settings/Startup\ Code/exceptions_c.obj \
./Project\ Settings/Startup\ Code/mcf5xxx_s.obj \
./Project\ Settings/Startup\ Code/startcf_c.obj \

OBJS_QUOTED += \
"./Project Settings/Startup Code/exceptions_c.obj" \
"./Project Settings/Startup Code/mcf5xxx_s.obj" \
"./Project Settings/Startup Code/startcf_c.obj" \

C_DEPS += \
./Project\ Settings/Startup\ Code/exceptions_c.d \
./Project\ Settings/Startup\ Code/startcf_c.d \

OBJS_OS_FORMAT += \
./Project\ Settings/Startup\ Code/exceptions_c.obj \
./Project\ Settings/Startup\ Code/mcf5xxx_s.obj \
./Project\ Settings/Startup\ Code/startcf_c.obj \

C_DEPS_QUOTED += \
"./Project Settings/Startup Code/exceptions_c.d" \
"./Project Settings/Startup Code/startcf_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Project\ Settings/Startup\ Code/exceptions_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c
	@echo 'Building file: $<'
	@echo 'Executing target #94 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Project Settings/Startup Code/exceptions.args" -o "Project Settings/Startup Code/exceptions_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Project\ Settings/Startup\ Code/exceptions_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/exceptions.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Project\ Settings/Startup\ Code/mcf5xxx_s.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/mcf5xxx.s
	@echo 'Building file: $<'
	@echo 'Executing target #95 $<'
	@echo 'Invoking: ColdFire Assembler'
	"$(CF_ToolsDirEnv)/mwasmmcf" @@"Project Settings/Startup Code/mcf5xxx.args" -o "Project Settings/Startup Code/mcf5xxx_s.obj" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Project\ Settings/Startup\ Code/startcf_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c
	@echo 'Building file: $<'
	@echo 'Executing target #96 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Project Settings/Startup Code/startcf.args" -o "Project Settings/Startup Code/startcf_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Project\ Settings/Startup\ Code/startcf_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/startcf.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


