################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FEC/fec.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FEC/fec.c 

OBJS += \
./Sources/HAL/FEC/fec_c.obj 

OBJS_QUOTED += \
"./Sources/HAL/FEC/fec_c.obj" 

C_DEPS += \
./Sources/HAL/FEC/fec_c.d 

OBJS_OS_FORMAT += \
./Sources/HAL/FEC/fec_c.obj 

C_DEPS_QUOTED += \
"./Sources/HAL/FEC/fec_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/HAL/FEC/fec_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FEC/fec.c
	@echo 'Building file: $<'
	@echo 'Executing target #9 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HAL/FEC/fec.args" -o "Sources/HAL/FEC/fec_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HAL/FEC/fec_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FEC/fec.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


