################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"$(MCUToolsBaseDirEnv)/ColdFire_Support/Derivatives/device/src/mcf51cn128.c" \

C_SRCS += \
$(MCUToolsBaseDirEnv_ESCAPED)/ColdFire_Support/Derivatives/device/src/mcf51cn128.c \

OBJS += \
./Libs/mcf51cn128_c.obj \

OBJS_QUOTED += \
"./Libs/mcf51cn128_c.obj" \

C_DEPS += \
./Libs/MCF51CN128_C.d \

OBJS_OS_FORMAT += \
./Libs/mcf51cn128_c.obj \

C_DEPS_QUOTED += \
"./Libs/MCF51CN128_C.d" \


# Each subdirectory must supply rules for building sources it contributes
Libs/mcf51cn128_c.obj: $(MCUToolsBaseDirEnv_ESCAPED)/ColdFire_Support/Derivatives/device/src/mcf51cn128.c
	@echo 'Building file: $<'
	@echo 'Executing target #103 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Libs/MCF51CN128.args" -o "Libs/mcf51cn128_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Libs/MCF51CN128_C.d: $(MCUToolsBaseDirEnv_ESCAPED)/ColdFire_Support/Derivatives/device/src/mcf51cn128.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


