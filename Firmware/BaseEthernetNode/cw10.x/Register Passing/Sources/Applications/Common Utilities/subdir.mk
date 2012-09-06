################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Utilities/utilities.c" \

C_SRCS += \
E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Utilities/utilities.c \

OBJS += \
./Sources/Applications/Common\ Utilities/utilities_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/Common Utilities/utilities_c.obj" \

C_DEPS += \
./Sources/Applications/Common\ Utilities/utilities_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/Common\ Utilities/utilities_c.obj \

C_DEPS_QUOTED += \
"./Sources/Applications/Common Utilities/utilities_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Common\ Utilities/utilities_c.obj: E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Utilities/utilities.c
	@echo 'Building file: $<'
	@echo 'Executing target #93 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Common Utilities/utilities.args" -o "Sources/Applications/Common Utilities/utilities_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Common\ Utilities/utilities_c.d: E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Utilities/utilities.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


