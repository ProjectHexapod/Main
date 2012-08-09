################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/APPLICATIONS/WEB/static_web_pages.c" \

C_SRCS += \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/WEB/static_web_pages.c \

OBJS += \
./Sources/Applications/Web\ Server/Static\ Web\ Pages/static_web_pages_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/Web Server/Static Web Pages/static_web_pages_c.obj" \

C_DEPS += \
./Sources/Applications/Web\ Server/Static\ Web\ Pages/static_web_pages_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/Web\ Server/Static\ Web\ Pages/static_web_pages_c.obj \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Web\ Server/Static\ Web\ Pages/static_web_pages_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/WEB/static_web_pages.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Web Server/Static Web Pages/static_web_pages.args" -o "Sources/Applications/Web Server/Static Web Pages/static_web_pages_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Web\ Server/Static\ Web\ Pages/static_web_pages_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/APPLICATIONS/WEB/static_web_pages.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


