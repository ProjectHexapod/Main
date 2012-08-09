################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/SPI bridge/spi_bridge.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/SPI\ bridge/spi_bridge.c \

OBJS += \
./Sources/Applications/Serial\ Bridge/SPI\ Bridge/spi_bridge_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/Serial Bridge/SPI Bridge/spi_bridge_c.obj" \

C_DEPS += \
./Sources/Applications/Serial\ Bridge/SPI\ Bridge/spi_bridge_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/Serial\ Bridge/SPI\ Bridge/spi_bridge_c.obj \

C_DEPS_QUOTED += \
"./Sources/Applications/Serial Bridge/SPI Bridge/spi_bridge_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Serial\ Bridge/SPI\ Bridge/spi_bridge_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/SPI\ bridge/spi_bridge.c
	@echo 'Building file: $<'
	@echo 'Executing target #93 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Serial Bridge/SPI Bridge/spi_bridge.args" -o "Sources/Applications/Serial Bridge/SPI Bridge/spi_bridge_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Serial\ Bridge/SPI\ Bridge/spi_bridge_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/SPI\ bridge/spi_bridge.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


