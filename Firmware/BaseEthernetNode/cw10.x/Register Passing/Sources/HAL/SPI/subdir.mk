################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SPI/spi.c" 

C_SRCS += \
/home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SPI/spi.c 

OBJS += \
./Sources/HAL/SPI/spi_c.obj 

OBJS_QUOTED += \
"./Sources/HAL/SPI/spi_c.obj" 

C_DEPS += \
./Sources/HAL/SPI/spi_c.d 

OBJS_OS_FORMAT += \
./Sources/HAL/SPI/spi_c.obj 

C_DEPS_QUOTED += \
"./Sources/HAL/SPI/spi_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/HAL/SPI/spi_c.obj: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SPI/spi.c
	@echo 'Building file: $<'
	@echo 'Executing target #76 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HAL/SPI/spi.args" -o "Sources/HAL/SPI/spi_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HAL/SPI/spi_c.d: /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/SPI/spi.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


