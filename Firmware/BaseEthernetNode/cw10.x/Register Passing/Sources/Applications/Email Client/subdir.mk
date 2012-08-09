################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Email Client/email_client.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Email\ Client/email_client.c \

OBJS += \
./Sources/Applications/Email\ Client/email_client_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/Email Client/email_client_c.obj" \

C_DEPS += \
./Sources/Applications/Email\ Client/email_client_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/Email\ Client/email_client_c.obj \

C_DEPS_QUOTED += \
"./Sources/Applications/Email Client/email_client_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Email\ Client/email_client_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Email\ Client/email_client.c
	@echo 'Building file: $<'
	@echo 'Executing target #96 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Email Client/email_client.args" -o "Sources/Applications/Email Client/email_client_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Email\ Client/email_client_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/APPLICATIONS/Email\ Client/email_client.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


