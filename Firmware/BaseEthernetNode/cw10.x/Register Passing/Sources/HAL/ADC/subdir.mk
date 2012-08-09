################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/ADC/adc.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/ADC/adc.c \

OBJS += \
./Sources/HAL/ADC/adc_c.obj \

OBJS_QUOTED += \
"./Sources/HAL/ADC/adc_c.obj" \

C_DEPS += \
./Sources/HAL/ADC/adc_c.d \

OBJS_OS_FORMAT += \
./Sources/HAL/ADC/adc_c.obj \

C_DEPS_QUOTED += \
"./Sources/HAL/ADC/adc_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/HAL/ADC/adc_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/ADC/adc.c
	@echo 'Building file: $<'
	@echo 'Executing target #85 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HAL/ADC/adc.args" -o "Sources/HAL/ADC/adc_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HAL/ADC/adc_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/ADC/adc.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


