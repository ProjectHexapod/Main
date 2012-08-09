################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/APPLICATIONS/UIF Terminal/uif_terminal.c" \

C_SRCS += \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/UIF\ Terminal/uif_terminal.c \

OBJS += \
./Sources/Applications/User\ Interface/uif_terminal_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/User Interface/uif_terminal_c.obj" \

C_DEPS += \
./Sources/Applications/User\ Interface/uif_terminal_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/User\ Interface/uif_terminal_c.obj \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/User\ Interface/uif_terminal_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/UIF\ Terminal/uif_terminal.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/User Interface/uif_terminal.args" -o "Sources/Applications/User Interface/uif_terminal_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/User\ Interface/uif_terminal_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/UIF\ Terminal/uif_terminal.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


