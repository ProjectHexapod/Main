################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/Services/FreeRTOS/Sources/croutine.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/Services/FreeRTOS/Sources/list.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/Services/FreeRTOS/Sources/queue.c" \
"C:/Users/jwhong/Desktop/M51CN128RD SW/Sources/Services/FreeRTOS/Sources/tasks.c" \

C_SRCS += \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/croutine.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/list.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/queue.c \
C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/tasks.c \

OBJS += \
./Sources/Services/FreeRTOS/Source/croutine_c.obj \
./Sources/Services/FreeRTOS/Source/list_c.obj \
./Sources/Services/FreeRTOS/Source/queue_c.obj \
./Sources/Services/FreeRTOS/Source/tasks_c.obj \

OBJS_QUOTED += \
"./Sources/Services/FreeRTOS/Source/croutine_c.obj" \
"./Sources/Services/FreeRTOS/Source/list_c.obj" \
"./Sources/Services/FreeRTOS/Source/queue_c.obj" \
"./Sources/Services/FreeRTOS/Source/tasks_c.obj" \

C_DEPS += \
./Sources/Services/FreeRTOS/Source/croutine_c.d \
./Sources/Services/FreeRTOS/Source/list_c.d \
./Sources/Services/FreeRTOS/Source/queue_c.d \
./Sources/Services/FreeRTOS/Source/tasks_c.d \

OBJS_OS_FORMAT += \
./Sources/Services/FreeRTOS/Source/croutine_c.obj \
./Sources/Services/FreeRTOS/Source/list_c.obj \
./Sources/Services/FreeRTOS/Source/queue_c.obj \
./Sources/Services/FreeRTOS/Source/tasks_c.obj \


# Each subdirectory must supply rules for building sources it contributes
Sources/Services/FreeRTOS/Source/croutine_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/croutine.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/FreeRTOS/Source/croutine.args" -o "Sources/Services/FreeRTOS/Source/croutine_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/FreeRTOS/Source/croutine_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/croutine.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/FreeRTOS/Source/list_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/list.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/FreeRTOS/Source/list.args" -o "Sources/Services/FreeRTOS/Source/list_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/FreeRTOS/Source/list_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/list.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/FreeRTOS/Source/queue_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/queue.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/FreeRTOS/Source/queue.args" -o "Sources/Services/FreeRTOS/Source/queue_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/FreeRTOS/Source/queue_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/queue.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/FreeRTOS/Source/tasks_c.obj: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/tasks.c
	@echo 'Building file: $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/FreeRTOS/Source/tasks.args" -o "Sources/Services/FreeRTOS/Source/tasks_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/FreeRTOS/Source/tasks_c.d: C:/Users/jwhong/Desktop/M51CN128RD\ SW/Sources/Services/FreeRTOS/Sources/tasks.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


