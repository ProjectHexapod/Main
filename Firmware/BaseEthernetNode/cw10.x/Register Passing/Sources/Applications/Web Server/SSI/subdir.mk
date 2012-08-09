################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_ssi.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_ssi.c \

OBJS += \
./Sources/Applications/Web\ Server/SSI/http_ssi_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/Web Server/SSI/http_ssi_c.obj" \

C_DEPS += \
./Sources/Applications/Web\ Server/SSI/http_ssi_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/Web\ Server/SSI/http_ssi_c.obj \

C_DEPS_QUOTED += \
"./Sources/Applications/Web Server/SSI/http_ssi_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Web\ Server/SSI/http_ssi_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_ssi.c
	@echo 'Building file: $<'
	@echo 'Executing target #86 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Web Server/SSI/http_ssi.args" -o "Sources/Applications/Web Server/SSI/http_ssi_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Web\ Server/SSI/http_ssi_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_ssi.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


