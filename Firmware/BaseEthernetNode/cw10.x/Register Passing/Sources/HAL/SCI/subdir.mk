################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SCI/uart.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SCI/uart.c 

OBJS += \
./Sources/HAL/SCI/uart_c.obj 

OBJS_QUOTED += \
"./Sources/HAL/SCI/uart_c.obj" 

C_DEPS += \
./Sources/HAL/SCI/uart_c.d 

OBJS_OS_FORMAT += \
./Sources/HAL/SCI/uart_c.obj 

C_DEPS_QUOTED += \
"./Sources/HAL/SCI/uart_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/HAL/SCI/uart_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SCI/uart.c
	@echo 'Building file: $<'
	@echo 'Executing target #4 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HAL/SCI/uart.args" -o "Sources/HAL/SCI/uart_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HAL/SCI/uart_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SCI/uart.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


