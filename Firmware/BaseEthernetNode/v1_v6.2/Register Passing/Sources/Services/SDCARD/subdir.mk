################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/Services/SDCARD/SD.c" \

C_SRCS += \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/SDCARD/SD.c \

OBJS += \
./Sources/Services/SDCARD/SD_c.obj \

OBJS_QUOTED += \
"./Sources/Services/SDCARD/SD_c.obj" \

C_DEPS += \
./Sources/Services/SDCARD/SD_c.d \

OBJS_OS_FORMAT += \
./Sources/Services/SDCARD/SD_c.obj \

C_DEPS_QUOTED += \
"./Sources/Services/SDCARD/SD_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Services/SDCARD/SD_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/SDCARD/SD.c
	@echo 'Building file: $<'
	@echo 'Executing target #1 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/SDCARD/SD.args" -o "Sources/Services/SDCARD/SD_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/SDCARD/SD_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/SDCARD/SD.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


