################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common Utilities/alloc.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common Utilities/assert.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common Utilities/io.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common Utilities/printf.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common Utilities/rand.c" \
"C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common Utilities/stdlib.c" \

C_SRCS += \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/alloc.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/assert.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/io.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/printf.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/rand.c \
C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/stdlib.c \

OBJS += \
./Sources/Services/Common\ Utilities/alloc_c.obj \
./Sources/Services/Common\ Utilities/assert_c.obj \
./Sources/Services/Common\ Utilities/io_c.obj \
./Sources/Services/Common\ Utilities/printf_c.obj \
./Sources/Services/Common\ Utilities/rand_c.obj \
./Sources/Services/Common\ Utilities/stdlib_c.obj \

OBJS_QUOTED += \
"./Sources/Services/Common Utilities/alloc_c.obj" \
"./Sources/Services/Common Utilities/assert_c.obj" \
"./Sources/Services/Common Utilities/io_c.obj" \
"./Sources/Services/Common Utilities/printf_c.obj" \
"./Sources/Services/Common Utilities/rand_c.obj" \
"./Sources/Services/Common Utilities/stdlib_c.obj" \

C_DEPS += \
./Sources/Services/Common\ Utilities/alloc_c.d \
./Sources/Services/Common\ Utilities/assert_c.d \
./Sources/Services/Common\ Utilities/io_c.d \
./Sources/Services/Common\ Utilities/printf_c.d \
./Sources/Services/Common\ Utilities/rand_c.d \
./Sources/Services/Common\ Utilities/stdlib_c.d \

OBJS_OS_FORMAT += \
./Sources/Services/Common\ Utilities/alloc_c.obj \
./Sources/Services/Common\ Utilities/assert_c.obj \
./Sources/Services/Common\ Utilities/io_c.obj \
./Sources/Services/Common\ Utilities/printf_c.obj \
./Sources/Services/Common\ Utilities/rand_c.obj \
./Sources/Services/Common\ Utilities/stdlib_c.obj \

C_DEPS_QUOTED += \
"./Sources/Services/Common Utilities/alloc_c.d" \
"./Sources/Services/Common Utilities/assert_c.d" \
"./Sources/Services/Common Utilities/io_c.d" \
"./Sources/Services/Common Utilities/printf_c.d" \
"./Sources/Services/Common Utilities/rand_c.d" \
"./Sources/Services/Common Utilities/stdlib_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Services/Common\ Utilities/alloc_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/alloc.c
	@echo 'Building file: $<'
	@echo 'Executing target #8 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/Common Utilities/alloc.args" -o "Sources/Services/Common Utilities/alloc_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/Common\ Utilities/alloc_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/alloc.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/Common\ Utilities/assert_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/assert.c
	@echo 'Building file: $<'
	@echo 'Executing target #9 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/Common Utilities/assert.args" -o "Sources/Services/Common Utilities/assert_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/Common\ Utilities/assert_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/assert.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/Common\ Utilities/io_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/io.c
	@echo 'Building file: $<'
	@echo 'Executing target #10 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/Common Utilities/io.args" -o "Sources/Services/Common Utilities/io_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/Common\ Utilities/io_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/io.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/Common\ Utilities/printf_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/printf.c
	@echo 'Building file: $<'
	@echo 'Executing target #11 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/Common Utilities/printf.args" -o "Sources/Services/Common Utilities/printf_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/Common\ Utilities/printf_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/printf.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/Common\ Utilities/rand_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/rand.c
	@echo 'Building file: $<'
	@echo 'Executing target #12 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/Common Utilities/rand.args" -o "Sources/Services/Common Utilities/rand_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/Common\ Utilities/rand_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/rand.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

Sources/Services/Common\ Utilities/stdlib_c.obj: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/stdlib.c
	@echo 'Building file: $<'
	@echo 'Executing target #13 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Services/Common Utilities/stdlib.args" -o "Sources/Services/Common Utilities/stdlib_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Services/Common\ Utilities/stdlib_c.d: C:/Users/jwhong/Documents/Project-Hexapod/Firmware/BaseEthernetNode/Sources/Services/Common\ Utilities/stdlib.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


